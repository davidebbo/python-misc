#!/usr/bin/env python3

import unittest
from extract_minimal_tree import extract

Hominoidea = """(((Pongo_abelii_ott770295,Pongo_pygmaeus_ott770302:1.295194)Pongo:1.234,
    (((Pan_troglodytes_ott417950,Pan_paniscus)Pan_ott417957,Homo_sapiens_ott770315)ChimpHumanClade,
    (Gorilla_beringei_ott351685,Gorilla_gorilla_ott417965:2.345)Gorilla_ott417969)Homininae_ott312031)Hominidae_ott770311)Hominoidea_ott386191;"""

# remove all spaces and newlines from the tree
Hominoidea = Hominoidea.replace(" ", "").replace("\n", "")

'''
Unit test for extract_minimal_tree.extract
'''
class TestExtract(unittest.TestCase):

    def test_missing_taxa(self):
        taxa = {"Canis", "Pan", "Tupaia"}
        tree = extract(Hominoidea, taxa, expand_taxa=False)

        self.assertEqual(tree, None)

        self.assertEqual(
            taxa,
            {"Canis", "Tupaia"}
        )

    def test_one_taxon_expanded(self):
        taxa = {"Pan"}
        tree = extract(Hominoidea, taxa, expand_taxa=True)

        self.assertFalse(taxa)
        self.assertEqual(tree, '(Pan_troglodytes_ott417950,Pan_paniscus)Pan_ott417957')

    def test_two_taxa(self):
        taxa = {"Pan", "Pongo"}
        tree = extract(Hominoidea, taxa, expand_taxa=False)

        self.assertEqual(tree, '(Pongo:1.234,Pan_ott417957)Hominidae_ott770311')

    def test_two_taxa_expanded(self):
        taxa = {"Pan_troglodytes", "Pongo"}
        tree = extract(Hominoidea, taxa, expand_taxa=True)

        self.assertEqual(tree, '((Pongo_abelii_ott770295,Pongo_pygmaeus_ott770302:1.295194)Pongo:1.234,Pan_troglodytes_ott417950)Hominidae_ott770311')

    def test_three_taxa(self):
        taxa = {"Homo_sapiens", "Pan", "Pongo"}
        tree = extract(Hominoidea, taxa)

        self.assertEqual(tree, '(Pongo:1.234,(Pan_ott417957,Homo_sapiens_ott770315)ChimpHumanClade)Hominidae_ott770311')

    def test_two_nested_taxa(self):
        taxa = {"Pan", "Hominidae"}
        tree = extract(Hominoidea, taxa, expand_taxa=False)

        self.assertEqual(tree, '(Pan_ott417957)Hominidae_ott770311')

    def test_two_nested_taxa_with_expansion(self):
        taxa = {"Pan", "ChimpHumanClade"}
        tree = extract(Hominoidea, taxa, expand_taxa=True)

        self.assertEqual(tree, '((Pan_troglodytes_ott417950,Pan_paniscus)Pan_ott417957,Homo_sapiens_ott770315)ChimpHumanClade')

    def test_three_nested_taxa(self):
        taxa = {"Pan", "Hominidae", "Pan_paniscus"}
        tree = extract(Hominoidea, taxa, expand_taxa=False)

        self.assertEqual(tree, '((Pan_paniscus)Pan_ott417957)Hominidae_ott770311')

    def test_nested_with_implied_taxon(self):
        taxa = {"Hominidae", "Pan_paniscus", "Pan_troglodytes"}
        tree = extract(Hominoidea, taxa, expand_taxa=False)

        self.assertEqual(tree, '((Pan_troglodytes_ott417950,Pan_paniscus)Pan_ott417957)Hominidae_ott770311')

    def test_mixed_scenarios(self):
        taxa = {"Pongo", "Hominidae", "Pan_paniscus", "Gorilla_gorilla"}
        tree = extract(Hominoidea, taxa, expand_taxa=False)

        self.assertEqual(tree, '(Pongo:1.234,(Pan_paniscus,Gorilla_gorilla_ott417965:2.345)Homininae_ott312031)Hominidae_ott770311')


unittest.main()
