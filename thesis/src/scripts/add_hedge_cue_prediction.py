# -*- coding: utf-8 -*- 
# Script que carga las hedge_cue predichas a la tabla BIOSCOPE_TRAIN, para las instancias del held-out corpus
# El parámetro total vale Y o N e indica si utilizar todo el corpus de entrenamiento y evaluar sobre el de evaluación
# o evaluar sobre el heldout
# por defecto vale N
# Uso: add_hedge_cue_prediction.py {$BIOSCOPE | $BIOSCOPED} $RUN $TOTAL

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

if total=='Y':
	results_hc_file=os.path.join(working_dir,'crf_corpus','hc',run,'test.total.data.crf_results')
	table_to_update='bioscope_test'
else:
	results_hc_file=os.path.join(working_dir,'crf_corpus','hc',run,'test.data.crf_results')
	table_to_update='bioscope_train'

script_name=os.path.join(sys.path[0],sys.argv[0])


t0=time.clock()
# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

# Abro el archivo y lo voy recorriendo
# Asumo que en las primeras tres columnas está el documento, la oraición y el token_num
f=open(results_hc_file,'r')
for line in f:
	if line.startswith('#'):
		seq_guess_confidence=line.rstrip().split(' ')[1]
		#print "Confidence de la secuencia...",seq_guess_confidence
	elif line !='\n':
		tokens=line.rstrip().split('\t')			
		document_id=tokens[0]
		sentence_id=tokens[1]
		token_num=tokens[2]			
		(hedge_cue_class,confidence)=tokens[-1].split('/')		 
		#print "Actualizo ", document_id, sentence_id, token_num, hedge_cue_class,confidence
		c.execute('update '+table_to_update+' set guessed_hedge_cue=?, guessed_hc_token_guess_confidence=?, guessed_hc_seq_guess_confidence=? where document_id=? and sentence_id=? and token_num=?',(hedge_cue_class, confidence, seq_guess_confidence,document_id,sentence_id,token_num))
conn.commit()
f.close()
