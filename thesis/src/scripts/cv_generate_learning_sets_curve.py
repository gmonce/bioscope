# -*- coding: utf-8 -*- 
# Uso: cv_generate_learning_sets.py $BIOSCOPE 
import os.path
import time
import sys
import sqlite3

working_dir=sys.argv[1]
dbname=os.path.join(working_dir,'bioscope.db')
split=int(sys.argv[2])

# Inicializo la conexión a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

script_name=os.path.join(sys.path[0],sys.argv[0])

t0=time.clock()
# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c2=conn.cursor()

c.execute("delete from bioscope_train")
c.execute("delete from bioscope_test")
c.execute("select * from bioscope where split<=?",[split])
for row in c:
	c2.execute("insert into bioscope_train (document_id,sentence_id,token_num,word,lemma,pos,chunk,ner,hedge_cue,hedge_cue1,hedge_cue2,hedge_cue3,hedge_scope1,hedge_scope2,hedge_scope3,is_hyland_hedge,hc_candidate,cooccurs_with_hc_candidate) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",[row['document_id'],row['sentence_id'],row['token_num'],row['word'],row['lemma'],row['pos'],row['chunk'],row['ner'],row['hedge_cue'],row['hedge_cue1'],row['hedge_cue2'],row['hedge_cue3'],row['hedge_scope1'],row['hedge_scope2'],row['hedge_scope3'],row['is_hyland_hedge'],row['hc_candidate'],row['cooccurs_with_hc_candidate']])

c.execute("select * from bioscope where split=10")
for row in c:
	c2.execute("insert into bioscope_test (document_id,sentence_id,token_num,word,lemma,pos,chunk,ner,hedge_cue,hedge_cue1,hedge_cue2,hedge_cue3,hedge_scope1,hedge_scope2,hedge_scope3,is_hyland_hedge,hc_candidate,cooccurs_with_hc_candidate) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",[row['document_id'],row['sentence_id'],row['token_num'],row['word'],row['lemma'],row['pos'],row['chunk'],row['ner'],row['hedge_cue'],row['hedge_cue1'],row['hedge_cue2'],row['hedge_cue3'],row['hedge_scope1'],row['hedge_scope2'],row['hedge_scope3'],row['is_hyland_hedge'],row['hc_candidate'],row['cooccurs_with_hc_candidate']])

conn.commit()
