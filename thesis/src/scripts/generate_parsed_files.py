# -*- coding: utf-8 -*- 
# A partir de los articulos procesados con genia, genera los correspondientes resultados del análisis con el parser de stanford
# Recibe como parámetros el directorio de trabajo, el patrón de los archivos a generar, y un indicador binario que indica si debe regenerarse
# Ejemplo python generate_parsed_files.py $BIOSCOPE 'a*.genia' 1

import sys
import os.path
import pln_inco.stanford_parser
import pln_inco.bioscope
import string
import fnmatch

working_dir=sys.argv[1]
pattern=sys.argv[2]
regenerate=sys.argv[3]

parser_grammar_file='edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'

#xml_list=['abstracts_train.xml', 'abstracts_test.xml']
# En realidad esto no importa porque parsea todos los archivos del directorio, hay que corregirlo
# el bcp necesita un xml_file, pero creo que no lo usa.
xml_list=['abstracts_train.xml']

for bioscope_xml_file in xml_list:
	bcp=pln_inco.bioscope.BioscopeCorpusProcessor(working_dir, bioscope_xml_file)

	for fileName in os.listdir(bcp.genia_articles_dir):
			#print >>sys.stderr, "Considero...", fileName
			if fnmatch.fnmatch(fileName,pattern):
				#print 'Pruebo si existe:',os.path.join(bcp.parsed_files_dir,fileName.replace('.genia','.parsed'))
				if not os.path.exists(os.path.join(bcp.parsed_files_dir,fileName.replace('.genia','.parsed'))) or regenerate=='1':
					print>>sys.stderr,  'Parseo...:'+fileName
					source=open(os.path.join(bcp.genia_articles_dir,fileName),'r')
					sentences=source.read().splitlines()
					result=pln_inco.stanford_parser.lexicalized_parser_parse(sentences)
					document_result='\n'.join(result)
					dest=open(os.path.join(bcp.parsed_files_dir,fileName.replace('.genia','.parsed')),'w+')
					dest.write(document_result)
					source.close()
					dest.close()
				else:
					#print>>sys.stderr, 'Ya exist�a...:'+fileName
					pass
