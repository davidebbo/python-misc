import argparse
import logging
import os
import re
import sys
import time

import extract_trees

ottRE = re.compile(r"(\w+)_ott([-~\d]+)\@")
id_pattern = re.compile(r"(\d*)~?([-\d]*)$")

def add_inclusions_and_exclusions_from_one_zoom_file(file, all_included_otts, all_excluded_otts):
    with open(file, 'r', encoding="utf8") as stream:
        tree = stream.read()
        for name, ottIDs in ottRE.findall(tree):
            match = id_pattern.match(ottIDs)
            if match:
                excluded_otts = (match.group(2) or '').split('-') #split by minus signs
                base_ott = excluded_otts.pop(0) or match.group(1) #first number after '=' is the tree to extract.
                logging.debug(f'Base ott: {base_ott}, Excluded otts: {excluded_otts}')
                all_included_otts.add(base_ott)
                all_excluded_otts.update(excluded_otts)

def extract_trees_from_open_tree_file(open_tree_file, output_dir, all_included_otts, all_excluded_otts):
    # Read the contents of the open tree file into a string
    with open(open_tree_file, 'r', encoding="utf8") as f:
        fulltree = f.read()

    trees = extract_trees.extract(fulltree, all_included_otts, excluded_taxa=all_excluded_otts, separate_trees=True)

    logging.info(f"Extracted {len(trees)} trees from Open Tree file")

    # Save each tree to a file named after the taxon
    for ott, tree in trees.items():
        with open(os.path.join(output_dir, ott + ".phy"), "w", encoding="utf8") as f:
            f.write(tree)
            f.write(";\n")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Create subtrees from the Open Tree of Life, on the basis of ott numbers in a set of newick files.')
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

    start = time.time()
    if not os.path.isfile(args.open_tree_file):
        logging.warning("Could not find the OpenTree file {}".format(args.open_tree_file))

    included_otts = set()
    excluded_otts = set()

    for file in args.parse_files:
        logging.info(f"== Processing One Zoom file {file}")
        add_inclusions_and_exclusions_from_one_zoom_file(file, included_otts, excluded_otts)
    
    extract_trees_from_open_tree_file(args.open_tree_file, args.output_dir, included_otts, excluded_otts)
        
    logging.debug("Time taken: {} seconds".format(time.time() - start))