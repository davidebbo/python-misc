import argparse
import logging
import sys
from dendropy import Tree

def dend(treefile):
    logging.info(f"Reading tree from {treefile}")
    tree = Tree.get(path=treefile, schema='newick', preserve_underscores=True,suppress_leaf_node_taxa=True, suppress_internal_node_taxa=True)

    logging.info("Iterating over nodes")
    count = 0
    for node in tree.postorder_node_iter():
        count += 1
        print(node.label)
        if count == 20:
            break

    logging.info(f"Tree has {count} nodes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verbosity', '-v', action='count', default=0, help='verbosity level: output extra non-essential info')
    parser.add_argument('treefile', help='The base tree file in newick form')
    # parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    if args.verbosity==0:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    elif args.verbosity==1:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    elif args.verbosity==2:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    dend(args.treefile)


