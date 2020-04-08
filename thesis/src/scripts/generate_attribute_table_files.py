# -*- coding: utf-8 -*- 
# Levanta el corpus de los archivos y genera los archivos html de atributos
# Recibe como parámetros el directorio de trabajo, el xml con el corpus,el prefijo de nombres de documentos a levantar y un indicador binario de si solo generar las oraciones que tienen hedge y/o negación
# Ejemplo python generate_attribute_table_files.py $BIOSCOPE  a


import pln_inco.bioscope as bioscope
import os.path
import time
from sys import *
import codecs

working_dir=argv[1]
prefix=argv[2]

for bioscope_xml_file in ['abstracts_train.xml', 'abstracts_test.xml']:
	
	bcp=bioscope.BioscopeCorpusProcessor(working_dir, bioscope_xml_file)
	bc=bioscope.BioscopeCorpus(bcp,prefix)
	
	for (docId,d) in bc.documents.iteritems():
		#print >> stderr, "Genero atributos para el documento ",docId	
		for (sentenceId,sentence) in d.sentences.iteritems():
			if sentence.data_loaded:
				s_table=sentence.get_basic_attributes()
				tabFileName=docId+'.'+sentenceId+'.html'
				f=codecs.open(os.path.join(bcp.attribute_table_files_dir,tabFileName),'w+',encoding='utf-8')
				f.write('<HTML><BODY><TABLE border=1>\n')
				content=''
				i=0
				for s in s_table:
					content +='<TR>'
					if i==0:
						for e in s:
							if type(e)==list:
								content +='<TH>'+'['+','.join(e)+']'+'</TH>'					
							else:
								content +='<TH>'+e+'</TH>'					
					else:
						for e in s:	
							if not e: e='None'
							
							if type(e)==list:
								content +='<TD>'+'['+','.join(e)+']'+'</TD>'													
							else:
								content +='<TD>'+e+'</TD>'
					content=content+'</TR>\n'
					i=i+1
				f.write(content)
				f.write('</TABLE></BODY></HTML>')
				f.close()
