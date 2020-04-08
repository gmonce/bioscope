# -*- coding: utf-8 -*- 
# Script que actualiza el campo sentence_type de bioscope para separar en entrenamiento y held out
# Uso: split_training_corpus.py {BIOSCOPE | BIOSCOPED}

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import sys
import sqlite3
import random


dbname=os.path.join(sys.argv[1],'bioscope.db')
script_name=os.path.join(sys.path[0],sys.argv[0])

	
#Abro la tabla bioscope en dbfile
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c2=conn.cursor()

# Recorro la tabla bioscope y separo el 80% de las oraciones entre entrenamiento y testeo
c.execute('select document_id,sentence_id from bioscope_train group by sentence_id')
for row in c:
	#Sorteo
	if random.random()<0.8:
		sentence_type='TRAIN';
	else:
		sentence_type='TEST';
	c2.execute('update bioscope_train set sentence_type=? where document_id=? and sentence_id=?',(sentence_type,row['document_id'],row['sentence_id']))
conn.commit()
c2.close()
c.close()