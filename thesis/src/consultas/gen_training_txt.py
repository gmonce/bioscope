# -*- coding: utf-8 -*- 
# Script que toma las oraciones de entrenamiento y genera un txt

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3
from xml.etree.ElementTree import *
from operator import itemgetter, attrgetter


def obtener_texto(tokens,start,end):
	#Devuelve un string con las palabras del array tokens entre start y end
	
	#if 'Jurkat' in [x[1] for x in tokens if (x[0]>=start and x[0]<end)]:
	#	print [x[1] for x in tokens if (x[0]>=start and x[0]<end)]
	#	print "Devuelvo:", ' '.join([x[1] for x in tokens if (x[0]>=start and x[0]<end)])+' ',"#"
	
	text=' '.join([x[1] for x in tokens if (x[0]>=start and x[0]<end)])
	if text:
		return text+' '
	else:
		return text

working_dir=os.path.expandvars('$BIOSCOPE')		
dbname=os.path.join(working_dir,'bioscope.db')
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()
c2=conn.cursor()
c3=conn.cursor() 
c4=conn.cursor()

c.execute('select document_id from bioscope_train group by document_id')
sentences=[]
for row in c:
	c1.execute('select sentence_id from bioscope_train  where document_id=? group by sentence_id order by sentence_id',(row['document_id'],))		
	for row1 in c1:
	
		# Armo una lista con las palabras y sus posiciones
		c4.execute('select token_num,word from bioscope_train  where document_id=? and sentence_id=? order by token_num',(row['document_id'],row1['sentence_id']))
		tokens=c4.fetchall()
		sentence_text=obtener_texto(tokens,1,10000)			
		sentences.append(sentence_text)

for s in sentences:
	print s
