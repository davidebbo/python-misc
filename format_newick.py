#!/usr/bin/env python3
'''
Format a newick tree with indentation to make it more human readable
'''

import argparse
import sys
from newick.format_newick_impl import format

__author__ = "David Ebbo"

def main(args):
    format(args.treefile.read(), args.outputfile, args.indent_spaces)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('treefile', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help='The tree file in newick format')
    parser.add_argument('outputfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
    parser.add_argument('--indent_spaces', '-i', default=2, type=int, help='the number of spaces for each indentation level')
    args = parser.parse_args()
    main(args)
