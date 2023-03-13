#!/usr/bin/env python3
'''
Extract one or more subtrees from a Newick tree, including support for excluded taxa.
'''

'''
Everything is processed in a single pass over the tree string, using the newick_parser module.
As we walk through the nodes, we process both the target taxa and the excluded taxa.

From the command line, run for example:
python3 extract_trees.py tree.tre -t Tupaia Camelidae
'''


import argparse
import sys

from newick.extract_trees_impl import extract_trees

__author__ = "David Ebbo"

def main(args):
    target_taxa = set(args.taxa)
    excluded_taxa = set(args.excluded_taxa) if args.excluded_taxa else set()

    # Read the whole file as a string. This is not ideal, but it's still very fast
    # even with the full OpenTree tree, and the memory usage is acceptable.
    # This could be optimized to read by chunks, with much more complexity.
    tree = args.treefile.read()

    result = extract_trees(tree, target_taxa, excluded_taxa)

    if len(result) == 1:
        # If only one result, just output the tree
        args.outfile.write(f'{next(iter(result.values()))};\n')
    else:
        # If multiple items, output each on a separate line, prefixed with the name/ott
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
