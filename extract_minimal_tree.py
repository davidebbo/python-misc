#!/usr/bin/env python3

import argparse
import sys
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('treefile', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help='The tree file in newick form')
parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
parser.add_argument('--taxa', '-t', nargs='+', required=True, help='the taxon to search for')
parser.add_argument('--expand_taxa', '-x', action=argparse.BooleanOptionalAction, help='the taxon to search for')
args = parser.parse_args()

taxa = set(args.taxa)
expand_taxa = args.expand_taxa

# If not specified, only expand if there is only one taxon, since it's not meaningful
# to ask for a single non-expanded taxon
if not expand_taxa:
    expand_taxa = len(taxa) == 1

# Read the whole file as a string. This is not ideal, but it's still
# very fast even with the full OpenTree tree.
# This could be optimized to read by chunks, with more complexity
tree = args.treefile.read()

# We build the node list as we find them and process them
nodes = []

index = 0
index_stack = []

whole_token_regex = re.compile('[^(),;]*')
taxon_regex = re.compile('^(\w*?)(?:_ott(\d+))?(:[\d\.]*)?$')

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

        # But if we're not supposed to expand the taxon, just set it here, skipping the whole (...) block
        if not expand_taxa:
            start_index = index
    else:
        start_index = index

    match_full_name = whole_token_regex.match(tree, index)
    index += match_full_name.end() - index

    match_taxon = taxon_regex.match(match_full_name.group())
    if (match_taxon):
        taxon = match_taxon.group(1)
        if taxon in taxa:
            # We've found a taxon, so remove it from the list, and create a node for it
            taxa.remove(taxon)

            # Any node with higher depth must be a child of this one. Remove them from the search list
            children = [n for n in nodes if n["depth"] > len(index_stack)]
            nodes = [n for n in nodes if n not in children]

            if expand_taxa or not children:
                nodes.append(
                    {"tree_string": tree[start_index:index], "depth": len(index_stack)})
            else:
                # We're not expanding the taxon, so we need to wrap the children with the node
                nodes.append({
                    "tree_string": f"({','.join([node['tree_string'] for node in children])}){match_full_name.group()}",
                    "depth": len(index_stack)})

    if closed_brace:
        nodes_with_current_depth = [n for n in nodes if n["depth"] == len(index_stack) + 1]
        for node in nodes_with_current_depth:
            node["depth"] -= 1

        if len(nodes_with_current_depth) > 1:
            # We've found at least two nodes that match the current depth
            # Remove them from the list of nodes we're still looking for,
            # and replace them by a new node that wraps them
            nodes = [n for n in nodes if n not in nodes_with_current_depth]
            nodes.append(
                {"tree_string": f"({','.join([node['tree_string'] for node in nodes_with_current_depth])}){match_full_name.group()}",
                "depth": len(index_stack)})

    if tree[index] == ',':
        index += 1

if taxa:
    args.outfile.write(f'Could not find the following target taxa: {", ".join(taxa)}\n')
else:
    args.outfile.write(nodes[0]['tree_string'] + ";\n")
