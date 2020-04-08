# -*- coding: utf-8 -*- 
# Script que levanta a memoria el corpus, y graba los atributos "basicos" en las tablas correspondientes

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import sqlite3

working_dir=sys.argv[1]
dbname=os.path.join(working_dir,'bioscope.db')

xml_list=[('abstracts_train.xml','bioscope_train'),('abstracts_test.xml','bioscope_test')]

for (bioscope_xml_file,table_name) in xml_list:
	# Levanto el corpus correspondiente
	bcp=bioscope.util.BioscopeCorpusProcessor(working_dir, bioscope_xml_file)
	bc=bioscope.BioscopeCorpus(bcp,'a8307982.*')

	# Grabo los atributos básicos en las tablas
	for (docId,d) in bc.documents.iteritems():
		print "Genero atributos para el documento ",docId	
		for (sentenceId,sentence) in d.sentences.iteritems():
			print "Oración ",sentenceId
			token_num=0
			if sentence.data_loaded:
				s_table=sentence.get_basic_attributes()
				if sentenceId=='S315.12':
					print s_table
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
					
					
					# Proceso las hedge cues, genero un máximo de tres columnas para reflejar el anidamiento
					hedge_cue=['O']*3
					i=0
					for elem in s[5]:
						hedge_cue[i]=elem
						i=i+1
						if i==3:
							break
							
					if hedge_cue[0] != 'O':
						hc=hedge_cue[0]
					elif hedge_cue[1] != 'O':
						hc=hedge_cue[1]
					elif hedge_cue[2] != 'O':
						hc=hedge_cue[2]
					else:
						hc='O'	
					  
					
					# Proceso las marcas de scope
					# Genero un máximo de 3 columnas. Si no tienen nada, les pongo O
					hedge_scope=['O']*3
					i=0
					for elem in s[7]:
						hedge_scope[i]=elem
						i=i+1
						if i==3:
							break
					
					#print docId, sentenceId,token_num, s[0]
					#c.execute("""insert into """+table_name+""" (document_id,sentence_id,token_num,word,lemma,POS,CHUNK,NER,hedge_cue,hedge_cue1, 							hedge_cue2, hedge_cue3,hedge_scope1,hedge_scope2,hedge_scope3) 
					#values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",		(docId,sentenceId,token_num,s[0],s[1],s[2],s[3],s[4],hc,hedge_cue[0],hedge_cue[1],
					#hedge_cue[2],hedge_scope[0],hedge_scope[1],hedge_scope[2]))
