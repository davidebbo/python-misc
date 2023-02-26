#!/usr/bin/env python3
'''
Extract a minimal subtree that contains all the passed in taxa and their closest ancestors.
'''

import argparse
import logging
import re
import sys
from typing import Set

non_name_regex = re.compile(r'[,;:\(\)]')

def extract(newick_tree, target_taxa: Set[str], excluded_taxa: Set[str] = {},
            expand_taxa: bool = False, separate_trees: bool = False):
    # We build the node and exclusion lists as we find them and process them
    nodes = []
    excluded_ranges = []

    # Clone the taxa set so we don't modify the original
    target_taxa = set(target_taxa)

    # It doesn't make sense not to expand if we're separating trees
    if separate_trees:
        expand_taxa = True

    index = 0
    index_stack = []

    # Helper function to raise a syntax error with extra context
    def raise_syntax_error(message):
        raise SyntaxError(f'Syntax error: {message}. Index={index}, Text="{newick_tree[index-20:index+20]}"')

    while target_taxa or (len(nodes) >= 2 and not separate_trees):
        if newick_tree[index] == ';':
            break

        if newick_tree[index] == '(':
            index_stack.append(index)
            index += 1
            continue

        closed_brace = newick_tree[index] == ')'
        if closed_brace:
            # A closed brace cannot follow a comma
            if newick_tree[index-1] == ',':
                raise_syntax_error(f"unexpected comma")

            index += 1

            # Set the start index to the beginning of the node (where the open parenthesis is)
            try:
                node_start_index = index_stack.pop()
            except IndexError:
                raise_syntax_error(f"unmatched closed brace")

            # But if we're not supposed to expand the taxon, just set it to here, so we just have the taxon name
            if not expand_taxa:
                node_start_index = index
        else:
            node_start_index = index

        found_target_taxon = False
        taxon = ott_id = None

        full_name_start_index = index
        if newick_tree[index] == "'":
            # This is a quoted name, so we need to find the end of the name
            end_quote_index = newick_tree.index("'", index+1)

            taxon = newick_tree[index+1:end_quote_index]
            index = end_quote_index + 1
        else:
            # This may be an unquoted name, so we need to find the end
            match = non_name_regex.search(newick_tree, index)
            if match:
                index = match.start()
                taxon = newick_tree[full_name_start_index:index]

        # After the taxon, there may be an edge length
        edge_length = None
        if newick_tree[index] == ':':
            index += 1
            match = non_name_regex.search(newick_tree, index)
            if match:
                edge_length = newick_tree[index:match.start()]
                index = match.start()
            if not edge_length:
                raise_syntax_error(f"expected an edge length after a colon")

        # There should be a taxon, except after a closed brace where it's optional            
        if not (taxon or edge_length) and not closed_brace:
            raise_syntax_error(f"expected a taxon or an edge length (e.g. 'foo', 'foo:1.0', or ':1.0')")

        if taxon:
            # Check if the taxon has an ott id, and if so, parse it out
            if '_ott' in taxon:
                ott_index = taxon.index('_ott')
                ott_id = taxon[ott_index+4:]
                taxon = taxon[:ott_index]

            if taxon in target_taxa or ott_id in target_taxa:
                # We've found a target taxon, so remove it from the target list
                target_taxa.remove(taxon if taxon in target_taxa else ott_id)
                found_target_taxon = True
            
            if taxon in excluded_taxa or ott_id in excluded_taxa:
                # Add the excluded range, with different logic depending on comma position
                if newick_tree[node_start_index-1] == ',':
                    excluded_range = (node_start_index-1, index)
                elif newick_tree[index] == ',':
                    excluded_range = (node_start_index, index+1)
                else:
                    excluded_range = (node_start_index, index)
                excluded_ranges.append(excluded_range)
                # Sort the excluded ranges by start index. Not efficient, but not on critical path
                excluded_ranges.sort(key=lambda x: x[0])

        if found_target_taxon or closed_brace:
            # Any node with higher depth must be a child of this one
            # But ignore the whole child logic if we're separating trees
            children = [n for n in nodes if n["depth"] > len(index_stack)] if not separate_trees else []

            # Assert that all the children have depth 1 less than this node. This is
            # because any deeper nodes would have been bubbled up 
            assert all([node["depth"] == len(index_stack) + 1 for node in children])

            # Reduce the depth of the children to bubble them up
            for node in children:
                node["depth"] -= 1

            # If we found a taxon, or there are multiple children, we need to create a node for this one
            if found_target_taxon or len(children) > 1:
                # Remove the children from the search list
                nodes = [n for n in nodes if n not in children]

                # This conditional is a little more complex than I'd like, but we need to
                # handle a number of cases. There are two types of nodes we can create:
                # 1. A node that contains a full substring of the original tree, further split into:
                #    a. Only include the taxon's name
                #    b. Include the taxon's name and its entire subtree
                # 2. A node that just wraps the children as if they were siblings
                tree_string = ""
                if found_target_taxon and (expand_taxa or not children):
                    def string_to_append(start, end):
                        # Fix up situation that would end up generating "(,"
                        if tree_string and tree_string[-1] == '(' and newick_tree[start] == ',':
                            start += 1
                        return newick_tree[start:end]

                    # Put together the tree substring for this node, but with the excluded ranges removed
                    prev_range = (node_start_index, node_start_index)
                    for range in excluded_ranges:
                        # Only process ranges that are inside the current taxon
                        if range[0] > node_start_index and range[0] < index and range[1] > prev_range[1]:
                            tree_string += string_to_append(prev_range[1], range[0])
                            prev_range = range
                    tree_string += string_to_append(prev_range[1], index)
                else:
                    # Full name including the edge length
                    full_name = newick_tree[full_name_start_index:index]
                    tree_string = f"({','.join([node['tree_string'] for node in children])}){full_name}"

                nodes.append({"name": taxon, "ott": ott_id, "tree_string": tree_string, "depth": len(index_stack)})

        if newick_tree[index] == ',':
            index += 1
    
    if target_taxa:
        logging.warning(f'Could not find the following taxa: {", ".join(target_taxa)}')

    if separate_trees:
        # If we're separating trees, return a dictionary of trees, indexed by ott or name
        return {node['ott'] or node['name']: node['tree_string'] for node in nodes}

    # Otherwise return the one tree left, if any
    assert len(nodes) <= 1
    return nodes[0]['tree_string'] if len(nodes) > 0 else None

