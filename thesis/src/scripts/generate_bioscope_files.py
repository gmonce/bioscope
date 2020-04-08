# -*- coding: utf-8 -*- 
# Dado el corpus, genera archivos .bioscope con los textos de las oraciones, incluyendo los tags del corpus
# Recibe como parámetros el directorio de trabajo
# Ejemplo python generar_bioscope_files.py $BIOSCOPED

import sys
import os.path
import pln_inco.bioscope
import nltk.corpus
import xml
import string

working_dir=sys.argv[1]
	
xml_list=['abstracts_train.xml', 'abstracts_test.xml']

# Leo el corpus original

for bioscope_xml_file in xml_list:
	print >> sys.stderr, "Genero los archivos del corpus ",bioscope_xml_file
	bcp=pln_inco.bioscope.BioscopeCorpusProcessor(working_dir, bioscope_xml_file)
	for docset in bcp.original_bioscope_corpus.getchildren(): # Recorro los document set (en este caso es uno solo)
		sentences=[]
		for doc in docset.getchildren(): # Recorro los documentos	
			# Identificador del documento
			docId=doc.getchildren()[0].text 
			#print >> sys.stderr, "Proceso archivo ",docId
		
			for docpart in doc.getchildren():
				# Obtengo las oraciones en la parte
				sentences +=[(x,pln_inco.bioscope.bioscope_get_text(x)) for x in docpart.getchildren()]

			# Generación de las marcas de bioscope
			#print >> sys.stderr, "Genero tags de bioscope...",docId
			fileName=os.path.join(bcp.bioscope_files_dir,'a'+docId+'.bioscope')
			f=open(fileName,'w')
			f.write('<?xml version="1.0" encoding="utf-8"?>')
			f.write('<Annotation>')
			for (doc_sentence,sentence_text) in sentences:
				f.write(string.strip(xml.etree.ElementTree.tostring(doc_sentence,'utf-8'))+'\n')
			f.write('</Annotation>')
			f.close()
			sentences=[]
