#!/usr/bin/env python3
'''
Extract a minimal subtree that conatins all the passed in taxa and their closest ancestors.
'''

import argparse
import sys
import re


whole_token_regex = re.compile('[^(),;]*')
taxon_regex = re.compile('\w*')

def extract(tree, taxa, excluded_taxa={}, expand_taxa=False):
    # We build the node list as we find them and process them
    nodes = []
    excluded_ranges = []

    # Clone the taxa set so we don't modify the original
    taxa = set(taxa)

    index = 0
    index_stack = []

    while taxa or len(nodes) >= 2:
        if index == len(tree) or tree[index] == ';':
            break

        if tree[index] == '(':
            index_stack.append(index)
            index += 1
            continue

        closed_brace = tree[index] == ')'
        if closed_brace:
            index += 1

            # Set the start index to the begining of the taxon (where the open parenthesis is)
            start_index = index_stack.pop()

            # But if we're not supposed to expand the taxon, just set it to here, so we just have the taxon name
            if not expand_taxa:
                start_index = index
        else:
            start_index = index

        match_full_name = whole_token_regex.match(tree, index)
        index = match_full_name.end()

        # This is a bit of a hack to optimize the regex. Challenge is that '_ott'
        # is made of valid word characters, so replacing it with '%' makes it more
        # efficient to parse, as it just goes till the next non-word character
        full_name = match_full_name.group().replace('_ott', '%')
        if (match_taxon_regex := taxon_regex.match(full_name)):
            found_taxon = False
            taxon = match_taxon_regex.group(0)
            if taxon in taxa:
                # We've found a taxon, so remove it from the list
                taxa.remove(taxon)
                found_taxon = True
            elif taxon in excluded_taxa:
                # Add the excluded range, with different logic depending on comma position
                if tree[index] == ',':
                    excluded_ranges.append((start_index, index+1))
                elif tree[start_index-1] == ',':
                    excluded_ranges.append((start_index-1, index))
                else:
                    excluded_ranges.append((start_index, index))

        if found_taxon or closed_brace:
            # Any node with higher depth must be a child of this one
            children = [n for n in nodes if n["depth"] > len(index_stack)]

            # Assert that all the children have depth 1 less than this node. This is
            # because any deeper nodes would have been bubbled up 
            assert all([node["depth"] == len(index_stack) + 1 for node in children])

            # Reduce the depth of the children to bubble them up
            for node in children:
                node["depth"] -= 1

            # If we found a taxon, or there are multiple children, we need to create a node for this one
            if found_taxon or len(children) > 1:
                # Remove the children from the search list
                nodes = [n for n in nodes if n not in children]

                # This conditional is a little more complex than I'd like, but we need to
                # handle a number of cases. There are two types of nodes we can create:
                # 1. A node that contains a full substring of the original tree, further split into:
                #    a. Only include the taxon's name
                #    b. Include the taxon's name and its entire subtree
                # 2. A node that just wraps the children as if they were siblings
                if found_taxon and (expand_taxa or not children):
                    # Put together the tree substring for this node, but with the excluded ranges removed
                    tree_string = ""
                    prev_range = (start_index, start_index)
                    for range in excluded_ranges:
                        # Only process ranges that are within the current node
                        if range[0] >= start_index and range[0] < index:
                            tree_string += tree[prev_range[1]:range[0]]
                            prev_range = range
                    tree_string += tree[prev_range[1]:index]

                    nodes.append({"tree_string": tree_string, "depth": len(index_stack)})
                else:
                    nodes.append({
                        "tree_string": f"({','.join([node['tree_string'] for node in children])}){match_full_name.group()}",
                        "depth": len(index_stack)})

        if tree[index] == ',':
            index += 1
    
    # Throw an error if we didn't find all the taxa
    if taxa:
        raise Exception(f'Could not find the following taxa: {", ".join(taxa)}')

    return nodes[0]['tree_string'] if not taxa else None



def main(args):
    taxa = set(args.taxa)
    expand_taxa = args.expand_taxa
    excluded_taxa = set(args.excluded_taxa) if args.excluded_taxa else set()

    # If not specified, only expand if there is only one taxon, since it's not meaningful
    # to ask for a single non-expanded taxon
    if not expand_taxa:
        expand_taxa = len(taxa) == 1

    # Read the whole file as a string. This is not ideal, but it's still
    # very fast even with the full OpenTree tree.
    # This could be optimized to read by chunks, with more complexity
    tree = args.treefile.read()

    result = extract(tree, taxa, excluded_taxa, expand_taxa)

    args.outfile.write(result + ';\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('treefile', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help='The tree file in newick form')
    parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
    parser.add_argument('--taxa', '-t', nargs='+', required=True, help='the taxon to search for')
    parser.add_argument('--excluded_taxa', '-x', nargs='+', help='taxas to exclude from the result')
    parser.add_argument('--expand_taxa', '-e', action=argparse.BooleanOptionalAction, help='whether found subtrees should be expanded')
    args = parser.parse_args()
    main(args)
