#!/usr/bin/env python3

import unittest
from extract_trees import extract

test_tree = "(A,(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789,((CAA,CAB),CB)C,D)Root;"

'''
Unit test for extract_minimal_tree.extract
'''
class TestExtract(unittest.TestCase):

    def test_missing_taxa(self):
        tree = extract(test_tree, {"X", "BBC", "Y"})

        self.assertEqual(tree, 'BBC_ott456:78.9')

    def test_one_taxon_expanded(self):
        tree = extract(test_tree, {"B"}, expand_taxa=True)

        self.assertEqual(tree, '(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789')

    def test_two_taxa(self):
        tree = extract(test_tree, {"BA", "BBBA"})

        self.assertEqual(tree, '(BA,BBBA)B_ott789')

    def test_two_taxa_no_root_name(self):
        tree = extract(test_tree, {"CAA", "CAB"})

        self.assertEqual(tree, '(CAA,CAB)')

    def test_two_taxa_expanded(self):
        tree = extract(test_tree, {"BBC", "C"}, expand_taxa=True)

        self.assertEqual(tree, '((BBCA:12.34,BBCB)BBC_ott456:78.9,((CAA,CAB),CB)C)Root')

    def test_three_taxa(self):
        tree = extract(test_tree, {"BA", "C", "BBC"})

        self.assertEqual(tree, '((BA,BBC_ott456:78.9)B_ott789,C)Root')

    def test_three_taxa_polytomy(self):
        tree = extract(test_tree, {"BBAD", "BBAA", "BBAC"})

        self.assertEqual(tree, '(BBAA_ott123,BBAC,BBAD)BAA')

    def test_two_nested_taxa(self):
        tree = extract(test_tree, {"B", "BBC"})

        self.assertEqual(tree, '(BBC_ott456:78.9)B_ott789')

    def test_two_nested_taxa_with_expansion(self):
        tree = extract(test_tree, {"BBC", "BB"}, expand_taxa=True)

        self.assertEqual(tree, '((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB')

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

    def test_excluded_taxa(self):
        tree = extract(test_tree, {"BB"}, excluded_taxa={"BBC","BBAB","BBAD"}, expand_taxa=True)

        self.assertEqual(tree, '((BBAA_ott123,BBAC)BAA,(BBBA)BBB)BB')

    def test_excluded_taxa_start_at_root(self):
        tree = extract(test_tree, {"Root"}, excluded_taxa={"B","C"}, expand_taxa=True)

        self.assertEqual(tree, '(A,D)Root')

    def test_excluded_taxa_two_trees(self):
        tree = extract(test_tree, {"C", "B"}, excluded_taxa={"CB", "BB"}, expand_taxa=True)

        self.assertEqual(tree, '((BA)B_ott789,((CAA,CAB))C)Root')

    def test_one_separate_tree(self):
        tree = extract(test_tree, {"C"}, separate_trees=True)

        self.assertEqual(tree, {'C': '((CAA,CAB),CB)C'})

    def test_two_separate_trees(self):
        tree = extract(test_tree, {"C", "BAA"}, separate_trees=True)

        self.assertEqual(tree, {'BAA': '(BBAA_ott123,BBAB,BBAC,BBAD)BAA', 'C': '((CAA,CAB),CB)C'})

    def test_two_separate_trees_with_exclusions(self):
        tree = extract(test_tree, {"C", "BB"}, excluded_taxa={"BAA", "CAA"}, separate_trees=True)

        self.assertEqual(tree, {'BB': '((BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB', 'C': '((CAB),CB)C'})

    def test_quoted_taxa(self):
        # Real example found in Open Tree: (...)'Pristiformes/Rhiniformes_group_ott356644'

        tree_string = "(A,(B,'C':123)'foo/bar_ott356644',D)E;"

        tree = extract(tree_string, {"356644"}, expand_taxa=True)
        self.assertEqual(tree, "(B,'C':123)'foo/bar_ott356644'")

        tree = extract(tree_string, {"foo/bar"}, expand_taxa=True)
        self.assertEqual(tree, "(B,'C':123)'foo/bar_ott356644'")


unittest.main()
