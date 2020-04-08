# -*- coding: utf-8 -*- 
# Script que lee un archivo en formato conll y le modifica la últimas columna, asumiendo que tiene un scope en formato 
# Para eso aplica las reglas de morante2009 y lo pasa a formato bio
# al final hay un valor /num que indica la confianza
# También asume que el campo -2 es la hedge cue (esto lo usa para que los scopes siempre incluyan a la hedge cue)
# Las líneas que comienzan en numeral se mantienen, porque indican la confianza del clasificador en los valores asignados a la secuencia
# Uso: scope_postprocess.py source_file target_file

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
from string import *

source_filename=sys.argv[1]
target_filename=sys.argv[2]

script_name=os.path.join(sys.path[0],sys.argv[0])


t0=time.clock()
print script_name," Postprocessing file...", source_filename
#pln_inco.bioscope.scripts.postprocess_scope_learning_results(evaluation_file,target_file)



# Reglas de morante
def apply_morante2009_rules(sentence):

	"""
	# Asume las siguientes posiciones 
	-1: la clase
	14: in_nextS_scope
	13: pos del bisabuelo
	12: pos del abuelo
	11: pos del padre
	10: lemma
	9: pos
	8: scope del bisabuelo
	7: scope del abuelo
	6: scope del padre
	5: passive voice
	4: scope_hc
	"""	

	hay_scope=False
	total_F=0
	total_L=0
	token_pos=0
	hc_pos=0
	F_already_occurred=False
	hc_already_occurred=False
	first_L_after_F=-1
	first_L_after_hc=-1
	first_F=-1
	first_L=-1
	X_pos=-1
	Y_pos=-1
	#Z_pos=-1
	
	hc_parent_scope_start=-1
	hc_gparent_scope_start=-1
	hc_ggparent_scope_start=-1
	
	hc_parent_scope_end=-1
	hc_gparent_scope_end=-1
	hc_ggparent_scope_end=-1
	
	hay_nexts=False
	
	
	
	#print sentence[0][1], sentence[0][3]
	

	
	for token in sentence:

		# Atributos globales a la oración
		hc_ggparent_pos=token[8]
		hc_gparent_pos=token[7]
		hc_parent_pos=token[6]
		
		
		
	
	
		if token[-1]=='F': 
			#if sentence[0][1]=='S116.7':
			#	print "Hay una F en la posición... ", token

			F_already_occurred=True
			total_F=total_F+1
			if total_F==1:
				first_F=token_pos
		elif token[-1]=='L': 
			total_L=total_L+1
			if total_L==1:
				first_L=token_pos
			if F_already_occurred and first_L_after_F <0 :
				first_L_after_F=token_pos
			if hc_already_occurred and first_L_after_hc <0:
				first_L_after_hc=token_pos
		elif token[-1]=='X':
			# Caso especial, dos a la izquierda está el hc_parent_scope
			X_pos=token_pos
			
		elif token[-1]=='Y':
			# Caso especial, tres a la izquierda está el hc_gparent_scope
			Y_pos=token_pos
			
		if token[2]==sentence[0][3]:
			hc_already_occurred=True
			hc_pos=token_pos
			pos_hc=token[9]
		
		if token[11]=='L':
			hc_parent_scope_end=token_pos
		elif token[11]=='F':
			hc_parent_scope_start=token_pos		
		
		if token[12]=='L':
			hc_gparent_scope_end=token_pos		
		elif token[12]=='F':
			hc_gparent_scope_start=token_pos		
			
		
		if token[13]=='L':
			hc_ggparent_scope_end=token_pos		
		elif token[13]=='F':
			hc_ggparent_scope_start=token_pos		
			
		if token[14]=='L':
			nexts_scope_end=token_pos		
		elif token[14]=='F':
			nexts_scope_start=token_pos
			hay_nexts=True
			
			
		token_pos=token_pos+1

	if total_F>0 or total_L>0 or hc_pos>0:
		hay_scope=True
		
	# Aplico directamente las reglas de morante2009:
	# 1. Si hay un F y un L, el scope es todo lo que hay entre F y L, OK
	if total_F==1 and total_L==1:
		first=first_F
		last=first_L
		
		
	# 2. Si hay F pero no L, entonces solo queda el que marcó como F,OK
	if total_F>=1 and total_L==0:
		first=first_F
		last=first_F
	
	
	# 3. Si hay L sin F, se arranca en la hedge cue, y se termina en la L
	# Modifico la regla: si el L coincide con el fin del scope del abuelo, toma el scope del abuelo

		
	if total_F==0 and total_L==1:
		if token[6]=='ADJP' and token[7]=='VP' and hc_ggparent_scope_end==first_L:
			first=hc_ggparent_scope_start
		# Si hay voz pasiva, elijo preferentemente al bisabuelo en vez de al abuelo			
		elif pos_hc=='VBN' and hc_ggparent_scope_end==first_L:
			first=hc_ggparent_scope_start		
		elif hc_gparent_scope_end==first_L:
			first=hc_gparent_scope_start
		elif hc_parent_scope_end==first_L:
			first=hc_parent_scope_start
		elif hc_ggparent_scope_end==first_L:
			first=hc_ggparent_scope_start
		else:
			first=hc_pos
		last=first_L
	
	
	
	#if total_F==0 and total_L==1:
	#	first=hc_pos
	#	last=first_L
	
	
	
	# 4. Si hay un F y más de una L, entonces empieza en F y termina en el primer L después del F (si hay uno)
	if total_F==1 and total_L>1:
		first=first_F
		if first_L_after_F >=0:
			last=first_L_after_F
		else:
			last=first
	# 5. Si hay más de un F y un sólo L, entonces arrancamos en la hedge signal y terminamos en el L
	if total_F>1 and total_L==1:
		first=hc_pos
		last=first_L
	
	
	# 6. Si no hay first y hay varios last, entonces arrancamos en la hedge signal y terminamos en el primer L después de ella
	if total_F==0 and total_L>1:
		first=hc_pos
		if first_L_after_hc >=0:
			last=first_L_after_hc
		else:
			last=first
	# 7. No hay nada, pero hay cue,  en ese caso pongo como scope la hc_pos (esto no aparecía en MOrante)
	if total_F==0 and total_L==0 and hc_pos>0:
		first=hc_pos
		last=first
	
	# 8. Hay mas de un F y más de un L (esto no aparecía en Morante2009)
	# Tomamos la primera F y la primera L
	if total_F>1 and total_L>1:
		first=first_F
		last=first_L
		

	# Finalmente, si había una X, entonces la F es la posición de la X, y la L es el fin del scope del parent
	if X_pos<>-1 and hc_parent_scope_end<>-1:
		first=X_pos
		last=hc_parent_scope_end
		

	# Finalmente, si había una Y, entonces la F es la posición de la Y, y la L es el fin del scope del gparent
	if Y_pos<>-1 and hc_gparent_scope_end<>-1:
		first=Y_pos
		last=hc_gparent_scope_end



	# Reglas de procesamiento finales
	# Si es un MD en voz pasiva, coincido con la S cercana, si existe
	# Regla x1

	"""
	if pos_hc=='MD' and token[5]=='Y' and hc_gparent_pos in ('S','SBAR'):
		print sentence[0][1],":Regla MD y voz pasiva, con abuelo"
		first=hc_gparent_scope_start
		last=hc_gparent_scope_end
	elif pos_hc=='MD' and token[5]=='Y' and hc_ggparent_pos in ('S','SBAR'):
		print sentence[0][1], ":Regla MD y voz pasiva, con bisabuelo"
		first=hc_ggparent_scope_start
		last=hc_ggparent_scope_end
	"""
	# Agregada en la corrida 35, sustituye a lo anterior	
	if pos_hc=='MD' and token[5]=='Y' and hay_nexts:
		print sentence[0][1],":Regla MD"
		first=nexts_scope_start
		last=nexts_scope_end
	
		
	# Regla x2
	# Si es un verbo en voz pasiva, entonces toma la S más cercana si existe

	"""
	if pos_hc=='VBN' and sentence[hc_pos-1][10]=='be' and hc_gparent_pos in ('S','SBAR'):
		print sentence[0][1],":Regla VBN y voz pasiva, con abuelo"
		first=hc_gparent_scope_start
		last=hc_gparent_scope_end
	elif pos_hc=='VBN' and sentence[hc_pos-1][10]=='be' and hc_ggparent_pos in ('S','SBAR'):
		print sentence[0][1], ":Regla VBN y voz pasiva, con bisabuelo"
		first=hc_ggparent_scope_start
		last=hc_ggparent_scope_end
	"""
	# Agregada en la corrida 35, sustituye a lo anterior
	if pos_hc=='VBN' and sentence[hc_pos-1][10]=='be' and hay_nexts:
		print sentence[0][1],":Regla VBN" 
		first=nexts_scope_start
		last=nexts_scope_end
		
		
	# Regla x3: si a la izquierda del scope hay un which, lo incluyo
	# Agregado en la corrida 36
	if sentence[0][1]=='S686.2':
		print "Oración con which"
		print first
		print sentence[first-1][9]
	if sentence[first-1][10] == 'which' and token[5]=='Y':
		print sentence[0][1],":Regla Which" 
		first=first-1
		print "Nuevo first:",first
	
	
	
	# Finalmente, si había una Z, entonces la F es la posición de la Z, y la L es el fin del scope del ggparent
	# Esto lo sacamos porque no funcionó
	#if Z_pos<>-1 and hc_ggparent_scope_end<>-1:
	#	first=Z_pos
	#	last=hc_ggparent_scope_end


	# Regla que debería sustituir a las anteriores: si la F coincide con el comienzo de un constituyente, entonces la L es el fin del constituyente
	# No funcionó<z
	"""
	if first==hc_parent_scope_start:
		last=hc_parent_scope_end
	elif first==hc_gparent_scope_start:
		last=hc_gparent_scope_end	
	elif first==hc_ggparent_scope_start:
		last=hc_ggparent_scope_end	
	
	"""

	# Veo si hay alguna hedge cue fuera del scope, en ese caso, ajusto el scope para que las incluya
	# Esto no estaba incluido en las reglas de morante
	token_pos=0
	for token in sentence:
		#print token
		if token[4]<>'O':
			if token_pos<first:
				first=token_pos
			if token_pos>last:
				last=token_pos
		token_pos+=1
	
	if sentence[0][1]=='S686.2':
		print "devuelvo:",(first,last)
	
	return (hay_scope,first,last)
