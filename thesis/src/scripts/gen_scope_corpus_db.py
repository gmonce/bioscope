# -*- coding: utf-8 -*- 
# Script que toma la tabla base de entrenamiento (bioscope80) y genera las instancias de entrenamiento para el scope (bioscope80_scope)
# Hace lo mismo con bioscope20
# Si le pasamos el parámetro total en Y, entonces genera los scopes para todas las instancias del corpus de entrenamiento #(bioscope_train_scope), y del corpus de evaluación (bioscope_test_scope). Para el corpus de evaluación también crea instancias utilizando 
# las guessed hedge cues
# Uso: gen_scope_corpus.py {BIOSCOPE | BIOSCOPED} TOTAL

import pln_inco.bioscope.scope_rules
import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
import sqlite3


def generate_scope_analysis_table(dbname,source_table,sentence_type, target_table):
	"""
	Toma una tabla, recorre las oraciones y por scope diferente que encuenta,
	genera una instancia de entrenamiento con la oración y la identificación del HC 
	(además de los atributos que ya tenía y que me pueden servir para la clasificación). 
	Digamos, entonces que usamos bioscope_train con tipo de oración "TRAIN" o "TEST" y generamos
	Bioscope80_scope y bioscope20_scope, respectivamente
	Para el scope utiliza el scope original
	Convierte el scope al formato FOL
	@arg dbname: nombre del archivo que tiene la base de datos
	@type dbname:C{string}
	@arg source_table: nombre de la tabla origen (bioscope80)
	@type source_table:C{string}
	@arg sentence_type: indica el string que deben tener las instancias en el campo SENTENCE_TYPE
	@type sentence_type: C{string}
	@arg target_table: nombre de la tabla destino (bioscope80_scope)
	@type target_table:C{string}
	@arg use_guessed_hedge_cue: indica si utilizar la hedge cue aprendida en lugar de la original al generar los atributos, por defecto es False
	@type C{Boolean}
	"""

	#Conexión a la base de datos
	t0=time.clock()
	conn= sqlite3.connect(dbname)	
	conn.text_factory = str
	conn.row_factory=sqlite3.Row
	c=conn.cursor()
	c2=conn.cursor()
	c3=conn.cursor()
	c4=conn.cursor()

	# Dropeo la tabla destino y la creo de nuevo, igual a la origen, vacía
	try:
		c.execute('drop table '+target_table)
	except sqlite3.OperationalError:
		print "No pude borrar ",target_table
		pass

	# Armo la lista de columnas que voy a copiar de la tabla origen
	columnas='document_id,sentence_id,token_num,word,lemma,POS,chunk,ner'
	interrogantes='?,?,?,?,?,?,?,?'
	

	# Creo una tabla igual a la origen, vacía
	c.execute('create table '+target_table+' as select '+columnas+' from '+source_table+' where 0=1')

	conn.commit()

	# Agrego el diferenciador de instancia, la columna para la hc, y la columna para el scope
	c.execute('alter table '+target_table+' add column hc_start integer');
	c.execute('alter table '+target_table+' add column hc_token string');
	c.execute('alter table '+target_table+' add column scope string');
	c.execute('alter table '+target_table+' add column scope_hc string');
	c.execute('alter table '+target_table+' add column guessed_scope string');


	conn.commit;

	c.execute('create unique index ipk_'+target_table+ ' on '+target_table +' (document_id,sentence_id,token_num,hc_start)')

	conn.commit()

	
	# Recorro oración por oración y voy insertando
	# Antes armo la lista de columnas y signos de interrogación
	# Lo tenía automático, pero prefiero hacerlo a mano para controlar las columnas 
	# para las que quiero generar instancias para entrenar los scopes
	# Agrego las columnas de la tabla destino
	columnas+=',scope_hc,scope,hc_start,hc_token'
	interrogantes+=',?,?,?,?'	

	"""
	c.execute('select * from '+source_table+ ' limit 1')
	columnas=''
	interrogantes=''
	row=c.fetchone()
	cant_columnas=len(row.keys())+6

	for k in row.keys():
		columnas+=','+k
		interrogantes+=',?'
	columnas+=',scope_hc,scope,hc_start,hc_token'

	columnas=columnas.lstrip(',')
	"""
	
	# Ahora sí recorro e inserto
	if sentence_type=='ALL':
		c.execute('select document_id,sentence_id from '+ source_table+' group by document_id,sentence_id')
	else:
		#print "Estoy procesando el caso del held out..."
		#print 'select document_id,sentence_id from '+ source_table+' where sentence_type=\''+ sentence_type +  '\' group by document_id,sentence_id'
		c.execute('select document_id,sentence_id,count(*) cantidad from '+ source_table+' where sentence_type=? group by document_id,sentence_id',(sentence_type,))
	


	for sentence in c:
		# Recorro los diferentes scopes que existen
		for scope_number in ['1','2','3']:
			# Primero obtengo el número de scopes diferentes al mismo nivel
			c2.execute('select count(*) cantidad from '+source_table+
			' where document_id=? and sentence_id=? and hedge_scope'+scope_number+'=\'B-SPECXCOPE\'', 
			(sentence['document_id'],sentence['sentence_id']))		
			for row in c2:
				cantidad_hedges=row['cantidad']
			
			for cant in range(1,cantidad_hedges+1):
				c2.execute('select * from '+ source_table+' where document_id=? and sentence_id=? order by token_num ',
				(sentence['document_id'],sentence['sentence_id']))		
				valores_a_insertar=[]

				in_scope=False
				hedged=False
				hedge_token=''
				valores=[]
				numero_de_hedge=0


				for row in c2:
					# Guardo lo último que inserté, porque voy a tener que cambiar cuando termine el scope para poner la L
					valores=[]

					# Copio las columnas originales
					valores.append(row['document_id'])
					valores.append(row['sentence_id'])
					valores.append(row['token_num'])
					valores.append(row['word'])
					valores.append(row['lemma'])
					valores.append(row['pos'])
					valores.append(row['chunk'])
					valores.append(row['ner'])
					
					#for k in row.keys():	
					#	valores.append(row[k])

					# Marco el scope

					if row['hedge_scope'+scope_number]=='B-SPECXCOPE':
						# Contemplo el caso en el que hay dos scopes pegados
						if in_scope:
							print "Scope pegado:",row['sentence_id']
							# Modifico el último valor insertado, correspondía L
							valores_anterior[-1]='L'
							valores_a_insertar[-1]=valores_anterior
						# Solo lo considero comienzo si es el hedge correspondiente a la iteración, sino lo ignoro
						numero_de_hedge+=1
						if numero_de_hedge==cant:
							xcope='F'
							in_scope=True
							hedged=True
						else:
							xcope='O'
							in_scope=False
					elif row['hedge_scope'+scope_number]=='I-SPECXCOPE':
						xcope='O'
						if numero_de_hedge==cant:
							in_scope=True
						else:
							in_scope=False
					elif row['hedge_scope'+scope_number]=='O' and in_scope:
						# Modifico el último valor insertado, correspondía L
						valores_anterior[-1]='L'
						valores_a_insertar[-1]=valores_anterior
						xcope='O'
						in_scope=False
					else:
						xcope='O'
						in_scope=False


					# Marco si es el hedge cue del scope que estoy generando, solamente si estoy dentro del scope
					if in_scope:
						scope_hc=row['hedge_cue'+scope_number]
					else:
						scope_hc='O'
					valores.append(scope_hc)

					valores.append(xcope)

					# Actualizo la marca de hedge
					if in_scope:
						if row['hedge_cue'+scope_number] <> 'O':
							if hedge_token<>'':
								hedge_token=hedge_token+'_'+row['word']
							else:
								hedge_token=row['word']
								hedge_pos=row['token_num']

					# Agrego los valores a una lista, para insertar al final
					valores_a_insertar.append(valores)
					valores_anterior=valores

				# Si cuando termina todavía no se cerró el scope
				# tengo que cerrarlo
				if in_scope:
					valores_anterior[-1]='L'
					valores_a_insertar[-1]=valores_anterior

				# Cuando finalizo la recorrida, actualizo la hedge_pos y el hedge_token e inserto en la tabla destino
				if hedged:
					for valores in valores_a_insertar:
						# Agrego la columna hc_start
						valores.append(hedge_pos)
						# Agrego la columna hc_token
						valores.append(hedge_token)
						#print columnas
						#print valores
						#print 'insert into '+ target_table+' ('+ columnas+') values ('+ interrogantes+')',valores
						c3.execute('insert into '+ target_table+' ('+ columnas+') values ('+ interrogantes+')',valores)

									
				
	conn.commit()
			


