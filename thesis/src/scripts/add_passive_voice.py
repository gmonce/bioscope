# -*- coding: utf-8 -*- 
# Script que marca el atributo passive_voice, indicando si la hedge cue corresponde a una marca de voz pasiva
# Lo detecta si a la derecha hay un be/VB y luego un VBN (en una ventana de 5)
# python add_passive_voice.py {$BIOSCOPE | $BIOSCOPED} TOTAL


import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import sqlite3
from sys import *


working_dir=sys.argv[1]

if len(sys.argv)>2:
	total=sys.argv[2]
else:
	total='N'



dbname=os.path.join(working_dir,'bioscope.db')
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()
c2=conn.cursor()
c3=conn.cursor()


if total=='N':
	table_list=['bioscope80_scope','bioscope20_scope','bioscope20_ghc_scope']
else:
	table_list=['bioscope_train_scope','bioscope_test_scope','bioscope_test_ghc_scope']



for source_table in table_list:
	c.execute("update "+source_table+" set passive_voice='N'")

	# Obtengo todos los documentos que tienen "be" en algún lado, como candidatos.
	c.execute("select document_id,sentence_id,hc_start from "+ source_table+" where lemma='be' group by document_id,sentence_id,hc_start")
	for row in c:
		# Tiene que haber un be cerca de la hedge cue
		c1.execute("select count(*) cant from "+ source_table+" where lemma='be' and document_id=? and sentence_id=? and hc_start=? and token_num between hc_start-5 and hc_start+5 "
		,(row['document_id'],row['sentence_id'],row['hc_start']))	
		for row1 in c1:
			if row1['cant']>0:
				c2.execute("select count(*) cant from "+ source_table+" where document_id=? and sentence_id=? and hc_start=? and pos='VBN' and token_num between hc_start-5 and hc_start+5"
				,(row['document_id'],row['sentence_id'],row['hc_start']))				
				for row2 in c2:
					if row2['cant']>0:
						c3.execute("update "+source_table+" set passive_voice='Y' where document_id=? and sentence_id=? and hc_start=?",
						(row['document_id'],row['sentence_id'],row['hc_start']))

c3.close()
c2.close()	
c1.close()					
c.close()
conn.commit()