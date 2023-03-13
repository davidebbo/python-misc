#!/usr/bin/env python3
'''
Look for regex matches within files with very long lines (unlike grep, which matches entire lines).
The challenge is that the regex engine can't see the entire file at once, so we need to read the file in
chunks and stitch the chunks together before passing them to the regex engine.
'''

import argparse
import sys

from utilities.find_in_file import *

__author__ = "David Ebbo"

def main(args):
    for index, match in get_matches(chunks_from_file(args.file, args.chunk_size), args.regex, args.window_size):
        print(f"{index}: {match}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('regex', help='The expression to search for')
    parser.add_argument('file', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help='The input file')
    parser.add_argument('--window_size', '-w', type=int, default=100, help='the number of characters to display before and after each match')
    parser.add_argument('--chunk_size', '-c', type=int, default=10000, help='the size of the chunks to read from the file')
    args = parser.parse_args()
    main(args)
