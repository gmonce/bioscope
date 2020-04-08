# -*- coding: utf-8 -*- 

# Script que muestra el resultado del análisis de una oración
# python analizar_oracion.py document_id sentence_id hc_token

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import sys
import sqlite3
import random


dbname=sys.argv[1]
document_id=sys.argv[1]
sentence_id=sys.argv[2]

working_dir=os.path.expandvars('$BIOSCOPE')		
script_name=os.path.join(working_dir,'bioscope.db')
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()




print "<HEAD><meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" ></head>"
print "<HTML>"
print "<b>"
print "Documento:"+document_id+"<br>"
print "Oración:"+sentence_id+"<br>"

# Muestro el tipo de oración
c.execute('select sentence_type from bioscope where document_id=? and sentence_id=? order by token_num',[document_id,sentence_id])
for row in c:
	sentence_type=row['sentence_type']
	break
print "Tipo de oracion: "+sentence_type+" <br>"
print "</b>"

# Muestro la tabla de atributos
print '<a href=\"'+working_dir+'/bioscope_train/attributes/'+document_id+'.'+sentence_id+'.html\">Tabla de atributos</a><br>'

# Muestro el árbol de análisis
print '<a href=\"'+working_dir+'/bioscope_train/img/'+document_id+'.'+sentence_id+'.svg\">Árbol de análisis</a><br>'



# Muestro el texto de la oración
print "<table border=2><tr><td>"
c.execute('select * from bioscope where document_id=? and sentence_id=? order by token_num',[document_id,sentence_id])
for row in c:
	#print "<td>"+row['word']+"</td><td>"
	if row['hedge_cue']<>'O':
		print '<b>'+row['word']+'</b>'
	else:
		print row['word']+ ' '
print "</td></tr></table>"
	


# Muestro las hedge cues
print "Hedge cues"
c.execute('select * from bioscope where document_id=? and sentence_id=? order by token_num',[document_id,sentence_id])
print "<table border=1><tr>"
for row in c:
	if row['hedge_cue']<>'O' or row['guessed_hedge_cue']<>'O':
		print "<tr>"
		print "<td>"+str(row['token_num'])+" "+row['word']+" "+row['hedge_cue']+" "+row['guessed_hedge_cue']+"</td></tr>"

		# Muestro el scope original de la hedge cue
		print "<tr><td><b>Scope original:</b>"
		if sentence_type=='TRAIN': 
			c1.execute('select * from bioscope80_scope where document_id=? and sentence_id=? and hc_token=? order by token_num',                             			[document_id,sentence_id,row['word']])
		else:
			c1.execute('select * from bioscope20_scope where document_id=? and sentence_id=? and hc_token=? order by token_num',                             			[document_id,sentence_id,row['word']])
		in_scope=False
		for row1 in c1:
			if (row1['scope']=='F') or (row1['scope']=='O' and in_scope) or (row1['scope']=='L'):
				if row1['scope']=='F':
					in_scope=True
				elif row1['scope']=='L':	
					in_scope=False
				if row1['hedge_cue']<>'O':
					print "<font color=\"red\">"+row1['word']+"</font> "
				else:
					print row1['word']
		print "</td></tr>"

	if sentence_type=='TEST':
		c1.execute('select * from bioscope20_ghc_scope where document_id=? and sentence_id=? and hc_token=? order by token_num',                             		[document_id,sentence_id,row['word']])

		print "<tr><td><b>Scope con la hedge cue aprendida:</b>"
		in_scope=False
		for row1 in c1:
			if (row1['scope']=='F') or (row1['scope']=='O' and in_scope) or (row1['scope']=='L'):
				if row1['scope']=='F':
					in_scope=True
				elif row1['scope']=='L':	
					in_scope=False
				if row1['guessed_hedge_cue']<>'O':
					print "<font color=\"red\">"+row['word']+"</font>"
				else:
					print row1['word']
		print "</td></tr>"
		
	print  "Scope aprendido"
	c.execute('select * from bioscope20_all_scopes where document_id=? and sentence_id=? and hc_token=? order by token_num',                             		[document_id,sentence_id,hc_token])
	
	print "<table><tr>"
	in_scope=False
	for row in c:
		if (row['bio_guessed_scope']<>'O'):
			if row['guessed_hedge_cue']<>'O':
				print "<td><b>"+row['word']+"</b></td><td>"
			else:
				print "<td>"+row['word']+"</td><td>"
			
	print "</tr></table>"

print "</HTML>"
