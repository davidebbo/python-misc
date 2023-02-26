#!/usr/bin/env python3

import unittest
from extract_trees import extract

test_tree = "(A,(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789,((CAA,CAB):5.25,CB)C,D)Root;"

'''
Unit test for extract_trees.extract
'''
class test_extract(unittest.TestCase):

    def test_some_missing_taxa(self):
        tree = extract(test_tree, {"X", "BBC", "Y"})

        self.assertEqual(tree, {'456': '(BBCA:12.34,BBCB)BBC_ott456:78.9'})

    def test_all_missing_taxa(self):
        tree = extract(test_tree, {"X", "6789"})

        self.assertEqual(tree, {})

    def test_one_taxon(self):
        tree = extract(test_tree, {"B"})

        self.assertEqual(tree, {'789': '(BA,((BBAA_ott123,BBAB,BBAC,BBAD)BAA,(BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB)B_ott789'})

    def test_one_taxon_with_exclusion(self):
        tree = extract(test_tree, {"C"}, excluded_taxa={"CAA"})

        self.assertEqual(tree, {'C': '((CAB):5.25,CB)C'})

    def test_two_taxa(self):
        tree = extract(test_tree, {"BBC", "C"})

        self.assertEqual(tree, {'456': '(BBCA:12.34,BBCB)BBC_ott456:78.9', 'C': '((CAA,CAB):5.25,CB)C'})

    def test_two_nested_taxa(self):
        tree = extract(test_tree, {"123", "BAA"})

        self.assertEqual(tree, {'123': 'BBAA_ott123', 'BAA': '(BBAA_ott123,BBAB,BBAC,BBAD)BAA'})

    def test_two_taxa_with_exclusions(self):
        tree = extract(test_tree, {"C", "BB"}, excluded_taxa={"BAA", "CAA"})

        self.assertEqual(tree, {'BB': '((BBBA)BBB,(BBCA:12.34,BBCB)BBC_ott456:78.9)BB', 'C': '((CAB):5.25,CB)C'})

    def test_quoted_taxa(self):
        # Real example found in Open Tree: (...)'Pristiformes/Rhiniformes_group_ott356644'

        tree_string = "(A,(B,'C':123)'foo/bar_ott356644','abc$def':123.456)E;"

        tree = extract(tree_string, {"356644"})
        self.assertEqual(tree, {'356644': "(B,'C':123)'foo/bar_ott356644'"})

        tree = extract(tree_string, {"foo/bar"})
        self.assertEqual(tree, {'356644': "(B,'C':123)'foo/bar_ott356644'"})

        tree = extract(tree_string, {"abc$def"})
        self.assertEqual(tree, {'abc$def': "'abc$def':123.456"})


    def test_syntax_error_cases(self):
        def verify_exception(tree_string, taxa):
            exception = False
            try:
                extract(tree_string, taxa)
            except SyntaxError:
                exception = True

            self.assertTrue(exception)

        # Comma without a following taxon
        verify_exception("(A,,B);", {"B"})
        verify_exception("(A,B,);", {"C"})

        # Too many closing parens
        verify_exception("(A,B))(C,D);", {"C"})
        verify_exception(")))", {"C"})

        # Missing branch length
        verify_exception("(Blah,Foo:);", {"C"})

unittest.main()
