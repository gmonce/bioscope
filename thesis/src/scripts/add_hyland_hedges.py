# -*- coding: utf-8 -*- 
# Agrega una columna a la tabla bioscope_train y test para indicar si alguna de las palabras corresponde
# a los hedges que me pasó Ken Hyland
# este valor será incorporado como atributo al aprendizaje
# Uso: python add_hyland_hedges.py working_dir

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

try:
	c.execute('alter table bioscope_train add is_hyland_hedge string')
except sqlite3.OperationalError:
	pass
try:
	c.execute('alter table bioscope_test add is_hyland_hedge string')
except sqlite3.OperationalError:
	pass

#conn.commit


c.execute('update bioscope_train set is_hyland_hedge=\'N\'')
c.execute('update bioscope_test set is_hyland_hedge=\'N\'')
conn.commit()


hyland_hedges=['about','almost','apparent','apparently','appear','appeared','appears','approximately','around','assume','assumed','certain amount',
'certain extent','certain level','claim','claimed','could','doubt','doubtful','essentially','estimate','estimated','feel','felt','frequently','from our perspective',
'generally','guess','in general','in most cases','in most instances','in our view','indicate','indicated','largely','likely','mainly','may',
'maybe','might','mostly','often','on the whole','ought','perhaps','plausible','plausibly','possible','possibly','postulate','postulated','presumable',
'probable','probably','relatively','roughly','seems','should','sometimes','somewhat','suggest','suggested','suppose','suspect','tend to','tends to',
'typical','typically','uncertain','uncertainly','unclear','unclearly','unlikely','usually','would','broadly','tended to','presumably','suggests',
'from this perspective','from my perspective','in my view','in this view','in our opinion','in my opinon','to my knowledge','fairly','quite','rather x',
'argue','argues','argued','claims','feels','indicates','supposed','supposes','suspects','postulates']

for hh in [x for x in hyland_hedges if len(x.split( ))<3]:
	
	hh_words=hh.split(' ')
	if len(hh_words)==1:
		c.execute('update bioscope_train set is_hyland_hedge=\'Y\' where word=?',[hh_words[0]])
		c.execute('update bioscope_test set is_hyland_hedge=\'Y\' where word=?',[hh_words[0]])
	if len(hh_words)==2:
		# bioscope_train
		for tab in ['bioscope_train','bioscope_test']:
			c.execute('select * from '+tab+' b1 \
			where word=? and exists (select * from '+tab+' b2 where b2.document_id=b1.document_id \
			and b2.sentence_id=b1.sentence_id and b2.token_num=b1.token_num+1 \
			and b2.word=?)',[hh_words[0],hh_words[1]])
			for row in c:
				c1.execute('update '+tab+' set is_hyland_hedge=\'Y\'where document_id=? and sentence_id=? and token_num=?',
				[row['document_id'],row['sentence_id'],row['token_num']])
			c.execute('select * from '+tab+' b1 \
			where word=? and exists (select * from '+tab+' b2 where b2.document_id=b1.document_id \
			and b2.sentence_id=b1.sentence_id and b2.token_num=b1.token_num-1 \
			and b2.word=?)',[hh_words[1],hh_words[0]])
			for row in c:
				c1.execute('update '+tab+' set is_hyland_hedge=\'Y\'where document_id=? and sentence_id=? and token_num=?',
				[row['document_id'],row['sentence_id'],row['token_num']])

conn.commit()


		
