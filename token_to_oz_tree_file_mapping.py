token_to_file_map = {
    # Base tree for chordates, assuming initial divergence at 550Mya.
    # Note: BASE is not included here as it's passed explicitly as the starting tree


    'AMORPHEA': ['Amorphea.PHY', 50],
    'CRUMS': ['CRuMs.PHY'],
    'DIAPHORETICKES': ['Diaphoretickes.PHY', 100],
    'METAZOA': ['Animals.PHY', 150],
    'PORIFERA': ['PoriferaOneZoom.phy', 50],
    'CTENOPHORA': ['CtenophoresPoder2001.PHY', 50],
    'AMBULACRARIA': ['Ambulacraria.PHY', 20, 'Ambulacraria'],
    #  DEEPFIN tree root (Shark + bony-fish) is at 462.4. Guess for Cyclostome divergence = 500Mya
    'CYCLOSTOMATA': ['Cyclostome_full_guess.PHY', 43],
    'LAMPREYS': ['Lampreys_Potter2015.phy', 332.0],
    'GNATHOSTOMATA': ['BonyFishOpenTree.PHY', 65],
    # for fewer species but with dates, try 
    # tree.substitute('GNATHOSTOMATA@', 'BespokeTree/include_files/Deepfin2.phy', 37.6)  # C20=430Ma

    'CHONDRICHTHYES': ['Chondrichthyes_Renz2013.phy', 40],
    'HOLOCEPHALI': ['Holocephali_Inoue2010.PHY', 250],
    'BATOIDEA': ['Batoids_Aschliman2012.PHY', 100],
    # sharks are problematic in OToL v3 & 4, hence lots of files included here
    'SELACHII': ['Naylor2012Selachimorpha.PHY', 75],
    'DALATIIDAE': ['Naylor2012Dalatiidae.PHY', 116.1],
    'SOMNIOSIDAEOXYNOTIDAE': ['Naylor2012Somniosidae_Oxynotidae.PHY', 110.51],
    'ETMOPTERIDAE': ['Naylor2012Etmopteridae.phy', 110.51],
    'SQUATINIDAE': ['Naylor2012Squatinidae.phy', 147.59],
    'PRISTIOPHORIDAE': ['Naylor2012Pristiophoridae.phy', 147.59],
    'SCYLIORHINIDAE3': ['Naylor2012Scyliorhinidae3.PHY', 170],
    'SCYLIORHINIDAE2': ['Naylor2012Scyliorhinidae2.PHY', 134.467193],
    'CARCHARHINICAE_MINUS': ['Naylor2012Carcharhinicae_minus.PHY', 134.467193, 'Most_Carcharhinicae_'],

    #  Choanoflagellates: http://www.pnas.org/content/105/43/16641.short 

    ##########  NB: to use the original deepfin tree, substitute these text strings back in instead ##########
    # 	tree.substitute('TETRAPODA@', '(Xenopus_tropicalis:335.4,(Monodelphis_domestica:129,(Mus_musculus:71.12,Homo_sapiens:71.12):57.88):206.4)Tetrapodomorpha:46.5');
    # 	tree.substitute('COELACANTHIFORMES@', 'Latimeria_chalumnae:409.4');
    # 	tree.substitute('DIPNOI@', '(Neoceratodus_forsteri:241.804369,(Protopterus_aethiopicus_annectens:103.2,Lepidosiren_paradoxa:103.2):138.604369)Dipnoi:140.095631');
    # 	tree.substitute('POLYPTERIFORMES@', '(Erpetoichthys_calabaricus:29.2,(Polypterus_senegalus:16.555114,Polypterus_ornatipinnis:16.555114):12.644886)Polypteriformes:353.4');
    # 	tree.substitute('ACIPENSERIFORMES@', '(Polyodon_spathula:138.9,(Acipenser_fulvescens:38.592824,(Scaphirhynchus_platorynchus:19.382705,Scaphirhynchus_albus:19.382705):19.210119):100.307176)Acipenseriformes:211.2');


    'COELACANTHIFORMES': ['CoelacanthSudarto2010.phy', 414],
    'DIPNOI': ['LungfishCriswell2011.phy', 138],
    'POLYPTERIFORMES': ['BicherSuzuki2010.phy',      353.4, 'Polypteriformes'],
    'ACIPENSERIFORMES': ['SturgeonKrieger2008.phy',   166.1, 'Acipenseriformes'],
    'HOLOSTEI': ['GarsDeepfin.phy', 54.6, 'Holostei'],

    ########## TETRAPODS  ###########
    #  C18 @ 415, ChangedOneZoom tetrapods root @ 340 Mya. Stem = 75Ma
    'TETRAPODA': ['Tetrapods_Zheng_base.PHY', 75],
    # $tree.substitute('AMPHIBIA@',     'BespokeTree/include_files/AmphibiansOneZoom.phy',                30.0);
    'AMPHIBIA': ['AmphibiansOpenTree.PHY',              30.0],
    'CROCODYLIA': ['Crocodylia_OneZoom.phy', 152.86],
    'TESTUDINES': ['Testudines_OneZoom.phy', 55.77],
    'NEOGNATHAE': ['Neognathae_minus_passerines_OneZoom.PHY', 15.69],
    'PALAEOGNATHAE': ['PalaeognathaeMitchell2014.PHY', 40.45],
    'TINAMIFORMES': ['Tinamous_OneZoom.phy', 6.85],
    'PASSERIFORMES': ['PasserinesOneZoom.phy',      8],
    'GALAPAGOS_FINCHES_AND_ALLIES_': ['GalapagosFinchesLamichhaney2015.phy',      3.6],

    # for original onezoom tree use 
    # tree.substitute('EUTHERIA@',          'BespokeTree/include_files/PlacentalsOneZoom.phy');
    'MAMMALIA': ['Mammal_base.phy',            140],
    'MARSUPIALIA': ['Marsupial_recalibrated.phy', 73],
    'EUTHERIA': ['PlacentalsPoulakakis2010.phy',  70],
    'BOREOEUTHERIA': ['BoreoeutheriaOneZoom_altered.phy', 5],
    'XENARTHRA': ['XenarthraOneZoom.phy', 17.8],
    'AFROTHERIA': ['AfrotheriaPoulakakis2010.phy', 4.9],


    ########## (to use original OneZoom data, try ###############
    ##########	tree.substitute('PRIMATES@', 'BespokeTree/include_files/PrimatesOneZoom.phy', 23.3); #######

    #  Onezoom colugo-primate @ 90 Mya, Springer primates root @ 66.7065Mya. Here stem = 90 - 66.7065 = 23.3My
    #  But ancestor's tale colugo-primate @ 70 Ma

    # tree.substitute('PRIMATES@',      'BespokeTree/include_files/PrimatesSpringer2012.phy',  2.2932);  # base = 66.7068 C9 @ 69
    'PRIMATES': ['PrimatesSpringer2012_AT.PHY', 5],
    'HYLOBATIDAE': ['GibbonsCarbone2014.phy', 12.6],
    'DERMOPTERA': ['DermopteraJanecka2008.phy', 55],

    # STURGEON_TREE from http://onlinelibrary.wiley.com/doi/10.1111/j.1439-0426.2008.01088.x/abstract - should contain approx 30 spp. Base is at 

    # Needed
    # Correct Rattite tree
    # SHARK_TREE??
    # AMPHIOXUS_TREE_~32SPP - 24 Branchiostoma species, 7 Asymmetron species, 1 Epigonichthys (http://eolspecies.lifedesks.org/pages/63233) see http://www.bioone.org/doi/abs/10.2108/zsj.21.203

    # Tunicate tree ~ 2,150 spp - see T. Stuck for phylogeny

    # for dating look at B. Misof, et al. 2014. Phylogenomics resolves the timing and pattern of insect evolution. Science 346 (6210): 763-767.
    'PROTOSTOMIA': ['Protostomes.PHY', 50],
    'HOLOMYCOTA': ['Holomycota.PHY', 300],
    'APHELIDA': ['Aphelida_rough.PHY', 10]
}
