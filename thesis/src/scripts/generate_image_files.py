# -*- coding: utf-8 -*- 
# Levanta el corpus de los archivos y genera las imagenes
# Recibe como parámetros el directorio de trabajo, el xml con el corpus,el prefijo de nombres de documentos a levantar y un indicador binario de si solo generar las oraciones que tienen hedge y/o negación
# Ejemplo python generate_image_files.py $BIOSCOPE a 1


import pln_inco.bioscope as bioscope
import os.path
import time
from sys import *
import pln_inco.graphviz
import codecs

working_dir=argv[1]
prefix=argv[2]
only_hedge_and_negation_sentences=argv[3]

for bioscope_xml_file in ['abstracts_train.xml', 'abstracts_test.xml']:
	print working_dir,bioscope_xml_file
	bcp=pln_inco.bioscope.BioscopeCorpusProcessor(working_dir, bioscope_xml_file)
	bc=bioscope.BioscopeCorpus(bcp,prefix)
	for (docId,d) in bc.documents.iteritems():
		print >> stderr, "Genero imágenes para el documento ",docId
		for (sentenceId,sentence) in d.sentences.iteritems():
			print "Oración:",sentenceId, sentence.data_loaded
			if sentence.data_loaded:
				print "Data loaded..."
				if sentence.has_hedging() or sentence.has_negation() or (only_hedge_and_negation_sentences=='0'):
					print >> stderr, "Genero la imagen de la oracion ",sentenceId
					dot_spec=sentence.get_dot()
					dotFileName=docId+'.'+sentenceId+'.dot'
					f=codecs.open(os.path.join(bcp.image_files_dir,dotFileName),"wb+",encoding='utf-8')
					f.write(dot_spec)
					f.close()
					salida_svg=pln_inco.graphviz.generate(dot_spec,'svg')
					svgFileName=docId+'.'+sentenceId+'.svg'
					f=open(os.path.join(bcp.image_files_dir,svgFileName),"wb+")
					f.write(salida_svg)
					f.close()

