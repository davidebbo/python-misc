#!/usr/bin/env python3
'''
Enumerate all nodes in a Newick tree
'''

import re
from typing import Set

non_name_regex = re.compile(r'[,;:\(\)]')

def enumerate_nodes(newick_tree):
    index = 0
    index_stack = []

    # Helper function to raise a syntax error with extra context
    def raise_syntax_error(message):
        raise SyntaxError(f'Syntax error: {message}. Index={index}, Text="{newick_tree[index-20:index+20]}"')

    while newick_tree[index] != ';':

        if newick_tree[index] == '(':
            index_stack.append(index)
            index += 1
            continue

        closed_brace = newick_tree[index] == ')'
        if closed_brace:
            # A closed brace cannot follow a comma
            if newick_tree[index-1] == ',':
                raise_syntax_error(f"unexpected comma")

            index += 1

            # Set the start index to the beginning of the node (where the open parenthesis is)
            try:
                node_start_index = index_stack.pop()
            except IndexError:
                raise_syntax_error(f"unmatched closed brace")
        else:
            node_start_index = index

        found_target_taxon = False
        taxon = ott_id = None

        full_name_start_index = index
        if newick_tree[index] == "'":
            # This is a quoted name, so we need to find the end of the name
            end_quote_index = newick_tree.index("'", index+1)

            taxon = newick_tree[index+1:end_quote_index]
            index = end_quote_index + 1
        else:
            # This may be an unquoted name, so we need to find the end
            match = non_name_regex.search(newick_tree, index)
            if match:
                index = match.start()
                taxon = newick_tree[full_name_start_index:index]

        # After the taxon, there may be an edge length
        edge_length = 0.0
        if newick_tree[index] == ':':
            index += 1
            match = non_name_regex.search(newick_tree, index)
            if match:
                # Convert to a float
                try:
                    edge_length = float(newick_tree[index:match.start()])
                except ValueError:
                    raise_syntax_error(f"{edge_length} is not a valid edge length")
                index = match.start()

        # There should be a taxon, except after a closed brace where it's optional            
        if not (taxon or edge_length) and not closed_brace:
            raise_syntax_error(f"expected a taxon or an edge length (e.g. 'foo', 'foo:1.0', or ':1.0')")

        if taxon:
            # Check if the taxon has an ott id, and if so, parse it out
            if '_ott' in taxon:
                ott_index = taxon.index('_ott')
                ott_id = taxon[ott_index+4:]
                taxon = taxon[:ott_index]

        yield { 'taxon': taxon, 'ott_id': ott_id, 'edge_length': edge_length, 'start': node_start_index, 'end': index, 'depth': len(index_stack) }

        if newick_tree[index] == ',':
            index += 1
