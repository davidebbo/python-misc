#!/usr/bin/env python3

import unittest
from one_zoom.extract_minimal_tree import extract

test_tree = "(A,(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789,((CAA,CAB):5.25,CB)C,D)Root;"

'''
Unit test for extract_minimal_tree.extract
'''
class test_extract(unittest.TestCase):
    def test_some_missing_taxa(self):
        tree = extract(test_tree, {"X", "BBC", "Y"})

        self.assertEqual(tree, 'BBC_ott456:78.9')

    def test_all_missing_taxa(self):
        tree = extract(test_tree, {"X", "6789"})

        self.assertEqual(tree, None)

    def test_two_taxa(self):
        tree = extract(test_tree, {"BA", "BBBA"})

        self.assertEqual(tree, '(BA,BBBA)B_ott789')

    def test_two_taxa_no_root_name(self):
        tree = extract(test_tree, {"CAA", "CAB"})

        self.assertEqual(tree, '(CAA,CAB):5.25')

    def test_three_taxa(self):
        tree = extract(test_tree, {"BA", "C", "BBC"})

        self.assertEqual(tree, '((BA,BBC_ott456:78.9)B_ott789,C)Root')

    def test_three_taxa_polytomy(self):
        tree = extract(test_tree, {"BBAD", "BBAA", "BBAC"})

        self.assertEqual(tree, '(BBAA_ott123,BBAC,BBAD)BAA')

    def test_two_nested_taxa(self):
        tree = extract(test_tree, {"B", "BBC"})

        self.assertEqual(tree, '(BBC_ott456:78.9)B_ott789')

    def test_three_nested_taxa(self):
        tree = extract(test_tree, {"BB", "BBC", "B"})

        self.assertEqual(tree, '((BBC_ott456:78.9)BB)B_ott789')

    def test_nested_with_implied_taxon(self):
        tree = extract(test_tree, {"BBAB", "B", "BBAD"})

        self.assertEqual(tree, '((BBAB,BBAD)BAA)B_ott789')

    def test_mixed_scenarios(self):
        tree = extract(test_tree, {"BBB", "789", "BBCA", "BBCB"})

        self.assertEqual(tree, '((BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789')

    def test_find_by_ott(self):
        tree = extract(test_tree, {"123", "789", "456"})

        self.assertEqual(tree, '((BBAA_ott123,BBC_ott456:78.9)BB)B_ott789')

