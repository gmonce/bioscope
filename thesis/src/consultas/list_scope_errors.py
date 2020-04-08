# -*- coding: utf-8 -*- 
# Uso: python cons_scopes_simple.py $BIOSCOPE tabla
# Script que mira las oraciones en el corpus de entrenamiento y se fija si coincide con el scope de algún constituyente del aŕbol sintáctico

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3

working_dir=sys.argv[1]
table=sys.argv[2]
dbname=os.path.join(working_dir,'bioscope.db')
script_name=os.path.join(sys.path[0],sys.argv[0])


t0=time.clock()
# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()
err=conn.cursor()

# Inicializo el diccionario de hedge cues
hc_list=dict([])

#Consulto todas las oraciones con error
err.execute("select document_id,sentence_id,hc_start from "+ table+" where scope<>guessed_scope group by document_id,sentence_id,hc_start")
for row in err:
		# Obtengo los atributos de la instancia
		c1.execute("select * from "+table+" where document_id=? and sentence_id=? and hc_start=?",(row['document_id'],row['sentence_id'], row['hc_start']))
		for row1 in c1:
			print "#".join([row['document_id'],row['sentence_id'],str(row['hc_start']),row1['word'],row1['pos'],row1['hc_token'],row1['scope'],row1['guessed_scope'],row1['hc_parent_pos'],row1['in_hc_parent_scope'],row1['hc_gparent_pos'],row1['in_hc_gparent_scope'], row1['hc_ggparent_pos'],row1['in_hc_ggparent_scope'],row1['in_nexts_scope'],row1['passive_voice']])
