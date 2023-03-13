#!/usr/bin/env python3
'''
Extract a minimal tree that includes a set of taxa
'''

import argparse
import sys
from newick.extract_minimal_tree_impl import extract_minimal_tree

__author__ = "David Ebbo"

def main(args):
    target_taxa = set(args.taxa)

    # Read the whole file as a string. This is not ideal, but it's still
    # very fast even with the full OpenTree tree.
    # This could be optimized to read by chunks, with more complexity
    tree = args.treefile.read()

    result = extract_minimal_tree(tree, target_taxa)
    if result:
        args.outfile.write(result + ';\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('treefile', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help='The tree file in newick form')
    parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
    parser.add_argument('--taxa', '-t', nargs='+', required=True, help='the taxa to search for')
    args = parser.parse_args()
    main(args)
