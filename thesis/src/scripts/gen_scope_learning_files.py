# -*- coding: utf-8 -*- 
# Script que  genera los archivos de entrenamiento correspondientes
# Uso: gen_scope_corpus.py dbname training_file test_file test_file_ghc scenario total


import pln_inco.bioscope.scope_rules
import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3
from string import *


	
def gen_conll_file_scope(dbname,tablename,sentence_type,filename,xs,y,is_training_file=True,is_guessed_cue=False):
	""" 
	Genera el archivo para el entrenamiento/evaluación de scopes con CRF++, a partir de la tabla de bioscope que se le indique (bioscope80_scope o 
	bioscope20_scope)
	Este archivo está en formato CoNLL, tiene una línea por token, los atributos están
	separados por espacio, y el último es el que vamos a usar para clasificar. Las oraciones está­n separadas por líneas
	en blanco
	@arg dbname: nombre del archivo que tiene la base de datos
	@type dbname:C{string}
	@arg tablename: nombre de la tabla a partir de la cual generar el archivo
	@type tablename:C{string}
	@arg sentence_type: indica el string que deben tener las instancias en el campo SENTENCE_TYPE (solo tiene sentido si has_instances=False
	@type sentence_type: C{string}
	@arg xs: lista de atributos a generar. Tienen que ser iguales a las columnas de la tabla de atributos de bioscope. No incluyen la clase a aprender.
	@type xs: List
	@arg y: Clase a aprender (es uno de los atributos)
	@type y:List
	@arg is_training_file: Indica si estamos generando un archivo de entrenamiento (en tal caso, debe ponerse la clase a aprender al final. Sino, no se pone
	@type y:Boolean
	
	"""

	content=''	
	t0=time.clock()
	f=open(filename,'w+')
	conn= sqlite3.connect(dbname)	
	conn.text_factory = str
	conn.row_factory=sqlite3.Row
	c=conn.cursor()
	
	# Armo la lista separada por comas de los atributos
	# Por supuesto deben llamarse igual que las columnas de la tabla
	cabezal_select=','.join(xs)
	
	#Cambio
	if is_training_file:
		cabezal_select=cabezal_select+','+y+' '
	else:
		if not is_guessed_cue:
			cabezal_select=cabezal_select+',scope '

	c.execute('select document_id,sentence_id,token_num,hc_start,'+cabezal_select+' from '+tablename+' order by document_id,sentence_id,hc_start,token_num')
	
	prev_sentence_id='-1'	
	prev_instance=-1
	in_scope=False
	for row in c:
				if (prev_sentence_id != row['sentence_id'] or prev_instance != row['hc_start']):
					#Fin de la oración, dejo un espacio en blanco, excepto en la primera
					if prev_sentence_id != '-1':					
						content=content+'\n'
					prev_sentence_id = row['sentence_id']
					prev_instance=row['hc_start']
				for k in row.keys():
						value=row[k]		
						content=content+str(value)+'\t'

				#Borro el último tabulador
				content=rstrip(content)
				content=content+'\n'	
				#print content
				f.write(content)
				content=''
	f.close()
	c.close()
	#print 'Tiempo del proceso:', time.clock()-t0




dbname=sys.argv[1]
training_file=sys.argv[2]
test_file=sys.argv[3]
ghc_test_file=sys.argv[4]
scenario_file=sys.argv[5]

if len(sys.argv)>6:
	total=sys.argv[6]
else:
	total='N'

# Escenario con los atributos de entrenamiento/clase a aprender
scenario=open(scenario_file)
conf=yaml.load(scenario)
xs=conf['xs']
y=conf['y'] 

script_name=os.path.join(sys.path[0],sys.argv[0])

print script_name,"Generating training file",training_file
if total=='Y':
	gen_conll_file_scope(dbname,'bioscope_train_scope',None,training_file,xs,y,is_training_file=True)
else:
	gen_conll_file_scope(dbname,'bioscope80_scope',None,training_file,xs,y,is_training_file=True)


print script_name+":Generating test file",test_file
if total=='Y':
	#Cambio: tambien genero la clase original en el test file, para medir token accuracy
	# Solo lo hago cuando tengo la hedge cue original, sino no se puede, porque no lo tengo (obvio)
	gen_conll_file_scope(dbname,'bioscope_test_scope',None,test_file,xs,y,is_training_file=False)
else:
	gen_conll_file_scope(dbname,'bioscope20_scope',None,test_file,xs,y,is_training_file=False)

print script_name+":Generating test file, using guessed hedge cue", ghc_test_file
if total=='Y':
	gen_conll_file_scope(dbname,'bioscope_test_ghc_scope',None,ghc_test_file, xs,y,is_training_file=False,is_guessed_cue=True)
else:
	gen_conll_file_scope(dbname,'bioscope20_ghc_scope',None,ghc_test_file, xs,y,is_training_file=False,is_guessed_cue=True)
