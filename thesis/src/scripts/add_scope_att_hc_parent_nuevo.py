# -*- coding: utf-8 -*- 
# Script que levanta a memoria el corpus, y agrega en las tablas los atributos relacionados con el padre de la hedge cue
# python add_scope_att_hc_parent_db.py {$BIOSCOPE | $BIOSCOPED} TOTAL
# Ojo que hay cosas comentadas.

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

if total=='Y':
	xml_file_list=['abstracts_test.xml','abstracts_train.xml']
else:
	xml_file_list=['abstracts_train.xml']


for bioscope_xml_file in xml_file_list:

	print "Proceso archivo...",bioscope_xml_file
	bcp=bioscope.util.BioscopeCorpusProcessor(working_dir, bioscope_xml_file)
	#bc=bioscope.BioscopeCorpus(bcp,'a1989880.*')
	bc=bioscope.BioscopeCorpus(bcp,'.*')


	conn= sqlite3.connect(dbname)	
	conn.text_factory = str

	# Grabo los atributos básicos en las tablas
	c=conn.cursor()
	c1=conn.cursor()

	for (docId,d) in bc.documents.iteritems():
			print "Actualizo los scopes para el documento... ",docId	
			for (sentenceId,sentence) in d.sentences.iteritems():
				token_num=0
				if sentence.data_loaded:
					print "Proceso oracion:",sentenceId
					s_table=sentence.get_basic_attributes()
					for s in s_table[1:]:
						token_num=token_num+1
						#s[0]=word
						#s[1]=lemma
						#s[2]=POS
						#s[3]=Chunk
						#s[4]=NER
						#s[5]= lista de HEDGE_CUES
						#s[6]= lista de NEG_CUES
						#s[7]= lista de SPEC_XCOPES
					
					
						# Si es el primer token de una spec cue, entonces obtengo el POS de su abuelo
						if 'B-SPECCUE' in s[5]:
							#print "SentenceId:",sentenceId
							#print "docId:",docId
							#print "Token:", token_num
							#print "Word:", s[0]
							#print "Hedge_cues:", s[5]
							#print "Scopes:", s[7]

							hc_start=token_num						
						
							# Obtengo el número de token del padre
							(gp,gp_treepos)=sentence.get_leaf_grandparent(token_num-1,2)
							gp_pos=gp.node
							#print gp_treepos
							

							# Abuelo
							(gpp,gpp_treepos)=sentence.get_leaf_grandparent(token_num-1,3)
							gpp_pos=gpp.node

							#Bisabuelo
							if gpp_pos=='ROOT':
								gppp_pos='NONE'
							else:
								(gppp,gppp_treepos)=sentence.get_leaf_grandparent(token_num-1,4)
								gppp_pos=gppp.node
								
							#print "GPPP_POS:",gppp_pos

							# Tatarabuelo
							if gppp_pos in ('ROOT','NONE'):
								gpppp_pos='NONE'
							else:
								(gpppp,gpppp_treepos)=sentence.get_leaf_grandparent(token_num-1,5)
								gpppp_pos=gpppp.node
							
							#print "GPPP_POS:",gpppp_pos
							
							
							# Obtengo el siguiente scope S
							# Desde la corrida 41 está modificado para que cumpla con ciertas reglas
							# Dependiendo de la hedge cue
							
							hc_pos=s[2]
							hc_lemma=s[1]
							nextS_treepos=None
							

							# Obtengo los siguientes S,NP,VP
							if gp_pos in ('S','SBAR'):
								nextS=gp_treepos
							elif gpp_pos in ('S','SBAR'):
								nextS=gpp_treepos
							elif gppp_pos in ('S','SBAR'):
								nextS=gppp_treepos							
							elif gpppp_pos in ('S','SBAR'):
								nextS=gpppp_treepos														
							else:
								nextS=None


							if gp_pos=='NP':
								nextNP=gp_treepos
							elif gpp_pos=='NP':
								nextNP=gpp_treepos
							elif gppp_pos=='NP':
								nextNP=gppp_treepos							
							elif gpppp_pos=='NP':
								nextNP=gpppp_treepos														
							else:
								nextNP=None
							
							if gp_pos=='VP':
								nextVP=gp_treepos
							elif gpp_pos=='VP':
								nextVP=gpp_treepos
							elif gppp_pos=='VP':
								nextVP=gppp_treepos							
							elif gpppp_pos=='VP':
								nextVP=gpppp_treepos														
							else:
								nextVP=None

							
							# Si es un adverbio o adjetivo, marco lo que sea primero, un NP o un S #Verificado
							"""
							if hc_pos in ('RB','JJ'):
								if nextNP:
									if nextS:
										if len(nextNP)<len(nextS):
											nextS_treepos=nextNP
										else:
											nextS_treepos=nextS											
									else:
										nextS_treepos=nextNP
								else:
									nextS_treepos=nextS
							
							# Si es un verbo, excepto participio pasado, entonces uso el VP
							if hc_pos.startswith('VB') and hc_pos<>'VBN': #Verificado
								nextS_treepos=nextVP
								
							# Si es un MD, usa el nextVP	#Verificado
							if hc_pos=='MD':
								nextS_treepos=nextVP
							"""
							
							"""
							# Si es or, either, neither, utiliza el NP # Verificado
							if hc_lemma in ('or','either','neither'):
								nextS_treepos=nextNP
							"""
								
							
							# Si no lo asignó, usa el nextS
							if not nextS_treepos:
								nextS_treepos=nextS


							#print sentence.get_leaf_grandparent(token_num-1)[0].leaves()
							#print "Posiciones:", gp_pos,gpp_pos,gppp_pos

							# Obtengo los índices de los tokens del alcance del padre
							#print "Obtengo scope del padre:"
							(start,end)=sentence.get_node_hedge_scope(gp_treepos,hc_start-1)
							#print "Scope final para el padre:",(start,end)

							#print "Obtengo scope del abuelo:"							
							(startp,endp)=sentence.get_node_hedge_scope(gpp_treepos,hc_start-1)							
							
							
							if gppp_pos=='NONE':
								(startpp,endpp)=(startp,endp)
							else:
								#print "Obtengo scope del bisabuelo:"
								(startpp,endpp)=sentence.get_node_hedge_scope(gppp_treepos,hc_start-1)														
						
							if gpppp_pos=='NONE':
								(startppp,endppp)=(startpp,endpp)
							else:
								(startppp,endppp)=sentence.get_node_hedge_scope(gpppp_treepos,hc_start-1)														
								
							#print (start,end), (startp,endp), (startpp,endpp), (startppp,endppp)


							if nextS_treepos:
								(start_nextS,end_nextS)=sentence.get_node_hedge_scope(nextS_treepos,hc_start-1)
								

							# Actualizo
							if bioscope_xml_file=='abstracts_train.xml':
								if total=='N':
									table_list=['bioscope80_scope','bioscope20_scope','bioscope20_ghc_scope']
								else:
									table_list=['bioscope_train_scope']
							else:
								table_list=['bioscope_test_scope','bioscope_test_ghc_scope']
							
							#print >> stderr, "table _list :",table_list
					
							for table_name in table_list:
						
								# Marco el parent POS, y pongo el scope en O							
								c1.execute("update "+ table_name + 
								"  set hc_parent_POS=?, hc_gparent_pos=?, hc_ggparent_pos=?, hc_gggparent_pos=?, in_hc_parent_scope='O',in_hc_gparent_scope='O', \
								in_hc_ggparent_scope='O', in_nextS_scope='O', in_hc_gggparent_scope='O' where document_id=? and sentence_id=? and hc_start=?",
								(gp_pos,gpp_pos,gppp_pos,gpppp_pos, docId,sentenceId,token_num))
								
								# Marco el comienzo del parent scope
								c1.execute("update "+ table_name + " set in_hc_parent_scope='F' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
								(docId,sentenceId,token_num,start+1))
								
								# Marco el fin del parent scope
								c1.execute("update "+table_name+"  set in_hc_parent_scope='L' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
								(docId,sentenceId,token_num,end+1))

								# Marco el comienzo del grandparent scope
								c1.execute("update "+ table_name + " set in_hc_gparent_scope='F' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
								(docId,sentenceId,token_num,startp+1))
								
								# Marco el fin del grandparent scope
								c1.execute("update "+table_name+"  set in_hc_gparent_scope='L' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
								(docId,sentenceId,token_num,endp+1))

								# Marco el comienzo del ggrandparent scope
								c1.execute("update "+ table_name + " set in_hc_ggparent_scope='F' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
								(docId,sentenceId,token_num,startpp+1))
								
								# Marco el fin del ggrandparent scope
								c1.execute("update "+table_name+"  set in_hc_ggparent_scope='L' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
								(docId,sentenceId,token_num,endpp+1))
								
								# Marco el comienzo del gggrandparent scope
								c1.execute("update "+ table_name + " set in_hc_gggparent_scope='F' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
								(docId,sentenceId,token_num,startppp+1))
								
								# Marco el fin del gggrandparent scope
								c1.execute("update "+table_name+"  set in_hc_gggparent_scope='L' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
								(docId,sentenceId,token_num,endppp+1))


								# Marco el comienzo del nextS_scope
								if nextS_treepos:
									c1.execute("update "+ table_name + " set in_nextS_scope='F' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
									(docId,sentenceId,token_num,start_nextS+1))

									# Marco el fin del nextS_scope
									c1.execute("update "+table_name+"  set in_nextS_scope='L' where document_id=? and sentence_id=? and hc_start=? and token_num=?", 
									(docId,sentenceId,token_num,end_nextS+1))
								
								

	c.close()
	c1.close()
	conn.commit()
	
