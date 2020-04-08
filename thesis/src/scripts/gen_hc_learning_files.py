# -*- coding: utf-8 -*- 
# Script que toma la base de datos y genera los archivos de entrenamiento/testeo sobre el corpus de entrenamiento 
# El parámetro total vale Y o N e indica si utilizar todo el corpus de entrenamiento y evaluar sobre el de evaluación
# o evaluar sobre el heldout
# por defecto vale N
# Uso: gen_hc_learning_files dbname training_file testing_file  config_filename total

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml



dbname=sys.argv[1]
training_file=sys.argv[2]
test_file=sys.argv[3]
config_filename=sys.argv[4]

if len(sys.argv)>5:
	total=sys.argv[5]
else:
	total='N'

script_name=os.path.join(sys.path[0],sys.argv[0])

# Leo la configuración del escenario 
config_file=open(config_filename)
conf=yaml.load(config_file)
xs=conf['xs']
y=conf['y'] 

if total=='Y':
	print script_name+": Generating full training file",training_file
	pln_inco.bioscope.util.gen_conll_file_hc(dbname,'BIOSCOPE_TRAIN','ALL',training_file,xs,y,predicted_y=False)
	print script_name+": Generating full test file",test_file
	pln_inco.bioscope.util.gen_conll_file_hc(dbname,'BIOSCOPE_TEST','ALL',test_file,xs,y,predicted_y=False)
	print script_name+":Done"
else:
	print script_name+": Generating 80% training file",training_file
	pln_inco.bioscope.util.gen_conll_file_hc(dbname,'BIOSCOPE_TRAIN','TRAIN',training_file,xs,y,predicted_y=False)
	print script_name+": Generating 20% test file",test_file
	pln_inco.bioscope.util.gen_conll_file_hc(dbname,'BIOSCOPE_TRAIN','TEST',test_file,xs,y,predicted_y=False)
	print script_name+":Done"
