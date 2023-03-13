#!/usr/bin/env python3

import unittest
from newick.extract_trees_impl import extract_trees

test_tree = "(A,(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789,((CAA,CAB):5.25,CB)C,D)Root;"

'''
Unit test for extract_trees.extract
'''
class test_extract(unittest.TestCase):
    def test_some_missing_taxa(self):
        tree = extract_trees(test_tree, {"X", "BBC", "Y"})

        self.assertEqual(tree, {'456': '(BBCA:12.34,BBCB)BBC_ott456:78.9'})

    def test_all_missing_taxa(self):
        tree = extract_trees(test_tree, {"X", "6789"})

        self.assertEqual(tree, {})

    def test_one_taxon(self):
        tree = extract_trees(test_tree, {"B"})

        self.assertEqual(tree, {'789': '(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789'})

    def test_one_taxon_with_exclusion(self):
        tree = extract_trees(test_tree, {"C"}, excluded_taxa={"CAA"})

        self.assertEqual(tree, {'C': '((CAB):5.25,CB)C'})

    def test_two_taxa(self):
        tree = extract_trees(test_tree, {"BBC", "C"})

        self.assertEqual(tree, {'456': '(BBCA:12.34,BBCB)BBC_ott456:78.9', 'C': '((CAA,CAB):5.25,CB)C'})

    def test_two_nested_taxa(self):
        tree = extract_trees(test_tree, {"123", "BAA"})

        self.assertEqual(tree, {'123': 'BBAA_ott123', 'BAA': '(BBAA_ott123,BBAB,BBAC,BBAD)BAA'})

    def test_two_taxa_with_exclusions(self):
        tree = extract_trees(test_tree, {"C", "BB"}, excluded_taxa={"BAA", "CAA"})

        self.assertEqual(tree, {'BB': '((BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB', 'C': '((CAB):5.25,CB)C'})

    def test_nested_exclusions(self):
        tree = extract_trees("((A,B)C,D)E;", {"E"}, excluded_taxa={"B", "C"})

        self.assertEqual(tree, {'E': '(D)E'})
