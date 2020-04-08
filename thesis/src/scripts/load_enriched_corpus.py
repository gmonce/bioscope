# -*- coding: utf-8 -*- 
# Script que levanta a memoria el corpus
# python load_enriched_corpus.py $BIOSCOPE pattern

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import sqlite3

working_dir=sys.argv[1]
pattern=sys.argv[2]
xml_list=[('abstracts_train.xml','bioscope_train'),('abstracts_test.xml','bioscope_test')]
for (bioscope_xml_file,table_name) in xml_list:
	# Levanto el corpus correspondiente
	bcp=bioscope.util.BioscopeCorpusProcessor(working_dir, bioscope_xml_file)
	bc=bioscope.BioscopeCorpus(bcp,pattern)
