# -*- coding: utf-8 -*- 
# Recorre el corpus original y va copiando los archivos de Genia Event (si existen) al directorio event
# Recibe como parámetros el directorio de trabajo
# Ejemplo python copy_genia_event_files.py $BIOSCOPE

from sys import *
import os.path
import pln_inco.bioscope

working_dir=argv[1]

for bioscope_xml_file in ['abstracts_train.xml', 'abstracts_test.xml']:
	bcp=pln_inco.bioscope.BioscopeCorpusProcessor(working_dir, bioscope_xml_file)
	for docset in bcp.original_bioscope_corpus.getchildren(): # Recorro los document set (en este caso es uno solo)
		for doc in docset.getchildren(): # Recorro los documentos	
			# Identificador del documento
			docId=doc.getchildren()[0].text 
			print >> stderr, "Proceso archivo ",docId
	
			# En vez de copiarlo, lo abro y lo grabo.
			# Esto me permite ponerle el css en la copia
			try:
				source=open(os.path.join(bcp.genia_event_corpus_dir,docId+'.xml'),'r')
				dest=open(os.path.join(bcp.event_dir,'a'+docId+'.event.xml'),'w+')
				lineas=source.readlines()
				lineas.insert(1,'<?xml-stylesheet href="genia_event.css" type="text/css"?>')
				dest.writelines(lineas)
				source.close()
				dest.close()
			except IOError:
				print >>stderr, 'No existe el archivo '+ docId+'.xml'
