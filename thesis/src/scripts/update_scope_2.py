# -*- coding: utf-8 -*- 
# Script que actualiza el valor de scope_2, que es igual que scope, pero si el scope coincide
# con el alcance del padre, entonces en vez de F vale 
# Esto se va a usar en el postprocesamiento para no usar la F calculada, sino simplemente poner la F del scope del padre
# python update_scope_2.py {$BIOSCOPE | $BIOSCOPED} RUN TOTAL


import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import sqlite3
from sys import *


working_dir=sys.argv[1]
runx=int(sys.argv[2])

if len(sys.argv)>3:
	total=sys.argv[3]
else:
	total='N'



dbname=os.path.join(working_dir,'bioscope.db')
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()


if total=='N':
	table_list=['bioscope80_scope']
else:
	table_list=['bioscope_train_scope']


for source_table in table_list:
	c.execute('update '+source_table+' set scope_2=scope')


# Actualizo el scope para el parent
for source_table in table_list:
	c.execute('select document_id,sentence_id,hc_start from '+ source_table+' s where not exists (select * from '+ source_table+' s1 where s1.document_id=s.document_id and s1.sentence_id=s.sentence_id and s1.hc_start=s.hc_start and scope<>in_hc_parent_scope) group by document_id,sentence_id,hc_start')
	for row in c:
		c1.execute("update "+source_table+" set scope_2='X' where document_id=? and sentence_id=? and hc_start=? and scope='F'",(row['document_id'],row['sentence_id'],row['hc_start']))
		
# Actualizo el scope para el grandparent
if runx>16:
	for source_table in table_list:
		c.execute('select document_id,sentence_id,hc_start from '+ source_table+' s where not exists (select * from '+ source_table+' s1 where s1.document_id=s.document_id and s1.sentence_id=s.sentence_id and s1.hc_start=s.hc_start and scope<>in_hc_gparent_scope) group by document_id,sentence_id,hc_start')
		for row in c:
			c1.execute("update "+source_table+" set scope_2='Y' where document_id=? and sentence_id=? and hc_start=? and scope='F'",(row['document_id'],row['sentence_id'],row['hc_start']))

# Actualizo el scope para el nextS
#for source_table in table_list:
#	c.execute('select document_id,sentence_id,hc_start from '+ source_table+' s where not exists (select * from '+ source_table+' s1 where s1.document_id=s.document_id and s1.sentence_id=s.sentence_id and s1.hc_start=s.hc_start and scope<>in_nexts_scope) group by document_id,sentence_id,hc_start')
#	for row in c:
#		c1.execute("update "+source_table+" set scope_2='W' where document_id=? and sentence_id=? and hc_start=? and scope='F' and scope_2 not in ('X','Y')",(row['document_id'],row['sentence_id'],row['hc_start']))



# Actualizo el scope para el grandparent
# Lo sacamos porque no mejoró la performance.
#for source_table in table_list:
#	c.execute('select document_id,sentence_id,hc_start from '+ source_table+' s where not exists (select * from '+ source_table+' s1 where s1.document_id=s.document_id and s1.sentence_id=s.sentence_id and s1.hc_start=s.hc_start and scope<>in_hc_ggparent_scope) group by document_id,sentence_id,hc_start')
#	for row in c:
#		c1.execute("update "+source_table+" set scope_2='Z' where document_id=? and sentence_id=? and hc_start=? and scope='F'",(row['document_id'],row['sentence_id'],row['hc_start']))
	
c1.close()					
c.close()
conn.commit()
