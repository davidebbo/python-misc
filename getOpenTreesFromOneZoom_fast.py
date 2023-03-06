#!/usr/bin/env python3
'''
Create subtrees from the Open Tree of Life, on the basis of ott numbers in a set of newick files.
'''

'''
foobar_ott123@ means create a node named foobar with ott 123, consisting of all descendants of 123 in the opentree.
foobar_ott123~456-789-111@ means create a node named foobar with ott 123, using ott456 minus the descendant subtrees 789 and 111
The tilde sign can be read an a equals (Dendropy doesn't like equals signs in taxon names)
foobar_ott123~-789-111@ is shorthand for foobar_ott123~123-789-111@
foobar_ott~456-789-111@ means create a node named foobar without any OTT number, using ott456 minus the descendant subtrees 789 and 111
'''

import argparse
import logging
import os
import re
import sys

import extract_trees

__author__ = "David Ebbo"

full_ott_token = re.compile(r"'?([\w\-~]+)@'?(?::([\d\.]+))?")
ott_details = re.compile(r"(\w+)_ott(\d*)~?([-\d]*)$")

'''
Enumerates all the OneZoom tokens in a tree string (e.g. foobar_ott123~-789-111)
'''
def enumerate_one_zoom_tokens(tree):
    # Skip the comment block at the start of the file
    start_index = tree.index(']') if '[' in tree else 0

    for full_match in full_ott_token.finditer(tree, start_index):
        result = {'start': full_match.start(), 'end': full_match.end(),
                  'full_name': full_match.group(1),
                  'edge_length': float(full_match.group(2)) if full_match.group(2) else None}

        # Check if it matches our tilde (aka 'equal') exclusion syntax
        match = ott_details.match(result['full_name'])
        if match:
            result['excluded_otts'] = (match.group(3) or '').split('-') #split by minus signs

            # If present, the first number after '=' is the tree to extract.
            first_number_after_equal = result['excluded_otts'].pop(0)
            result['base_ott'] = first_number_after_equal or match.group(2) 

            # Note that we don't append the ott in the name if it came after the '='
            result['full_name'] = match.group(1)
            if not first_number_after_equal:
                result['full_name'] += f"_ott{result['base_ott']}"

        logging.debug(result)
        yield result

'''
Find all the included and excluded ott numbers in a OneZoom files, and add them to the sets
'''
def get_inclusions_and_exclusions_from_one_zoom_file(file, all_included_otts, all_excluded_otts):
    with open(file, 'r', encoding="utf8") as stream:
        tree = stream.read()

    for result in enumerate_one_zoom_tokens(tree):
        # Check if the result has a base ott (won't have it if it's inserting another OZ file)
        if 'base_ott' in result:
            all_included_otts.add(result['base_ott'])
            all_excluded_otts.update(result['excluded_otts'])

'''
Extract the subtrees from the Open Tree file, based on the list of included/excluded otts
'''
def extract_trees_from_open_tree_file(open_tree_file, output_dir, all_included_otts, all_excluded_otts):
    # Read the contents of the open tree file into a string
    with open(open_tree_file, 'r', encoding="utf8") as f:
        fulltree = f.read()

    trees = extract_trees.extract(fulltree, all_included_otts, excluded_taxa=all_excluded_otts)

    logging.info(f"Extracted {len(trees)} trees from Open Tree file")

    # Save each tree to a file named after the taxon
    for ott, tree in trees.items():
        file = os.path.join(output_dir, ott + ".phy")
        logging.debug(f'Writing file: {file}')
        with open(file, "w", encoding="utf8") as f:
            f.write(tree)
            f.write(";\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verbosity', '-v', action='count', default=0, help='verbosity level: output extra non-essential info')
    parser.add_argument('open_tree_file', help='Path to the Open Tree newick file')
    parser.add_argument('output_dir', help='Path to the directory in which to save the OpenTree subtrees. See https://github.com/jrosindell/OneZoomTouch')
    parser.add_argument('parse_files', nargs='+', help='A list of newick files to parse for OTT numbers, giving the subtrees to extract.')
    args = parser.parse_args()

    if args.verbosity==0:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    elif args.verbosity==1:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    elif args.verbosity==2:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    if not os.path.isfile(args.open_tree_file):
        logging.warning("Could not find the OpenTree file {}".format(args.open_tree_file))

    included_otts = set()
    excluded_otts = set()

    for file in args.parse_files:
        logging.info(f"== Processing One Zoom file {file}")
        get_inclusions_and_exclusions_from_one_zoom_file(file, included_otts, excluded_otts)
    
    extract_trees_from_open_tree_file(args.open_tree_file, args.output_dir, included_otts, excluded_otts)
