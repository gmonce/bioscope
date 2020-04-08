# -*- coding: utf-8 -*- 
# Uso: python cons_scopes_simple.py $BIOSCOPE tabla
# Script que mira las oraciones en el corpus de entrenamiento y se fija si coincide con el scope de algún constituyente del aŕbol sintáctico

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3

working_dir=sys.argv[1]
table=sys.argv[2]
dbname=os.path.join(working_dir,'bioscope.db')
script_name=os.path.join(sys.path[0],sys.argv[0])


t0=time.clock()
# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()
err=conn.cursor()

# Inicializo el diccionario de hedge cues
hc_list=dict([])

#Consulto todas las oraciones con error
err.execute("select document_id,sentence_id,hc_start from "+ table+" where scope<>guessed_scope group by document_id,sentence_id,hc_start")
for e in err:

	c.execute("select document_id,sentence_id,hc_start,hc_token,pos,hc_parent_pos,hc_gparent_pos,hc_ggparent_pos, passive_voice from "+table+" where document_id=? and sentence_id=? and hc_start=? and token_num=hc_start", [e['document_id'],e['sentence_id'], e['hc_start']])
	for row in c:
		hc_token=row['hc_token']
		pos=row['pos']	
		sentence_id=row['sentence_id']
		route=pos

		#if hc_token not in hc_list:
		#	hc_list[hc_token]=dict([])
		
		#if route not in hc_list[hc_token]:
		#	hc_list[hc_token][route]=[0,0,0,0,[],[],0,0,[],0]
			
	
		found=False
		# Veo si coincide el scope con el padre
		c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_hc_parent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
		for row1 in c1:
			if row1['cant']==0:
				#hc_list[hc_token][route][0]+=1
				coincidence='P'
				found=True
			
		# Veo si coincide el scope con el abuelo
		if not found:
			c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_hc_gparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
			for row1 in c1:
				if row1['cant']==0:
					#hc_list[hc_token][route][1]+=1			
					coincidence='GP'
					found=True

		# Veo si coincide el scope con el bisabuelo
		if not found:
			c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_hc_ggparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
			for row1 in c1:
				if row1['cant']==0:
					#hc_list[hc_token][route][2]+=1
					coincidence='GGP'
					found=True
		
		# Veo si coincide con el scope del tatarabuelo
		if not found:
			c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_hc_gggparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
			for row1 in c1:
				if row1['cant']==0:
					#hc_list[hc_token][route][9]+=1
					coincidence='GGGP'
					found=True
		# Veo si coincide con algun scope de mas arriba
		if not found:
			c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_nextS_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
			for row1 in c1:
				if row1['cant']==0:
					coincidence='OTHER'
					found=True	

		# No coincide con ninguno
		if not found:
			coincidence='NONE'
	

		# Veo ahora si lo guessed coincide con alguno
		found=False
		# Veo si coincide el scope con el padre
		c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and guessed_scope<>in_hc_parent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
		for row1 in c1:
			if row1['cant']==0:
				#hc_list[hc_token][route][0]+=1
				gcoincidence='P'
				found=True
			
		# Veo si coincide el scope con el abuelo
		if not found:
			c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and guessed_scope<>in_hc_gparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
			for row1 in c1:
				if row1['cant']==0:
					#hc_list[hc_token][route][1]+=1			
					gcoincidence='GP'
					found=True

		# Veo si coincide el scope con el bisabuelo
		if not found:
			c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and guessed_scope<>in_hc_ggparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
			for row1 in c1:
				if row1['cant']==0:
					#hc_list[hc_token][route][2]+=1
					gcoincidence='GGP'
					found=True
		
		# Veo si coincide con el scope del tatarabuelo
		if not found:
			c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and guessed_scope<>in_hc_gggparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
			for row1 in c1:
				if row1['cant']==0:
					#hc_list[hc_token][route][9]+=1
					gcoincidence='GGGP'
					found=True

		# Veo si coincide con algun scope de mas arriba
		if not found:
			c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and guessed_scope<>in_nextS_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
			for row1 in c1:
				if row1['cant']==0:
					gcoincidence='OTHER'
					found=True	

		# No coincide con ninguno
		if not found:
			gcoincidence='NONE'


		# Obtengo el texto del scope predicho 
		# Primero obtengo el comienzo
		c1.execute("select token_num from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope='F'",(row['document_id'],row['sentence_id'], row['hc_start']))
		first=None
		for row1 in c1:
			first=row1['token_num']
		last=None
		# Obtengo el final 
		c1.execute("select token_num from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope='L'",(row['document_id'],row['sentence_id'], row['hc_start']))
		for row1 in c1:
			last=row1['token_num']

		# Obtengo el texto 
		if first and last:
			c1.execute("select word from "+table+" where document_id=? and sentence_id=? and hc_start=? and token_num between ? and ?",(row['document_id'],row['sentence_id'], row['hc_start'],first,last))
			texto=""
			for row1 in c1:
				texto+=row1['word']
				texto+=" "
			texto=texto[0:len(texto)-1]
		else:
			texto="None"
			
		# Obtengo el texto del scope original
		# Primero obtengo el comienzo
		first=None
		c1.execute("select token_num from "+table+" where document_id=? and sentence_id=? and hc_start=? and guessed_scope='F'",(row['document_id'],row['sentence_id'], row['hc_start']))
		for row1 in c1:
			first=row1['token_num']
		# Obtengo el final 
		last=None
		c1.execute("select token_num from "+table+" where document_id=? and sentence_id=? and hc_start=? and guessed_scope='L'",(row['document_id'],row['sentence_id'], row['hc_start']))
		for row1 in c1:
			last=row1['token_num']

		# Obtengo el texto 
		if first and last:
			c1.execute("select word from "+table+" where document_id=? and sentence_id=? and hc_start=? and token_num between ? and ?",(row['document_id'],row['sentence_id'], row['hc_start'],first,last))
			gtexto=""
			for row1 in c1:
				gtexto+=row1['word']
				gtexto+=" "
			gtexto=gtexto[0:len(gtexto)-1]
		else:
			gtexto="None"

		# Muestro los resultados
		print "#".join([sentence_id,str(e['hc_start']),hc_token,route,coincidence, gcoincidence,texto,gtexto])
