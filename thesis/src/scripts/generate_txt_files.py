# -*- coding: utf-8 -*- 
# Dado el corpus, genera archivos .txt con los textos de las oraciones
# Recibe como parámetros el directorio de trabajo
# Si corpus_id=CONLL, entonces estamos hablando del archivo de evaluación del shared task 2010
# Ejemplo python generate_txt_files.py $BIOSCOPE corpus_id

import sys
import os.path
import pln_inco.bioscope 
import codecs

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
				
				# Genero el documento
				#print >> sys.stderr, "Genero documento txt...",docId
					
				fileName=os.path.join(bcp.txt_dir,'a'+docId+'.txt')
				f=codecs.open(fileName,'w', encoding='utf-8')
				#f.write(pln_inco.bioscope.bioscope_get_text(title)+'\n')
				for (doc_sentence,sentence_text) in sentences:
					f.write(sentence_text+'\n')
				f.close()
				sentences=[]



