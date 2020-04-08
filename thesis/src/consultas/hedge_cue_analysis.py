# -*- coding: utf-8 -*- 

# Script que analiza las hedge cues y como se reconocieron  y cuenta apariciones en el training corpus
# python hedge_cue_analysis.py 

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import sys
import sqlite3
import random

if len(sys.argv)>1:
	document_id=sys.argv[1]
	sentence_id=sys.argv[2]
else:
	document_id=None
	sentence_id=None


working_dir=os.path.expandvars('$BIOSCOPE')		
dbname=os.path.join(working_dir,'bioscope.db')
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()
c2=conn.cursor()

# Obtengo la lista de oraciones  a a analizar
if not document_id:
	c.execute('select document_id,sentence_id from bioscope_test  group by document_id,sentence_id')
else:
	c.execute('select document_id,sentence_id from bioscope_test  where document_id=? and sentence_id=? group by document_id,sentence_id',[document_id,sentence_id])

hedge_cues=[]
guessed_hedge_cues=[]
for row in c:
	# Armo la lista de hedge cues en el corpus de evaluacion
	c1.execute('select * from bioscope_test  where document_id=? and sentence_id=? and hedge_cue="B-SPECCUE"  order by token_num',[row['document_id'],row['sentence_id']])
	# Recorro los tokens de las hedge cues (puede haber más de una)
	for t in c1:
		# Armo la hedge cue
		c2.execute('select * from bioscope_test t1 where document_id=? and sentence_id=? and token_num>? and hedge_cue in ("I-SPECCUE","D-SPECCUE") and not exists (select * from bioscope_test t2 where document_id=? and sentence_id=? and hedge_cue="B-SPECCUE" and token_num>? and token_num<t1.token_num)', [row['document_id'],row['sentence_id'],t['token_num'],row['document_id'],row['sentence_id'], t['token_num']])
		hedge_cue=t['word']+' '
		discontinua=False
		for row2 in c2:
			if row2['hedge_cue']=='D-SPECCUE':
				discontinua=True	
			hedge_cue+=row2['word']+' '
		if discontinua:
			hedge_cue+="* "
		# Cuando termino, elimino el último blanco
		hedge_cue=hedge_cue[:-1]
		# Inserto en la lista de HC
		hedge_cues.append([row['document_id'],row['sentence_id'],t['token_num'],hedge_cue])

	# Armo la lista de guessed hedge cues para la oracion
	c1.execute('select * from bioscope_test where document_id=? and sentence_id=? and guessed_hedge_cue="B-SPECCUE" order by token_num',[row['document_id'],row['sentence_id']])
	for t in c1:
		# Armo la hedge cue
		c2.execute('select * from bioscope_test t1 where document_id=? and sentence_id=? and token_num>? and guessed_hedge_cue in ("I-SPECCUE","D-SPECCUE") and not exists (select * from bioscope_test t2 where document_id=? and sentence_id=? and hedge_cue="B-SPECCUE" and token_num>? and token_num<t1.token_num)', [row['document_id'],row['sentence_id'],t['token_num'],row['document_id'],row['sentence_id'], t['token_num']])
		hedge_cue=t['word']+' '
		discontinua=False
		for row2 in c2:
			if row2['guessed_hedge_cue']=='D-SPECCUE':
				discontinua=True
			hedge_cue+=row2['word']+' '
		if discontinua:
			hedge_cue+="* "
		# Cuando termino, elimino el último blanco
		hedge_cue=hedge_cue[:-1]
		# Inserto en la lista de HC
		guessed_hedge_cues.append([row['document_id'],row['sentence_id'],t['token_num'],hedge_cue])

# Armo la lista de hedge cues que aparecen en el training corpus, solamente los textos
training_hedge_cues=[]
c.execute('select document_id,sentence_id from bioscope_train group by document_id,sentence_id')
for row in c:
	c1.execute('select * from bioscope_train where document_id=? and sentence_id=? and hedge_cue="B-SPECCUE" order by token_num',[row['document_id'],row['sentence_id']])
	for t in c1:
		c2.execute('select * from bioscope_train t1 where document_id=? and sentence_id=? and token_num>? and hedge_cue in ("I-SPECCUE","D-SPECCUE") and not exists (select * from bioscope_train t2 where document_id=? and sentence_id=? and hedge_cue="B-SPECCUE" and token_num>? and token_num<t1.token_num)', [row['document_id'],row['sentence_id'],t['token_num'],row['document_id'],row['sentence_id'], t['token_num']])
		hedge_cue=t['word']+' '
		discontinua=False
		for row2 in c2:
			if row2['hedge_cue']=='D-SPECCUE':
				discontinua=True
			hedge_cue+=row2['word']+' '
		if discontinua:
			hedge_cue+="* "
		hedge_cue=hedge_cue[:-1]
		training_hedge_cues.append(hedge_cue)


# Cuento TP,FP,FN
hc_list=dict([])
tp=0
fn=0
fp=0
for hc in hedge_cues:
	hedge_cue=hc[3]

	if hedge_cue not in hc_list:
		hc_list[hedge_cue]=[0,0,0,0,0]

	if hc in guessed_hedge_cues:
		# Aumento TP
		hc_list[hedge_cue][0]+=1
		tp+=1
	else:
		# Aumento FN
		hc_list[hedge_cue][1]+=1
		fn+=1

for hc in guessed_hedge_cues:
	hedge_cue=hc[3]
	if hedge_cue not in hc_list:
		hc_list[hedge_cue]=[0,0,0,0,0]
	if hc not in hedge_cues:
		# Aumento FP
		hc_list[hedge_cue][2]+=1
		fp+=1


# Recorro la lista de hedge cues y veo si aparecían en el corpus de entrenamiento como hedge cue
# Si no aparecían, las guardo para listar

# Levanto el corpus en formato texto
f = open('training_corpus.txt', 'r')
tc=f.read()
for (key,item) in hc_list.iteritems():
	if key in training_hedge_cues:
		hc_list[key][3]+=training_hedge_cues.count(key)
	# Veo el total de ocurrencias en el training corpus
	# Tiene que existir el archivo training_corpus.txt con los textos
	hc_list[key][4]+=tc.count(' '+key)



print 'Hedge cue,TP,FN,FP,in_tc_as_hc,in_tc'
for (key,item) in hc_list.iteritems():
	print key+","+",".join([str(x) for x in item])