def generate_scope_analysis_table_ghc(dbname,source_table,sentence_type,target_table):
	"""
	Toma una tabla con las palabras y por cada hedge cue que haya adviniado, genera una instancia
	de la oración, donde se intentará adivinar el scope 
	Digamos, entonces que usamos bioscope_train con tipo de oración "TEST" y generamos bioscope20_ghc_scope
	@arg dbname: nombre del archivo que tiene la base de datos
	@type dbname:C{string}
	@arg source_table: nombre de la tabla origen (bioscope80)
	@type source_table:C{string}
	@arg sentence_type: indica el string que deben tener las instancias en el campo SENTENCE_TYPE (solo tiene sentido si has_instances=False
	@type sentence_type: C{string}
	@arg target_table: nombre de la tabla destino (bioscope80_scope)
	@type target_table:C{string}
	"""

	#Conexión a la base de datos
	t0=time.clock()
	conn= sqlite3.connect(dbname)	
	conn.text_factory = str
	conn.row_factory=sqlite3.Row
	c=conn.cursor()
	c1=conn.cursor()
	c2=conn.cursor()
	c3=conn.cursor()
	

	# Dropeo la tabla destino y la creo de nuevo, igual a la origen, vacía
	try:
		c.execute('drop table '+target_table)
	except sqlite3.OperationalError:
		pass

	# Armo la lista de columnas que voy a copiar de la tabla origen
	columnas='document_id,sentence_id,token_num,word,lemma,POS,chunk,ner'
	interrogantes='?,?,?,?,?,?,?,?'
	

	# Creo una tabla igual a la origen, vacía
	c.execute('create table '+target_table+' as select '+columnas+' from '+source_table+' where 0=1')

	conn.commit()

	# Agrego el diferenciador de instancia, la columna para la hc, y la columna para el scope
	c.execute('alter table '+target_table+' add column hc_start integer');
	c.execute('alter table '+target_table+' add column scope_hc string');
	c.execute('alter table '+target_table+' add column guessed_scope string');
	c.execute('alter table '+target_table+' add column hc_token string');

	conn.commit;

	c.execute('create unique index ipk_'+target_table+ ' on '+target_table +' (document_id,sentence_id,token_num,hc_start)')

	conn.commit()

	
	# Recorro oración por oración y voy insertando
	# Antes armo la lista de columnas y signos de interrogación
	# Lo tenía automático, pero prefiero hacerlo a mano para controlar las columnas 
	# para las que quiero generar instancias para entrenar los scopes
	# Agrego las columnas de la tabla destino
	columnas+=',scope_hc,hc_start'
	interrogantes+=',?,?'	

	# Ahora sí recorro e inserto
	if sentence_type=='ALL':
		c.execute('select document_id,sentence_id from '+ source_table+' group by document_id,sentence_id')
	else:
		c.execute('select document_id,sentence_id from '+ source_table+' where sentence_type=? group by document_id,sentence_id',(sentence_type,))
	
	for sentence in c:
		# Obtengo las distintas hedge cues adivinadas para la oración
		c1.execute('select * from '+source_table+' where document_id=? and sentence_id=? and guessed_hedge_cue=\'B-SPECCUE\'',(sentence['document_id'],sentence['sentence_id']))
		for row1 in c1:
			# Por cada hedge cue, inserto una instancia de la oración en la tabla destino
			c2.execute('select * from '+ source_table+' where document_id=? and sentence_id=? order by token_num ',
			(sentence['document_id'],sentence['sentence_id']))
			in_hedge_cue=False
			for row2 in c2:
				valores=[]

				# Simplemente copio el token
				# La hedge cue la pongo solamente si es la que estoy procesando
				if row2['token_num']<row1['token_num']:
					scope_hc='O'
				elif row2['token_num']==row1['token_num']:
					scope_hc=row2['guessed_hedge_cue']
					hc_token=row2['word']
					in_hedge_cue=True
				elif row2['guessed_hedge_cue']  in ('I-SPECCUE','D-SPECCUE') and in_hedge_cue:
					scope_hc=row2['guessed_hedge_cue']
					hc_token=hc_token+'_'+row2['word']
				elif row2['guessed_hedge_cue']=='B-SPECCUE' and in_hedge_cue:
					scope_hc='O'
					in_hedge_cue=False
				else:
					scope_hc='O'

				valores.append(row2['document_id'])
				valores.append(row2['sentence_id'])
				valores.append(row2['token_num'])
				valores.append(row2['word'])
				valores.append(row2['lemma'])
				valores.append(row2['pos'])
				valores.append(row2['chunk'])
				valores.append(row2['ner'])
				valores.append(scope_hc)
				valores.append(row1['token_num'])
				
				#print columnas
				#print valores
				c3.execute('insert into '+ target_table+' ('+ columnas+') values ('+ interrogantes+')',valores)
			# Después de que termino, actualizo el valor de hc_token
			c3.execute('update '+target_table+' set hc_token=? where document_id=? and sentence_id=? and hc_start=?',
			(hc_token,sentence['document_id'],sentence['sentence_id'],row1['token_num']))
			
	conn.commit()




