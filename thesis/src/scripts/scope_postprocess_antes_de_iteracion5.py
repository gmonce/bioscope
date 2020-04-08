# -*- coding: utf-8 -*- 
# Script que lee un archivo en formato conll y le modifica la últimas columna, asumiendo que tiene un scope en formato 
# Para eso aplica las reglas de morante2009 y lo pasa a formato bio
# al final hay un valor /num que indica la confianza
# Las l�neas que comienzan en numeral se mantienen, porque indican la confianza del clasificador en los valores asignados a la secuencia
# Uso: scope_postprocess.py source_file target_file runx

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
from string import *

source_filename=sys.argv[1]
target_filename=sys.argv[2]
runx=int(sys.argv[3])
script_name=os.path.join(sys.path[0],sys.argv[0])


t0=time.clock()
print script_name," Postprocessing file...", source_filename
#pln_inco.bioscope.scripts.postprocess_scope_learning_results(evaluation_file,target_file)



# Reglas de morante
def apply_morante2009_rules(sentence):

	"""
	# Asume las siguientes posiciones 
	-1: la clase
	15: in_nexts_scope (opcional)
	14: in_ggparent_scope (opcional)
	13: in_gparent_scope (opcional)
	12: in_parent_scope (opcional)
	11: pos del bisabuelo (opcional)
	10: pos del abuelo (opcional)
	9: pos del padre (opcional)
	8: passive voice (opcional)	
	7: lemma
	6: pos 	
	5: word
	4: scope_hc
	3: hc_start
	2: token_num
	1: sentence_id
	0: document
	"""	

	hay_scope=False
	total_F=0
	total_L=0
	token_pos=0
	hc_pos=-1
	F_already_occurred=False
	hc_already_occurred=False
	first_L_after_F=-1
	first_L_after_hc=-1
	first_F=-1
	first_L=-1
	
	if runx>=16:
		X_pos=-1
		Y_pos=-1
	
		hc_parent_scope_start=-1
		hc_gparent_scope_start=-1
		hc_ggparent_scope_start=-1

		hc_parent_scope_end=-1
		hc_gparent_scope_end=-1
		hc_ggparent_scope_end=-1

		hay_nexts=False
	
	#print sentence[0][1], sentence[0][3]
	for token in sentence:
		token_num=token[2]
		hc_start=token[3]
			
		# Atributos globales a la oraci�n
		if runx >= 16:
			hc_ggparent_scope=token[14]
			hc_gparent_scope=token[13]
			hc_parent_scope=token[12]
			passive_voice=token[8]
			nexts_scope=token[15]
			hc_parent_pos=token[9]
			hc_gparent_pos=token[10]
			hc_ggparent_pos=token[11]
	
		if token[-1]=='F': 
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
		elif runx>=16 and token[-1]=='X':
			# Caso especial para las reglas X
			X_pos=token_pos
			
		elif runx>16 and token[-1]=='Y':
			# Caso especial para las reglas Y
			Y_pos=token_pos
			
		if token_num==hc_start:
			hc_already_occurred=True
			hc_pos=token_pos
			POS_hc=token[6]
			lemma_hc=token[7]
		
		if runx >=16:
			if hc_parent_scope=='L':
				hc_parent_scope_end=token_pos
			elif hc_parent_scope=='F':
				hc_parent_scope_start=token_pos		
			
		if runx>=20:
			if hc_gparent_scope=='L':
				hc_gparent_scope_end=token_pos		
			elif hc_gparent_scope=='F':
				hc_gparent_scope_start=token_pos		
				
			
			if hc_ggparent_scope=='L':
				hc_ggparent_scope_end=token_pos		
			elif hc_ggparent_scope=='F':
				hc_ggparent_scope_start=token_pos		
				
			if nexts_scope=='L':
				nexts_scope_end=token_pos		
			elif nexts_scope=='F':
				nexts_scope_start=token_pos
				hay_nexts=True
			
			
		token_pos=token_pos+1


	print "TotalF:",total_F," TotalL:",total_L, " Hc pos:",hc_pos, " hc start:",hc_start, " hc_parent_scope_start:", hc_parent_scope_start, " hc_parent_scope_end:", hc_parent_scope_end, " x pos:",X_pos
	if X_pos==-1 and  Y_pos==-1:
		if not (total_F==1 and total_L==1):
			print "Incorrecta"
			

	if total_F>0 or total_L>0 or hc_pos>=0:
		hay_scope=True


	# Aplico directamente las reglas de morante2009:
	# 1. Si hay un F y un L, el scope es todo lo que hay entre F y L, OK
	if total_F==1 and total_L==1:
		first=first_F
		last=first_L
		
		
	# 2. Si hay F pero no L, entonces solo queda el que marc� como F,OK
	if total_F>=1 and total_L==0:
		first=first_F
		last=first_F
	
	
	# 3. Si hay L sin F, se arranca en la hedge cue, y se termina en la L (Morante)
	# Si hay scopes, postproceso un poco m�s
	if total_F==0 and total_L==1:
		# Regla original de Morante
		first=hc_pos
		last=first_L
	
	
	# 4. Si hay un F y más de una L, entonces empieza en F y termina en el primer L después del F (si hay uno)
	# Lo cambiamos en la corrida 40: utiliza el next scope S si puede, antes
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
	
	
	# 6. Si no hay first y hay varios last, entonces arrancamos en la hedge signal y 
	# terminamos en el primer L después de ella (Morante)
	# Si hay scopes, utiliza el nexts_scope
	if total_F==0 and total_L>1:
		# Morante
		first=hc_pos
		if first_L_after_hc >=0:
			last=first_L_after_hc
		else:
			last=first

	# 7. No hay nada, pero hay cue,  en ese caso pongo como scope la hc_pos (esto no aparecía en MOrante)
	# Si hay scopes, hago más cosas
	if total_F==0 and total_L==0 and hc_pos>=0:
		# Morante
		first=hc_pos
		last=hc_pos
			
	
	# 8. Hay mas de un F y más de un L (esto no aparecía en Morante2009)
	# Tomamos la primera F y la primera L
	if total_F>1 and total_L>1:
		first=first_F
		last=first_L

		

	# Regla que sobreescribe a las anteriores
	# Si hay next S, entonces lo usa
	# Sino, usa el parent
	# Regla 9, que sobreescribe a todas las otras para los casos en los que no pudo adivinar bien
	if not (total_F==1 and total_L==1):
		if runx>45 and hay_nexts:
			first=nexts_scope_start
			last=nexts_scope_end
		elif runx>45:
			first=hc_parent_scope_start
			last=hc_parent_scope_end
		
	
		

	# Si hab�a una X, entonces la F es la posici�n de la X, y la L es el fin del scope del parent
	if runx>=16 and X_pos<>-1 and hc_parent_scope_end<>-1:
		first=X_pos
		last=hc_parent_scope_end
		

	# Si hab�a una Y, entonces la F es la posici�n de la Y, y la L es el fin del scope del gparent
	if runx>=20 and Y_pos<>-1 and hc_gparent_scope_end<>-1:
		#print "Modifico porque hay Y en la oraci�n ",sentence[0][1]
		first=Y_pos
		last=hc_gparent_scope_end
		
	# Si detect� X e Y, entonces usa el nexts
	if runx>45 and X_pos<>-1 and Y_pos<>-1 and hay_nexts:
		first=nexts_scope_start
		last=nexts_scope_end
	

	# Reglas de procesamiento finales
	# Si es un MD en voz pasiva, coincido con la S cercana, si existe
	# Regla x1

	"""
	if scope_rules and pos_hc=='MD' and passive_voice=='Y' and hc_gparent_pos in ('S','SBAR'):
		print sentence[0][1],":Regla MD y voz pasiva, con abuelo"
		first=hc_gparent_scope_start
		last=hc_gparent_scope_end
	elif scope_rules and pos_hc=='MD' and passive_voice=='Y' and hc_ggparent_pos in ('S','SBAR'):
		print sentence[0][1], ":Regla MD y voz pasiva, con bisabuelo"
		first=hc_ggparent_scope_start
		last=hc_ggparent_scope_end
	"""
	# Agregada en la corrida 35, sustituye a lo anterior	
	"""
	if runx> 45 and pos_hc=='MD' and passive_voice=='Y' and hay_nexts:
		#print sentence[0][1],":Regla MD"
		#print "Start:",nexts_scope_start
		#print "End:",nexts_scope_end
		first=nexts_scope_start
		last=nexts_scope_end
	"""
		
	# Regla x2
	# Si es un verbo en voz pasiva, entonces toma la S más cercana si existe

	"""
	if scope_rules and pos_hc=='VBN' and sentence[hc_pos-1][7]=='be' and hc_gparent_pos in ('S','SBAR'):
		print sentence[0][1],":Regla VBN y voz pasiva, con abuelo"
		first=hc_gparent_scope_start
		last=hc_gparent_scope_end
	elif scope_rules and pos_hc=='VBN' and sentence[hc_pos-1][7]=='be' and hc_ggparent_pos in ('S','SBAR'):
		print sentence[0][1], ":Regla VBN y voz pasiva, con bisabuelo"
		first=hc_ggparent_scope_start
		last=hc_ggparent_scope_end

	# Agregada en la corrida 35, sustituye a lo anterior
	if scope_rules and pos_hc=='VBN' and sentence[hc_pos-1][7]=='be' and hay_nexts:
		print sentence[0][1],":Regla VBN" 
		first=nexts_scope_start
		last=nexts_scope_end
		
		
	# Regla x3: si a la izquierda del scope hay un which, lo incluyo
	# Agregado en la corrida 36
	if scope_rules and sentence[first-1][7] == 'which' and passive_voice=='Y':
		print sentence[0][1],":Regla Which" 
		first=first-1

	
	# Regla x4: si es is likely/JJ, entonces tomo el enclosing S
	# Agregado en la corrida 38
	# Para corregir errores S461.5 y S467.7
	if scope_rules and pos_hc=='JJ' and lemma_hc=='likely' and (sentence[hc_pos-1][7]=='be' or sentence[hc_pos-2][7]=='be') and hay_nexts:
		print sentence[0][1],":regla likely"
		first=nexts_scope_start
		last=nexts_scope_end
		
	
	# Regla x5: agregada en la corrida 40, elimina las referencias al final de un scope
	# Para esto, tiene que terminar en un paréntesis y tener largo mayor a 8
	# Heurístico heurístico
	
	if sentence[last][7]==')':
		print "Regla referencia 2"
	
		# Busco el parentesis que abre
		i=last-1
		opening=-1
		while i>=first:
			if sentence[i][7]=='(':
				opening=i
				break
			i=i-1

		if opening<>-1 and last-opening>8:
			last=opening-1
		
	
	# Finalmente, si había una Z, entonces la F es la posición de la Z, y la L es el fin del scope del ggparent
	# Esto lo sacamos porque no funcionó
	#if scope_rules and Z_pos<>-1 and hc_ggparent_scope_end<>-1:
	#	first=Z_pos
	#	last=hc_ggparent_scope_end
	"""

	# Regla que debería sustituir a las anteriores: si la F coincide con el comienzo de un constituyente, entonces la L es el fin del constituyente
	# No funcionó<z

	"""
	if scope_rules and first==hc_parent_scope_start:
		last=hc_parent_scope_end
	elif scope_rules and first==hc_gparent_scope_start:
		last=hc_gparent_scope_end	
	elif scope_rules and first==hc_ggparent_scope_start:
		last=hc_ggparent_scope_end	
	
	"""

	# Veo si hay alguna hedge cue fuera del scope, en ese caso, ajusto el scope para que las incluya
	# Esto no estaba incluido en las reglas de morante
	# Lo modifico en la corrida 41 para que use el nexts_scope
	token_pos=0
	hay_problema=False
	for token in sentence:
		#print token
		if token[4]<>'O':
			if token_pos<first:
				first=token_pos
				hay_problema=True
			if token_pos>last:
				last=token_pos
				hay_problema=True
		token_pos+=1
	
	# Si hay nexts enotnces lo uso
	if runx> 45 and hay_problema and hay_nexts:
		first=min([first,nexts_scope_start])
		last=max([last,nexts_scope_end])
	
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
		print sentence[0][1]
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