def main(args):
    target_taxa = set(args.taxa)
    excluded_taxa = set(args.excluded_taxa) if args.excluded_taxa else set()
    expand_taxa = args.expand_taxa

    # If not specified, only expand if there is only one taxon, since it's not meaningful
    # to ask for a single non-expanded taxon
    if not expand_taxa:
        expand_taxa = len(target_taxa) == 1

    # Read the whole file as a string. This is not ideal, but it's still
    # very fast even with the full OpenTree tree.
    # This could be optimized to read by chunks, with more complexity
    tree = args.treefile.read()

    result = extract(tree, target_taxa, excluded_taxa, expand_taxa, args.separate_trees)

    if args.separate_trees:
        for name, tree in result.items():
            args.outfile.write(f'{name}: {tree};\n')
    elif result:
        args.outfile.write(result + ';\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('treefile', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help='The tree file in newick form')
    parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
    parser.add_argument('--taxa', '-t', nargs='+', required=True, help='the taxon to search for')
    parser.add_argument('--excluded_taxa', '-x', nargs='+', help='taxa to exclude from the result')
    parser.add_argument('--expand_taxa', '-e', action=argparse.BooleanOptionalAction, help='whether found subtrees should be expanded')
    parser.add_argument('--separate_trees', '-s', action=argparse.BooleanOptionalAction, help='found subtrees should not be merged into a single tree')
    args = parser.parse_args()
    main(args)
