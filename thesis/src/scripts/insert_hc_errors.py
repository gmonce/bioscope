# -*- coding: utf-8 -*- 
# Uso: insert_hc_errors.py $BIOSCOPE $RUN $TOTAL

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3

working_dir=sys.argv[1]
run=sys.argv[2]

if len(sys.argv)>3:
	total=sys.argv[3]
else:
	total='N'

dbname=os.path.join(working_dir,'bioscope.db')


# Inicializo la conexión a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

if total=='N':
	error_table='hc_learning_errors_heldout'
else:
	error_table='hc_learning_errors'

script_name=os.path.join(sys.path[0],sys.argv[0])


t0=time.clock()
# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

# Primero borro lo que había, por las dudas
c.execute("delete from "+error_table+" where run=?",(run,))

if total=='N':
	c.execute("insert into "+error_table+" select document_id,sentence_id,? from bioscope_train where sentence_type='TEST' and hedge_cue<>guessed_hedge_cue group by document_id,sentence_id",(run,))
else:
	c.execute("insert into "+error_table+" select document_id,sentence_id,? from bioscope_train where  hedge_cue<>guessed_hedge_cue group by document_id,sentence_id",(run,))

conn.commit()