# Fin Reglas de morante	
	

source=open(source_filename,'r')
target=open(target_filename,'w+')
	
sentence=[]
confidences=[]

for line in source:
	#Cargo toda una oración
	if line.startswith('#'):
		target.write(line)
	elif line != '\n':
		attributes=split(line.rstrip(),'\t')
		if '/' in attributes[-1]:		
			(tag,confidence)=attributes[-1].split('/')
			attributes[-1]=tag
			confidences.append(confidence)
		sentence.append(attributes)
	else:
		(hay_scope, first,last)=apply_morante2009_rules(sentence)
			
		# Si no hay scope, me aseguro de que ponga todo O
		if not hay_scope:
			first=10000
				
		# Por las dudas, corrijo
		if last<first:
			last=first
			
		#print 'Reconocí la oración ',sentence
		# Proceso la oración y voy modificando los campos, pasando a formato BIO y ajustando el scope
		pos=0
		while pos<len(sentence):
			# Ajusto scope original
			if pos < first:
				sentence[pos][-1]='O'
			elif pos==first:
				sentence[pos][-1]='F'
			elif pos>=first and pos<last:
				sentence[pos][-1]='O'
			elif pos==last:
				sentence[pos][-1]='L'			
			else:
				sentence[pos][-1]='O'
			
			
			# Escribo el token en el destino
			content=''
			for t in sentence[pos]:
				content+=t
				content+='\t'
			content=rstrip(content,'\t')
			if confidences:			
				content+='/'+confidences[pos]
			target.write(rstrip(content,'\t')+'\n')
			pos=pos+1		
		# Dejo espacio en 
		sentence=[]
		confidences=[]
		target.write('\n')

source.close()
target.close()	
print script_name,":Done (Elapsed time:", time.clock()-t0,"seconds)"	
