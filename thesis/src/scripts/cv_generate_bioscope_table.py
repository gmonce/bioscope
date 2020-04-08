# -*- coding: utf-8 -*- 
# Uso: cv_generate_bioscope_table.py $BIOSCOPE 

import os.path
import time
import sys
import sqlite3
import random

working_dir=sys.argv[1]
dbname=os.path.join(working_dir,'bioscope.db')


# Inicializo la conexión a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

script_name=os.path.join(sys.path[0],sys.argv[0])
bioscope_table='BIOSCOPE'

t0=time.clock()
# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c2=conn.cursor()

try:
	c.execute('drop table bioscope')
except sqlite3.OperationalError:
	pass
c.execute("create table bioscope as select document_id, sentence_id,token_num,word,lemma,pos,chunk,ner,hedge_cue,hedge_cue1,hedge_cue2,hedge_cue3,hedge_scope1,hedge_scope2,hedge_scope3, is_hyland_hedge, hc_candidate, cooccurs_with_hc_candidate from bioscope_train")
c.execute('alter table bioscope add column split integer')

# Inicializo el split 1 con lo que había en bioscope_test
c.execute("insert into bioscope select document_id, sentence_id, token_num,word,lemma,pos,chunk,ner,hedge_cue,hedge_cue1,hedge_cue2,hedge_cue3,hedge_scope1,hedge_scope2,hedge_scope3, is_hyland_hedge, hc_candidate, cooccurs_with_hc_candidate,1 from bioscope_test")

c.execute('create unique index ipk_bioscope on bioscope (document_id,sentence_id,token_num)')
c.execute('select document_id from bioscope group by document_id')
for row in c:
        #Sorteo
	split=str(random.uniform(1,10.99)).split('.')[0]
        c2.execute('update bioscope set split=?  where document_id=?',(split,row['document_id']))


conn.commit()
