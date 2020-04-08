# -*- coding: utf-8 -*- 
# Actualiza el valor de los hedge cue discontinuos como either..or
# están marcados ambos como B-SPECCUE, pero si aparecen en el mismo scope
# tengo que cambiar al segundo para que diga D-SPECCUE
# lo hago directamente en las tablas 
# Uso: python update_discontinuous_hc.py working_dir

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3

working_dir=sys.argv[1]
dbname=os.path.join(working_dir,'bioscope.db')
script_name=os.path.join(sys.path[0],sys.argv[0])

# Inicializo la conexión
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()


# Obtengo todos los tokens del corpus de entrenamiento que forman parte de un mismo scope con otro B-SPECCUE
# y son B-SPECCUE, y les cambio la etiqueta
c.execute('select * from bioscope_train b1 where hedge_cue1=\'B-SPECCUE\' and exists  (select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue1=\'B-SPECCUE\' and b2.token_num<b1.token_num and not exists (select * from bioscope_train b4 where b4.document_id=b1.document_id and b4.sentence_id=b1.sentence_id	and b4.token_num>=b2.token_num and b4.token_num<=b1.token_num and b4.hedge_scope1=\'O\') and 1>=(select count(*) from bioscope_train b3 where b3.document_id=b1.document_id and b3.sentence_id=b1.sentence_id and b3.token_num>=b2.token_num and b3.token_num<=b1.token_num and hedge_scope1=\'B-SPECXCOPE\'))')
for row in c:
		print "Actualizo nivel 1...",[row['document_id'],row['sentence_id'],row['token_num']]
		c1.execute('update bioscope_train set hedge_cue1=\'D-SPECCUE\', hedge_cue=\'D-SPECCUE\' where document_id=? and sentence_id=? and token_num=?',[row['document_id'],row['sentence_id'],row['token_num']])
	
c.execute('select * from bioscope_train b1 where hedge_cue2=\'B-SPECCUE\' and exists  (select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue2=\'B-SPECCUE\' and b2.token_num<b1.token_num and not exists (select * from bioscope_train b4 where b4.document_id=b1.document_id and b4.sentence_id=b1.sentence_id	and b4.token_num>=b2.token_num and b4.token_num<=b1.token_num and b4.hedge_scope2=\'O\') and 1>=(select count(*) from bioscope_train b3 where b3.document_id=b1.document_id and b3.sentence_id=b1.sentence_id and b3.token_num>=b2.token_num and b3.token_num<=b1.token_num and hedge_scope2=\'B-SPECXCOPE\'))')
for row in c:
		print "Actualizo nivel 2...",[row['document_id'],row['sentence_id'],row['token_num']]
		c1.execute('update bioscope_train set hedge_cue2=\'D-SPECCUE\', hedge_cue=\'D-SPECCUE\' where document_id=? and sentence_id=? and token_num=?',[row['document_id'],row['sentence_id'],row['token_num']])
	
c.execute('select * from bioscope_train b1 where hedge_cue3=\'B-SPECCUE\' and exists  (select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue3=\'B-SPECCUE\' and b2.token_num<b1.token_num and not exists (select * from bioscope_train b4 where b4.document_id=b1.document_id and b4.sentence_id=b1.sentence_id	and b4.token_num>=b2.token_num and b4.token_num<=b1.token_num and b4.hedge_scope3=\'O\') and 1>=(select count(*) from bioscope_train b3 where b3.document_id=b1.document_id and b3.sentence_id=b1.sentence_id and b3.token_num>=b2.token_num and b3.token_num<=b1.token_num and hedge_scope3=\'B-SPECXCOPE\'))')
for row in c:
		print "Actualizo nivel 3...",[row['document_id'],row['sentence_id'],row['token_num']]
		c1.execute('update bioscope_train set hedge_cue3=\'D-SPECCUE\', hedge_cue=\'D-SPECCUE\' where document_id=? and sentence_id=? and token_num=?',[row['document_id'],row['sentence_id'],row['token_num']])
	
#Hago lo mismo con las tablas de evaluación
c.execute('select * from bioscope_test b1 where hedge_cue1=\'B-SPECCUE\' and exists  (select * from bioscope_test b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue1=\'B-SPECCUE\' and b2.token_num<b1.token_num and not exists (select * from bioscope_test b4 where b4.document_id=b1.document_id and b4.sentence_id=b1.sentence_id	and b4.token_num>=b2.token_num and b4.token_num<=b1.token_num and b4.hedge_scope1=\'O\') and 1>=(select count(*) from bioscope_test b3 where b3.document_id=b1.document_id and b3.sentence_id=b1.sentence_id and b3.token_num>=b2.token_num and b3.token_num<=b1.token_num and hedge_scope1=\'B-SPECXCOPE\'))')
for row in c:
	print "Actualizo nivel 1...",[row['document_id'],row['sentence_id'],row['token_num']]
	c1.execute('update bioscope_test set hedge_cue1=\'D-SPECCUE\', hedge_cue=\'D-SPECCUE\' where document_id=? and sentence_id=? and token_num=?',[row['document_id'],row['sentence_id'],row['token_num']])

c.execute('select * from bioscope_test b1 where hedge_cue2=\'B-SPECCUE\' and exists  (select * from bioscope_test b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue2=\'B-SPECCUE\' and b2.token_num<b1.token_num and not exists (select * from bioscope_test b4 where b4.document_id=b1.document_id and b4.sentence_id=b1.sentence_id	and b4.token_num>=b2.token_num and b4.token_num<=b1.token_num and b4.hedge_scope2=\'O\') and 1>=(select count(*) from bioscope_test b3 where b3.document_id=b1.document_id and b3.sentence_id=b1.sentence_id and b3.token_num>=b2.token_num and b3.token_num<=b1.token_num and hedge_scope2=\'B-SPECXCOPE\'))')
for row in c:
	print "Actualizo nivel 2...",[row['document_id'],row['sentence_id'],row['token_num']]
	c1.execute('update bioscope_test set hedge_cue2=\'D-SPECCUE\', hedge_cue=\'D-SPECCUE\' where document_id=? and sentence_id=? and token_num=?',[row['document_id'],row['sentence_id'],row['token_num']])

c.execute('select * from bioscope_test b1 where hedge_cue3=\'B-SPECCUE\' and exists  (select * from bioscope_test b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue3=\'B-SPECCUE\' and b2.token_num<b1.token_num and not exists (select * from bioscope_test b4 where b4.document_id=b1.document_id and b4.sentence_id=b1.sentence_id	and b4.token_num>=b2.token_num and b4.token_num<=b1.token_num and b4.hedge_scope3=\'O\') and 1>=(select count(*) from bioscope_test b3 where b3.document_id=b1.document_id and b3.sentence_id=b1.sentence_id and b3.token_num>=b2.token_num and b3.token_num<=b1.token_num and hedge_scope3=\'B-SPECXCOPE\'))')
for row in c:
	print "Actualizo nivel 3...",[row['document_id'],row['sentence_id'],row['token_num']]
	c1.execute('update bioscope_test set hedge_cue3=\'D-SPECCUE\', hedge_cue=\'D-SPECCUE\' where document_id=? and sentence_id=? and token_num=?',[row['document_id'],row['sentence_id'],row['token_num']])


conn.commit()

