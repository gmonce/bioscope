# -*- coding: utf-8 -*- 
# Script que  actualiza el campo scope en la tabla BIOSCOPE20_SCOPE o BIOSCOPE20_GHC_SCOPE
# Uso: update_guessed_scope dbname test_file table_name

import sqlite3
import sys
import os.path

dbname=sys.argv[1]
results_filename=sys.argv[2]
table_name=sys.argv[3]

script_name=os.path.join(sys.path[0],sys.argv[0])


# Inicializo la conexión
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

# Levanto el resultado del aprendizaje
# Y actualizo el campo guessed_scope para reflejar lo obtenido
# Abreo el archivo y lo voy recorriendo
# Asumo que en las primeras cuatro columnas está el documento, la oración, el token_num y el hc_start
# Y en la última el resultado del aprendizaje
f=open(results_filename,'r')
for line in f:
	if line !='\n' and not line.startswith('#'):
		tokens=line.rstrip().split('\t')			
		document_id=tokens[0]
		sentence_id=tokens[1]
		token_num=tokens[2]	
		hc_start=tokens[3]	
		(tag,confidence)=tokens[-1].split('/')
		tokens[-1]=tag
		c.execute('update '+table_name+' set guessed_scope=? where document_id=? and sentence_id=? and token_num=? and hc_start=?',(tokens[-1],document_id,sentence_id,token_num,hc_start))
conn.commit()
f.close()	

