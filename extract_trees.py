#!/usr/bin/env python3
'''
Extract one or more taxa from a Newick tree, including support for excluded taxa.
'''

import argparse
import logging
import sys
from fast_newick_parser import parse_tree
from typing import Set

def extract(newick_tree, target_taxa: Set[str], excluded_taxa: Set[str] = {}):
    # We build the node and exclusion lists as we find them and process them
    nodes = []
    excluded_ranges = []

    # Clone the taxa set so we don't modify the original
    target_taxa = set(target_taxa)

    for node in parse_tree(newick_tree):
        taxon = node['taxon']
        ott_id = node['ott_id']
        node_start_index = node['start']
        node_end_index = node['end']

        # If this taxon is in the excluded list, add it to the excluded ranges
        if taxon in excluded_taxa or ott_id in excluded_taxa:
            # Use different logic depending on comma position
            if newick_tree[node_start_index-1] == ',':
                excluded_range = (node_start_index-1, node_end_index)
            elif newick_tree[node_end_index] == ',':
                excluded_range = (node_start_index, node_end_index+1)
            else:
                excluded_range = (node_start_index, node_end_index)
            excluded_ranges.append(excluded_range)
            # Sort the excluded ranges by start index. Not efficient, but not on critical path
            excluded_ranges.sort(key=lambda x: x[0])

        # If this taxon is in the target list, add it to the nodes list
        if taxon in target_taxa or ott_id in target_taxa:
            target_taxa.remove(taxon if taxon in target_taxa else ott_id)

            tree_string = ""

            def string_to_append(start, end):
                # Fix up situation that would end up generating "(,"
                if tree_string and tree_string[-1] == '(' and newick_tree[start] == ',':
                    start += 1
                return newick_tree[start:end]

            # Put together the tree substring for this node, but with the excluded ranges removed
            prev_range = (node_start_index, node_start_index)
            for range in excluded_ranges:
                # Only process ranges that are inside the current taxon
                if range[0] > node_start_index and range[0] < node_end_index and range[1] > prev_range[1]:
                    tree_string += string_to_append(prev_range[1], range[0])
                    prev_range = range
            tree_string += string_to_append(prev_range[1], node_end_index)

            nodes.append({"name": taxon, "ott": ott_id, "tree_string": tree_string})

        # If we've found all the target taxa, we're done
        if not target_taxa:
            break

    if target_taxa:
        logging.warning(f'Could not find the following taxa: {", ".join(target_taxa)}')

    # Return a dictionary of trees, indexed by ott or name
    return {node['ott'] or node['name']: node['tree_string'] for node in nodes}


def main(args):
    target_taxa = set(args.taxa)
    excluded_taxa = set(args.excluded_taxa) if args.excluded_taxa else set()

    # Read the whole file as a string. This is not ideal, but it's still
    # very fast even with the full OpenTree tree.
    # This could be optimized to read by chunks, with more complexity
    tree = args.treefile.read()

    result = extract(tree, target_taxa, excluded_taxa)

    # Check if result is a dict, indicating multiple trees
    for name, tree in result.items():
        args.outfile.write(f'{name}: {tree};\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('treefile', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help='The tree file in newick form')
    parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
    parser.add_argument('--taxa', '-t', nargs='+', required=True, help='the taxon to search for')
    parser.add_argument('--excluded_taxa', '-x', nargs='+', help='taxa to exclude from the result')
    args = parser.parse_args()
    main(args)
