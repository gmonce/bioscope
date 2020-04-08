# -*- coding: utf-8 -*- 
# Uso: insert_scope_errors.py $BIOSCOPE $RUNX $TOTAL

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3

working_dir=sys.argv[1]
runx=sys.argv[2]

if len(sys.argv)>3:
	total=sys.argv[3]
else:
	total='N'

dbname=os.path.join(working_dir,'bioscope.db')


# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

if total=='N':
	error_table='scope_learning_errors_heldout'
	source_table='bioscope20_scope'
else:
	error_table='scope_learning_errors'
	source_table='bioscope_test_scope'

script_name=os.path.join(sys.path[0],sys.argv[0])


t0=time.clock()
# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

# Primero borro lo que había, por las dudas
c.execute("delete from "+error_table+" where runx=?",(runx,))


c.execute("insert into "+error_table+" select document_id,sentence_id,hc_start,? from "+ source_table +" where  scope<>guessed_scope  group by document_id,sentence_id,hc_start",(runx,))


conn.commit()
