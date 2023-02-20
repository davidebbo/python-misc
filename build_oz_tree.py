#!/usr/bin/env python3
'''
Build the entire OneZoom tree from the saved parts
'''

import argparse
import logging
import os
import sys
from getOpenTreesFromOneZoom_fast import enumerate_one_zoom_tokens

token_to_file_map = {
    'AMORPHEA': ['Amorphea.PHY', 50],
    'CRUMS': ['CRuMs.PHY'],
    'DIAPHORETICKES': ['Diaphoretickes.PHY', 100],
    'METAZOA': ['Animals.PHY', 150],
    'PORIFERA': ['PoriferaOneZoom.phy', 50],
    'CTENOPHORA': ['CtenophoresPoder2001.PHY', 50],
    'AMBULACRARIA': ['Ambulacraria.PHY', 20, 'Ambulacraria'],
    'CYCLOSTOMATA': ['Cyclostome_full_guess.PHY', 43],
    'LAMPREYS': ['Lampreys_Potter2015.phy', 332.0],
    'GNATHOSTOMATA': ['BonyFishOpenTree.PHY', 65],
    'CHONDRICHTHYES': ['Chondrichthyes_Renz2013.phy', 40],
    'HOLOCEPHALI': ['Holocephali_Inoue2010.PHY', 250],
    'BATOIDEA': ['Batoids_Aschliman2012.PHY', 100],
    'SELACHII': ['Naylor2012Selachimorpha.PHY', 75],
    'DALATIIDAE': ['Naylor2012Dalatiidae.PHY', 116.1],
    'SOMNIOSIDAEOXYNOTIDAE': ['Naylor2012Somniosidae_Oxynotidae.PHY', 110.51],
    'ETMOPTERIDAE': ['Naylor2012Etmopteridae.phy', 110.51],
    'SQUATINIDAE': ['Naylor2012Squatinidae.phy', 147.59],
    'PRISTIOPHORIDAE': ['Naylor2012Pristiophoridae.phy', 147.59],
    'SCYLIORHINIDAE3': ['Naylor2012Scyliorhinidae3.PHY', 170],
    'SCYLIORHINIDAE2': ['Naylor2012Scyliorhinidae2.PHY', 134.467193],
    'CARCHARHINICAE_MINUS': ['Naylor2012Carcharhinicae_minus.PHY', 134.467193, 'Most_Carcharhinicae_'],
    'COELACANTHIFORMES': ['CoelacanthSudarto2010.phy', 414],
    'DIPNOI': ['LungfishCriswell2011.phy', 138],
    'POLYPTERIFORMES': ['BicherSuzuki2010.phy',      353.4, 'Polypteriformes'],
    'ACIPENSERIFORMES': ['SturgeonKrieger2008.phy',   166.1, 'Acipenseriformes'],
    'HOLOSTEI': ['GarsDeepfin.phy', 54.6, 'Holostei'],
    'TETRAPODA': ['Tetrapods_Zheng_base.PHY', 75],
    'AMPHIBIA': ['AmphibiansOpenTree.PHY',              30.0],
    'CROCODYLIA': ['Crocodylia_OneZoom.phy', 152.86],
    'TESTUDINES': ['Testudines_OneZoom.phy', 55.77],
    'NEOGNATHAE': ['Neognathae_minus_passerines_OneZoom.PHY', 15.69],
    'PALAEOGNATHAE': ['PalaeognathaeMitchell2014.PHY', 40.45],
    'TINAMIFORMES': ['Tinamous_OneZoom.phy', 6.85],
    'PASSERIFORMES': ['PasserinesOneZoom.phy',      8],
    'GALAPAGOS_FINCHES_AND_ALLIES_': ['GalapagosFinchesLamichhaney2015.phy',      3.6],
    'MAMMALIA': ['Mammal_base.phy',            140],
    'MARSUPIALIA': ['Marsupial_recalibrated.phy', 73],
    'EUTHERIA': ['PlacentalsPoulakakis2010.phy',  70],
    'BOREOEUTHERIA': ['BoreoeutheriaOneZoom_altered.phy', 5],
    'XENARTHRA': ['XenarthraOneZoom.phy', 17.8],
    'AFROTHERIA': ['AfrotheriaPoulakakis2010.phy', 4.9],
    'PRIMATES': ['PrimatesSpringer2012_AT.PHY', 5],
    'HYLOBATIDAE': ['GibbonsCarbone2014.phy', 12.6],
    'DERMOPTERA': ['DermopteraJanecka2008.phy', 55],
    'PROTOSTOMIA': ['Protostomes.PHY', 50],
    'HOLOMYCOTA': ['Holomycota.PHY', 300],
    'APHELIDA': ['Aphelida_rough.PHY', 10]
}


def trim_tree(tree):
    # Skip the comment block at the start of the file, if any
    if '[' in tree:
        tree = tree[tree.index(']')+1:]

    # Trim any whitespace
    tree = tree.strip()

    # Strip the trailing semicolon
    if tree[-1] == ';':
        tree = tree[:-1]

    return tree
    
def expand_newick(oz_file, sub_trees_folder, output_stream):
    logging.debug(f'Expanding {oz_file}')

    with open(oz_file, 'r', encoding="utf8") as stream:
        tree = stream.read()

    tree = trim_tree(tree)
    index = 0

    # Get the One Zoom include file folder from the path to the file
    oz_folder = os.path.dirname(oz_file)

    for result in enumerate_one_zoom_tokens(tree):
        output_stream.write(tree[index:result['start']])

        if 'base_ott' in result:
            ot_part_file = os.path.join(sub_trees_folder, f'{result["base_ott"]}.phy')

            # Check if the file exists
            if os.path.exists(ot_part_file):
                with open(ot_part_file, 'r', encoding="utf8") as stream:
                    ot_part_tree = stream.read()
                ot_part_tree = trim_tree(ot_part_tree)
                output_stream.write(ot_part_tree)
                logging.debug(f"Processed OT part file {ot_part_file}")
            else:
                logging.warning(f"Subtree file {ot_part_file} does not exist")
        else:
            oz_sub_file_name = token_to_file_map[result["full_name"]][0]
            oz_sub_file = os.path.join(oz_folder, oz_sub_file_name)

            if os.path.exists(oz_sub_file):
                expand_newick(oz_sub_file, sub_trees_folder, output_stream)
            else:
                logging.warning(f"OZ file {oz_sub_file} does not exist")

        index = result['end']
        
    output_stream.write(tree[index:])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verbosity', '-v', action='count', default=0, help='verbosity level: output extra non-essential info')
    parser.add_argument('treefile', help='The base tree file in newick form')
    parser.add_argument('subtreesfolder', help='The folder containing the subtree files')
    parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout, help='The output tree file')
    args = parser.parse_args()

    if args.verbosity==0:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    elif args.verbosity==1:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    elif args.verbosity==2:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    expand_newick(args.treefile, args.subtreesfolder, args.outfile)
    args.outfile.write(';')
