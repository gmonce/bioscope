# -*- coding: utf-8 -*- 
# Uso: python cons_scope_rel.py $BIOSCOPE tabla
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

# Inicializo el diccionario de hedge cues
hc_list=dict([])


# Consulto todas las oraciones de la tabla que me digan

c.execute("select document_id,sentence_id,hc_start,hc_token,pos,hc_parent_pos,hc_gparent_pos,hc_ggparent_pos, passive_voice from "+table+" where token_num=hc_start group by document_id,sentence_id,hc_start")
for row in c:


	hc_token=row['hc_token']
	hc_parent_pos=row['hc_parent_pos']
	hc_gparent_pos=row['hc_gparent_pos']
	hc_ggparent_pos=row['hc_ggparent_pos']
	pos=row['pos']	
	sentence_id=row['sentence_id']
	passive_voice=row['passive_voice']
	#route=hc_ggparent_pos+"/"+hc_gparent_pos+"/"+hc_parent_pos+"/"+pos+"/"+passive_voice
	route=pos
	
	
	
	# Veo si se adivinó
	if table=='bioscope20_scope':
		c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>guessed_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
		for row1 in c1:
			if row1['cant']==0:
				guessed='Y'
			else:
				guessed='N'
	else:
		guessed='N/A'

	if hc_token not in hc_list:
		hc_list[hc_token]=dict([])
	
	if route not in hc_list[hc_token]:
		hc_list[hc_token][route]=[0,0,0,0,[],[],0,0,[],0]
		
	if guessed=='Y':
		hc_list[hc_token][route][4].append(sentence_id) 		
		hc_list[hc_token][route][6]+=1		
	elif guessed=='N':
		hc_list[hc_token][route][7]+=1		
		hc_list[hc_token][route][5].append(sentence_id) 			
	else:
		hc_list[hc_token][route][4].append(sentence_id) 			
		
	
	found=False
	# Veo si coincide el scope con el padre
	c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_hc_parent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
	for row1 in c1:
		if row1['cant']==0:
			hc_list[hc_token][route][0]+=1
			found=True
		
	# Veo si coincide el scope con el abuelo
	if not found:
		c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_hc_gparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
		for row1 in c1:
			if row1['cant']==0:
				hc_list[hc_token][route][1]+=1			
				found=True

	# Veo si coincide el scope con el bisabuelo
	if not found:
		c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_hc_ggparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
		for row1 in c1:
			if row1['cant']==0:
				hc_list[hc_token][route][2]+=1
				found=True
	
	# Veo si coincide con el scope del tatarabuelo
	# hc_list[hc_token][route][9]
	if not found:
		c1.execute("select count(*) cant from "+table+" where document_id=? and sentence_id=? and hc_start=? and scope<>in_hc_gggparent_scope",(row['document_id'],row['sentence_Id'],row['hc_start']))
		for row1 in c1:
			if row1['cant']==0:
				hc_list[hc_token][route][9]+=1
				found=True
	

	if not found:
		hc_list[hc_token][route][3]+=1	
		hc_list[hc_token][route][8].append(sentence_id) 			
		
	

# Muestro los resultados
for (hedge_cue,routes) in hc_list.iteritems():
	for (route,value) in routes.iteritems():

		guessed_sentences=''
		cant_ejemplos=0
		for v in value[4]:
			guessed_sentences+=" "+v
			cant_ejemplos+=1
			if cant_ejemplos>4:
				break

		not_guessed_sentences=''
		cant_ejemplos=0
		for v in value[5]:
			not_guessed_sentences+=" "+v
			cant_ejemplos+=1
			if cant_ejemplos>4:
				break
				
		not_scopes=''
		cant_ejemplos=0
		for v in value[8]:
			not_scopes+=" "+v
			cant_ejemplos+=1
			if cant_ejemplos>10:
				break
				
		
		print ",".join([hedge_cue,route,str(value[0]),str(value[1]),str(value[2]),str(value[9]),str(value[3]),
		str(value[6]),str(value[7]),guessed_sentences,not_guessed_sentences,not_scopes])


