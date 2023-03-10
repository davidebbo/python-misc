import argparse
import sys
from newick_parser import parse_tree


def analyze_tree(tree):
    node_count = 0

    leaf_nodes = 0
    nodes_with_edge_length = 0
    nodes_with_ott = 0

    sub_species = 0
    species = 0
    higher_level_taxa = 0

    total_leaf_node_depth = 0

    for node in parse_tree(tree):
        node_count += 1

        if node['is_leaf']:
            leaf_nodes += 1
            total_leaf_node_depth += node['depth']

        if node['edge_length']:
            nodes_with_edge_length += 1

        if node['ott']:
            nodes_with_ott += 1

        taxon = node['taxon'].split('.')[0]
        if taxon.count('_') > 2:
            # Figure out what to do with these
            pass
        elif taxon.count('_') == 2:
            sub_species += 1
        elif taxon.count('_') == 1:
            species += 1
        else:
            higher_level_taxa += 1


    print(f"Node count: {node_count}")
    print(f"Leaf nodes: {leaf_nodes}")
    print(f"Nodes with edge length: {nodes_with_edge_length}, Nodes without edge length: {node_count - nodes_with_edge_length}")
    print(f"Nodes with OTT: {nodes_with_ott}, Nodes without OTT: {node_count - nodes_with_ott}")
    print(f"Sub-species: {sub_species}, Species: {species}, Higher level taxa: {higher_level_taxa}")
    print(f"Average leaf node depth: {total_leaf_node_depth / leaf_nodes:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('treefile', type=argparse.FileType(
        'r'), nargs='?', default=sys.stdin, help='The tree file in newick format')
    args = parser.parse_args()

    tree = args.treefile.read()
    analyze_tree(tree)