working_dir=sys.argv[1]
dbname=os.path.join(working_dir,'bioscope.db')
script_name=os.path.join(sys.path[0],sys.argv[0])

if len(sys.argv)>2:
	total=sys.argv[2]
else:
	total='N'


t0=time.clock()
print script_name,t0," Generating scope learning instances..."

if total=='Y':
	generate_scope_analysis_table(dbname,'bioscope_train','ALL','bioscope_train_scope')
else:
	generate_scope_analysis_table(dbname,'bioscope_train','TRAIN','bioscope80_scope')

print script_name,time.clock(),":Done (Elapsed time:", time.clock()-t0,"seconds)"


print script_name,"Generating scope testing instances..."
t0=time.clock()
if total=='Y':
	generate_scope_analysis_table(dbname,'bioscope_test','ALL','bioscope_test_scope')
else:
	generate_scope_analysis_table(dbname,'bioscope_train','TEST','bioscope20_scope')

print script_name+":Done (Elapsed time:", time.clock()-t0,"seconds)" 


print script_name,"Generating scope testing instances, using guessed hedge cue..."
if total=='Y':
	generate_scope_analysis_table_ghc(dbname,'bioscope_test','ALL','bioscope_test_ghc_scope')
else:
	generate_scope_analysis_table_ghc(dbname,'bioscope_train','TEST','bioscope20_ghc_scope')

print script_name+":Done (Elapsed time:", time.clock()-t0,"seconds)" 




