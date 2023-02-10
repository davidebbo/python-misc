#!/usr/bin/env python3

import unittest
from extract_minimal_tree import extract

test_tree = "(A,(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B,((CAA,CAB),CB)C,D)Root;"

'''
Unit test for extract_minimal_tree.extract
'''
class TestExtract(unittest.TestCase):

    def test_missing_taxa(self):
        taxa = {"X", "BBC", "Y"}
        tree = extract(test_tree, taxa, expand_taxa=False)

        self.assertEqual(tree, None)

        self.assertEqual(
            taxa,
            {"X", "Y"}
        )

    def test_one_taxon_expanded(self):
        taxa = {"B"}
        tree = extract(test_tree, taxa, expand_taxa=True)

        self.assertFalse(taxa)
        self.assertEqual(tree, '(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B')

    def test_two_taxa(self):
        taxa = {"BA", "BBBA"}
        tree = extract(test_tree, taxa, expand_taxa=False)

        self.assertEqual(tree, '(BA,BBBA)B')

    def test_two_taxa_no_root_name(self):
        taxa = {"CAA", "CAB"}
        tree = extract(test_tree, taxa, expand_taxa=False)

        self.assertEqual(tree, '(CAA,CAB)')

    def test_two_taxa_expanded(self):
        taxa = {"BBC", "C"}
        tree = extract(test_tree, taxa, expand_taxa=True)

        self.assertEqual(tree, '((BBCA:12.34,BBCB)BBC_ott456:78.9,((CAA,CAB),CB)C)Root')

    def test_three_taxa(self):
        taxa = {"BA", "C", "BBC"}
        tree = extract(test_tree, taxa)

        self.assertEqual(tree, '((BA,BBC_ott456:78.9)B,C)Root')

    def test_three_taxa_polytomy(self):
        taxa = {"BBAD", "BBAA", "BBAC"}
        tree = extract(test_tree, taxa)

        self.assertEqual(tree, '(BBAA_ott123,BBAC,BBAD)BAA')

    def test_two_nested_taxa(self):
        taxa = {"B", "BBC"}
        tree = extract(test_tree, taxa, expand_taxa=False)

        self.assertEqual(tree, '(BBC_ott456:78.9)B')

    def test_two_nested_taxa_with_expansion(self):
        taxa = {"BBC", "BB"}
        tree = extract(test_tree, taxa, expand_taxa=True)

        self.assertEqual(tree, '((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB')

    def test_three_nested_taxa(self):
        taxa = {"BB", "BBC", "B"}
        tree = extract(test_tree, taxa, expand_taxa=False)

        self.assertEqual(tree, '((BBC_ott456:78.9)BB)B')

    def test_nested_with_implied_taxon(self):
        taxa = {"BBAB", "B", "BBAD"}
        tree = extract(test_tree, taxa, expand_taxa=False)

        self.assertEqual(tree, '((BBAB,BBAD)BAA)B')

    def test_mixed_scenarios(self):
        taxa = {"BBB", "B", "BBCA", "BBCB"}
        tree = extract(test_tree, taxa, expand_taxa=False)

        self.assertEqual(tree, '((BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B')


unittest.main()
