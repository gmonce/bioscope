# -*- coding: utf-8 -*- 
# Agrega una columna a la tabla bioscope_train y test para indicar si la palabra es candidata a hc (aparece en el corpus de entrenamiento como hedge cue)
# o si aparece junto con otra candidata a hedge cue
# este valor será incorporado como atributo al aprendizaje
# Uso: python add_hc_corpus_occurrences.py working_dir

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3

working_dir=sys.argv[1]
script_name=os.path.join(sys.path[0],sys.argv[0])
dbname=os.path.join(working_dir,'bioscope.db')

if len(sys.argv)>2:
	total=sys.argv[2]
else:
	total='N'


# Inicializo la conexión
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()

try:
	c.execute('alter table bioscope_train add hc_candidate string')
except sqlite3.OperationalError:
	pass

try:
	c.execute('alter table bioscope_train add cooccurs_with_hc_candidate string')
except sqlite3.OperationalError:
	pass


try:
	c.execute('alter table bioscope_test add hc_candidate string')
except sqlite3.OperationalError:
	pass

try:
	c.execute('alter table bioscope_test add cooccurs_with_hc_candidate string')
except sqlite3.OperationalError:
	pass




c.execute('update bioscope_train set hc_candidate=\'N\'')
c.execute('update bioscope_train set cooccurs_with_hc_candidate=\'N\'')

c.execute('update bioscope_test set hc_candidate=\'N\'')
c.execute('update bioscope_test set cooccurs_with_hc_candidate=\'N\'')

conn.commit()

# Obtengo todas las hedge cues del corpus de entrenamiento, sin el held out, y actualizo el corpus de entrenamiento completo
# Solamente tengo en cuenta aquellas que son de una sola palabra, para no meter ruido

if total=='N':
	c.execute('select distinct word from bioscope_train b1 where sentence_type=\'TRAIN\' and hedge_cue=\'B-SPECCUE\' and not exists \
			(select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.token_num=b1.token_num+1 		and b2.hedge_cue<>\'O\') and not exists \
			(select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue=\'D-SPECCUE\')');
else:
	c.execute('select distinct word from bioscope_train b1 where hedge_cue=\'B-SPECCUE\' and not exists \
			(select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.token_num=b1.token_num+1 		and b2.hedge_cue<>\'O\') and not exists \
			(select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue=\'D-SPECCUE\')');

rows=c.fetchall();
for row in rows:
	c.execute('update bioscope_train set hc_candidate=\'Y\' where word=?',[row['word']]);


# Obtengo todas las hedge cues del corpus de entrenamiento y actualizo el corpus de evaluación
c.execute('select distinct word from bioscope_train b1 where hedge_cue=\'B-SPECCUE\' and not exists \
	(select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.token_num=b1.token_num+1 \
	and b2.hedge_cue<>\'O\') and not exists \
	(select * from bioscope_train b2 where b2.document_id=b1.document_id and b2.sentence_id=b1.sentence_id and b2.hedge_cue=\'D-SPECCUE\')');
rows=c.fetchall();
for row in rows:
	c.execute('update bioscope_test set hc_candidate=\'Y\' where word=?',[row['word']]);
	

# Agrego la marca de coocurrencia con una hedge cue a todas las demás palabras de la oración
c.execute('select document_id,sentence_id,token_num from bioscope_train b1 where hc_candidate=\'Y\'')
for row in c:
	c1.execute('update bioscope_train set cooccurs_with_hc_candidate=\'Y\' where document_id=? and sentence_id=? and hc_candidate=\'Y\' and token_num<>?',[row['document_id'],row['sentence_id'],row['token_num']])


# Agrego la marca de coocurrencia con una hedge cue a todas las demás palabras de la oración, evaluation corpus
c.execute('select document_id,sentence_id,token_num from bioscope_test b1 where hc_candidate=\'Y\'')
for row in c:
	c1.execute('update bioscope_test set cooccurs_with_hc_candidate=\'Y\' where document_id=? and sentence_id=? and hc_candidate=\'Y\' and token_num<>?',[row['document_id'],row['sentence_id'],row['token_num']])

conn.commit()

