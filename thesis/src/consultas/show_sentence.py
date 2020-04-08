# -*- coding: utf-8 -*- 

# Script que muestra el resultado del análisis de una oración
# python show_sentence.py document_id sentence_id

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

print "<HEAD><meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" >"
print "<link rel=\"stylesheet\" type=\"text/css\" href=\"scripts.css\" />"
print"</head>"
print "<HTML>"

# Obtengo la lista de oraciones a mostrar, desde bioscope20_scope
if not document_id:
	c2.execute('select document_id,sentence_id from bioscope20_scope group by document_id,sentence_id')
else:
	c2.execute('select document_id,sentence_id from bioscope20_scope where document_id=? and sentence_id=? group by document_id,sentence_id',[document_id,sentence_id])

for row2 in c2:

	document_id=row2['document_id']
	sentence_id=row2['sentence_id']

	# Calculo el tipo de oración
	c.execute('select sentence_type from bioscope_train where document_id=? and sentence_id=? order by token_num',[document_id,sentence_id])
	for row in c:
		sentence_type=row['sentence_type']
		break

	print "______________________________________________________________________________<br>"	
	print "Documento:",document_id,"Oración:",sentence_id,"Tipo:", sentence_type, "<br>"

	# Muestro la tabla de atributos
	print '<a href=\"'+working_dir+'/attributes/'+document_id+'.'+sentence_id+'.html\">Tabla de atributos</a><br>'

	# Muestro el árbol de análisis
	print '<a href=\"'+working_dir+'//img/'+document_id+'.'+sentence_id+'.svg\">Árbol de análisis</a><br>'


	# Muestro el texto de la oración
	print "<table>"

	c.execute('select * from bioscope_train where document_id=? and sentence_id=? order by token_num',[document_id,sentence_id])
	s=c.fetchall()

	print "Confianza en la clasificación de la secuencia: <span class=negrita>"+str(s[0]['guessed_hc_seq_guess_confidence'])+'</span><br>'

	print "<tr>"
	for row in s:
			print '<td class="main_text">'+row['word']+'</td>'
	print "</tr>"


	# Muestro los POS
	print "<tr>"
	for row in s:
		print '<td>'+row['pos']+'</td>'
	print "</tr>"

	# Muestro los chunk
	print "<tr>"
	for row in s:
		print '<td>'+row['chunk']+'</td>'
	print "</tr>"

	# Muestro el número de token
	print "<tr>"
	for row in s:
		print '<td>'+str(row['token_num'])+'</td>'
	print "</tr>"
	
	
	# Muestro la hedge cue en negrita si la reconoció, y en rojo si no pudo reconocerla
	print "<tr>"
	for row in s:
		if row['hedge_cue']<>'O':
			if row['guessed_hedge_cue']==row['hedge_cue']:
				print '<td class="guessed_hedge_cue">'+row['word']+'</td>'
			else:
				print '<td class="not_guessed_hedge_cue">'+row['word']+'</td>'
		else:
			print '<td></td>'
	print "</tr>"


	# Muestro la confianza en la clasificación de cada token
	print "<tr>"
	for row in s:
		if row['hedge_cue']<>'O' or row['guessed_hedge_cue']<>'O':
			print '<td class=negrita>'+str(row['guessed_hc_token_guess_confidence'])+'</td>'	
		else:
			print '<td>'+str(row['guessed_hc_token_guess_confidence'])+'</td>'
	print "</tr>"
	print "</table>"

	# Ahora voy por las instancias
	# Para eso recorro la tabla BIOSCOPE20_SCOPE
	# que son las del corpus held out
	# generadas a partir de la hedge cue original

	print "Reconocimiento de scopes<br>"

	c.execute('select hc_start,hc_token from bioscope20_scope where document_id=? and sentence_id=? group by hc_start,hc_token',[document_id,sentence_id])
	for row in c:
		print "Hedge cue:"+str(row['hc_token'])+" Pos:"+str(row['hc_start'])+"<br>"
		c1.execute('select * from bioscope20_all_scopes where document_id=? and sentence_id=? and hc_start=?',[document_id,sentence_id,row['hc_start']])
		s=c1.fetchall()
		print "Confianza en el reconocimiento de la secuencia:"+str(s[0]['guessed_scope_seq_confidence'])+"<br>"
		print "POS del padre de la hedge cue:"+str(s[0]['hc_parent_pos'])+"<br>"
		print "<table>"

		# Muestro el scope original
		print "<tr>"
		for row1 in s:
			if row1['bio_scope']<>'O':
				if row1['hedge_cue']<>'O':
					print "<td class=guessed_hedge_cue>"+row1['word']+"</td>"
				else:
					print "<td>"+row1['word']+"</td>"
			else:
				print "<td>"+"</td>"
		print "</tr>"

		# Muestro el indicador de si está en el scope del padre
		print "<tr>"
		for row1 in s:
			if row1['in_hc_parent_scope']:
				print "<td>"+row1['in_hc_parent_scope']+"</td>"
			else:
				print "<td>"+"</td>"	

		print "</tr>"
		print "<tr>"
		
		# Muestro el guessed hedge scope
		for row1 in s:
			if row1['bio_guessed_scope']<>'O':
				if row1['guessed_hedge_cue']<>'O':
					print "<td class=guessed_hedge_cue>"+row1['word']+"</td>"
				else:
					print "<td>"+row1['word']+"</td>"
			else:
				print "<td>"+"</td>"
		print "</tr>"

		print "<tr>"
		for row1 in s:
			if row1['bio_guessed_scope']<>'O':
				print "<td class=negrita>"+str(row1['guessed_scope_token_confidence'])+"</td>"
			else:
				print "<td>"+str(row1['guessed_scope_token_confidence'])+"</td>"
			
		print "</tr>"

		print "</table>"



	print "</table>"

print "</HTML>"
