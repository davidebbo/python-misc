#!/usr/bin/env python3

import unittest
from extract_minimal_tree import extract

Hominoidea = "(((Pongo_abelii_ott770295:1.295194,Pongo_pygmaeus_ott770302:1.295194)Pongo_ott417949:12.704806,(((Pan_troglodytes_ott417950:1.596326,Pan_paniscus_ott158484:1.596326)Pan_ott417957:4.403674,Homo_sapiens_ott770315:6.0)ChimpHumanClade_:2.0,(Gorilla_beringei_ott351685:1.776755,Gorilla_gorilla_ott417965:1.776755)Gorilla_ott417969:6.223245)Homininae_ott312031:6.0)Hominidae_ott770311:4.0,((Hylobates_pileatus_ott995054:1.5,(((Hylobates_klossii_ott995047:0.8,Hylobates_moloch_ott732213:0.8):0.2,((Hylobates_agilis_ott166550:0.4,Hylobates_albibarbis_ott96942:0.4):0.45,Hylobates_muelleri_ott995050:0.85):0.15):0.15,Hylobates_lar_ott995038:1.15):0.35)Hylobates_ott166552:3.9,(((((Nomascus_leucogenys_ott1029454:0.2,Nomascus_siki_ott995043:0.2):0.5,(Nomascus_gabriellae_ott847446:0.2,Nomascus_annamensis_ott5852672:0.2):0.5):0.3,Nomascus_concolor_ott180370:1.0):1.1,(Nomascus_nasutus_ott440190:1.5,Nomascus_hainanus_ott492226:1.5):0.6)Nomascus_ott712901:2.7,((Hoolock_hoolock_ott1029474:1.4,Hoolock_leuconedys_ott574262:1.4)Hoolock_ott712902:2.8,Symphalangus_syndactylus_ott417961:4.2):0.6):0.6)Hylobatidae_ott166544:12.6)Hominoidea_ott386191:7.0;"

'''
Unit test for extract_minimal_tree.extract
'''
class TestExtract(unittest.TestCase):

    def test_missing_taxon(self):
        taxa = {"Canis", "Pan", "Tupaia"}
        tree = extract(Hominoidea, taxa, expand_taxa=False)

        self.assertEqual(
            taxa,
            {"Canis", "Tupaia"}
        )

unittest.main()
