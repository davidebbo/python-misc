#!/usr/bin/env python3
'''
Build the entire OneZoom tree from the saved parts
'''

import argparse
import logging
import os
import sys
from getOpenTreesFromOneZoom_fast import enumerate_one_zoom_tokens
from token_to_oz_tree_file_mapping import token_to_file_map

def trim_tree(tree):
    # Skip the comment block at the start of the file, if any
    if '[' in tree:
        tree = tree[tree.index(']')+1:]

    # Trim any whitespace
    tree = tree.strip()

    # Strip the trailing semicolon
    if tree[-1] == ';':
        tree = tree[:-1]

    return tree
    
def expand_newick(oz_file, sub_trees_folder, output_stream):
    logging.debug(f'Expanding {oz_file}')

    with open(oz_file, 'r', encoding="utf8") as stream:
        tree = stream.read()

    tree = trim_tree(tree)
    index = 0

    # Get the One Zoom include file folder from the path to the file
    oz_folder = os.path.dirname(oz_file)

    for result in enumerate_one_zoom_tokens(tree):
        output_stream.write(tree[index:result['start']])

        if 'base_ott' in result:
            ot_part_file = os.path.join(sub_trees_folder, f'{result["base_ott"]}.phy')

            # Check if the file exists
            if os.path.exists(ot_part_file):
                with open(ot_part_file, 'r', encoding="utf8") as stream:
                    ot_part_tree = stream.read()
                ot_part_tree = trim_tree(ot_part_tree)
                output_stream.write(ot_part_tree)
                logging.debug(f"Processed OT part file {ot_part_file}")
            else:
                logging.warning(f"Subtree file {ot_part_file} does not exist")
        else:
            oz_sub_file_name = token_to_file_map[result["full_name"]][0]
            oz_sub_file = os.path.join(oz_folder, oz_sub_file_name)

            if os.path.exists(oz_sub_file):
                expand_newick(oz_sub_file, sub_trees_folder, output_stream)
            else:
                logging.warning(f"OZ file {oz_sub_file} does not exist")

        index = result['end']
        
    output_stream.write(tree[index:])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verbosity', '-v', action='count', default=0, help='verbosity level: output extra non-essential info')
    parser.add_argument('treefile', help='The base tree file in newick form')
    parser.add_argument('subtreesfolder', help='The folder containing the subtree files')
    parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
    args = parser.parse_args()

    if args.verbosity==0:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    elif args.verbosity==1:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    elif args.verbosity==2:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    expand_newick(args.treefile, args.subtreesfolder, args.outfile)
    args.outfile.write(';')
