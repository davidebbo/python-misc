import glob
import io
import os
import re
import sys

import extract_trees

'''
foobar_ott123@ means create a node named foobar with ott 123, consisting of all descendants of 123 in the opentree.
foobar_ott123~456-789-111@ means create a node named foobar with ott 123, using ott456 minus the descendant subtrees 789 and 111
The tilde sign can be read an a equals (Dendropy doesn't like equals signs in taxon names)
foobar_ott123~-789-111@ is shorthand for foobar_ott123~123-789-111@
foobar_ott~456-789-111@ means create a node named foobar without any OTT number, using ott456 minus the descendant subtrees 789 and 111
'''

ottRE = re.compile(r"(\w+)_ott([-~\d]+)\@")
id_pattern = re.compile(r"(\d*)~?([-\d]*)$")

all_otts = set()
all_del_otts = set()


for file in glob.glob("data/OZTreeBuild/AllLife/BespokeTree/include_OTT3.3draft1/*.PHY"):
    print(f'=== {file} ===')
    with open(file) as f:
        tree = f.read()
        for name, ottIDs in ottRE.findall(tree):
            print(f'{name} {ottIDs}')
            match = id_pattern.match(ottIDs)
            if match:
                subfile_name = match.group(1) or name
                del_otts = (match.group(2) or '').split('-') #split by minus signs
                base_ott = del_otts.pop(0) or match.group(1) #first number after '=' is the tree to extract.
                all_otts.add(base_ott)
                all_del_otts.update(del_otts)
                print(f'    {base_ott} {del_otts}')



# Read all the files in the directory path
# files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


# Read the contents of the file into a string
with open('data/OpenTree/draftversion13_4.tre') as f:
    fulltree = f.read()



def expand_newick(path, output_stream):
    with open(path) as f:
        tree = f.read()

        index = 0
        for name, ottIDs in ottRE.findall(tree):
            match = id_pattern.match(ottIDs)
            if match:
                del_otts = (match.group(2) or '').split('-') #split by minus signs
                base_ott = del_otts.pop(0) or match.group(1) #first number after '=' is the tree to extract.
                output_stream.write(tree[index:match.start()])
                output_stream.write(trees_by_ott[base_ott])
                index = match.end()
        
        output_stream.write(tree[index:])



# foo.Bar()



# taxon_regex = re.compile('([\w-]*)_ott(\d+)')
# ott_lookup = { match.group(1): match.group(2) for match in taxon_regex.finditer(fulltree)}
# taxon_lookup = { match.group(2): match.group(1) for match in taxon_regex.finditer(fulltree)}


# # get the list of file names with extension .phy in the directory without the extension
# path = "data/OZTreeBuild/AllLife/OpenTreeParts/OpenTree_all"
# files = [os.path.splitext(f)[0] for f in os.listdir(path) if f.endswith('.phy')]
# # files = glob.glob("data/OZTreeBuild/AllLife/OpenTreeParts/OpenTree_all/*.phy")

# # Turn the list of file names into a list of numbers if they are numbers
# taxa = {f for f in files if f.isdigit()}

# # Turn the list of numbers into a set of taxon names if they are in the lookup
# # taxa = {taxon_lookup[str(f)] for f in ott_numbers if str(f) in taxon_lookup}

# # taxa.remove('Rhiniformes_group')
# # taxa.remove('Deep_Sea_Hydrothermal_Vent_Gp_6_DHVEG-6')


# Exception: Could not find the following taxa: 747323, 5248234, 5205266, 356644, 4795972, 523271

# Additional trees: 415970 4795972 494997 5205266 5246141 971869 973629
all_otts.remove('4795972')
all_otts.remove('5205266')

# WARNING:root:File OpenTreeParts/OpenTree_all/523271.nwk does not exist, skipping
# WARNING:root:File OpenTreeParts/OpenTree_all/747323.nwk does not exist, skipping
# WARNING:  Could not find subtree _ott296715 within tree in OpenTreeParts/OpenTree_all/921404.nwk
# WARNING:root:File OpenTreeParts/OpenTree_all/7001160.nwk does not exist, skipping
# WARNING:root:File OpenTreeParts/OpenTree_all/5877728.nwk does not exist, skipping

all_otts.remove('523271')
all_otts.remove('747323')
all_otts.remove('356644')
all_otts.remove('5248234')



trees = extract_trees.extract(fulltree, all_otts, excluded_taxa=all_del_otts, separate_trees=True)

trees_by_ott = {ott: tree for ott, tree in trees.items()}

print(f"Found {len(trees)} trees")

# expand_newick('data/OZTreeBuild/AllLife/BespokeTree/include_files/Base.PHY', sys.stdout)


f = io.StringIO()
f.write('foo')
expand_newick('data/OZTreeBuild/AllLife/BespokeTree/include_files/Base.PHY', sys.stdout)

# # Save each tree to a file named after the taxon
# for ott, tree in trees.items():
#     # Save the tree to a file named after the taxon
#     with open(f"data/OZTreeBuild/AllLife/OpenTreeParts/OpenTree_all/tmp/{ott}.phy", "w") as f:
#         f.write(tree)
#         f.write(";\n")


# Rhiniformes_group, Deep_Sea_Hydrothermal_Vent_Gp_6_DHVEG-6

# whole_token_regex = re.compile('[\w\':\.\-/#\*]+')
        # elif newick_tree[index] != ')':
        #     raise Exception(f'Found invalid character \'{newick_tree[index]}\' at index {index} ({newick_tree[index-50:index+50]})')
