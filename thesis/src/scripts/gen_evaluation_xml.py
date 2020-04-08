#-*- coding: utf-8 -*- 
# Script que toma las oraciones de evaluación y genera el xml correspondiente a partir de los valores en las tablas
# evaluation_type vale HELDOUT o TOTAL. En el  primer caso, utiliza el corpus heldout de evaluación, en el segundo usa el corpus de evaluación directamente
# hc_type vale HC_ORIGINAL o HC_GUESSED
# scope_type value SCOPE_ORIGINAL o SCOPE_GUESSED
# xml_file es el archivo que se va a generar

# Utilizado luego para la evaluación
# Uso: python gen_evaluation_xml.py dbname evaluation_type hc_type scope_type xml_file
# python gen_evaluation_xml.py $BIOSCOPE/bioscope.db HELDOUT HC_ORIGINAL SCOPE_GUESSED temp.xml

import pln_inco.bioscope.scope_rules
import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
reload(sys)
import yaml
import sqlite3
import xml.etree.ElementTree
#from xml.etree.ElementTree import *
from operator import itemgetter, attrgetter


sys.setdefaultencoding('latin1')

def get_all_scopes(instances_table_name,scope_table_name,scope_column, document_id,sentence_id):
	# Recorro la tabla donde están los scopes, y genero un array con los valores. Cada elemento del array tiene: una secuencia (start,end) que indica
	# el scope, y una lista [h1,...] con las posiciones de las hedge cues dentro del scope
	c2.execute("select distinct hc_start from "+scope_table_name+" where document_id=? and sentence_id=?", (document_id,sentence_id))
	scopes=[]
	for row2 in c2:
		c3.execute("select * from "+scope_table_name+"  where document_id=? and sentence_id=? and hc_start=? order by token_num", (row['document_id'],row1['sentence_id'],row2['hc_start']))	
		start=0
		end=0
		hc_list=[]

		for row3 in c3:
			
			if row3[scope_column]=='F':
				start=row3['token_num']
				in_scope=True
			elif row3[scope_column]=='L':
				end=row3['token_num']
				in_scope=False


			if row3['scope_hc']=='B-SPECCUE':
				hc_list.append([row3['token_num'],row3['token_num']])
			elif row3['scope_hc']=='I-SPECCUE':
				hc_list[-1][1]=row3['token_num']
			elif row3['scope_hc']=='D-SPECCUE':
				hc_list.append([row3['token_num'],row3['token_num']])
					
		if end==0:
			end=start
		
		# Si no hay scope, no tiene sentido que haya hedge cue
		if end!=0 or start!=0:
			scopes.append((start,end,hc_list))
		
	if debug:
		print "Scopes:", sorted(scopes, key=itemgetter(0))
	return sorted(scopes, key=itemgetter(0))


def find_external_scopes(scopes):
	# Dada una lista de scpes en forma (start,end, hedge_cue_list)
	# Devuelve los externos (es decir, que no son incluido por ninguno de los otros
	# En la forma (start,end,hedge_cue_list, included_scopes)

	external_scopes=[]
	#Numero los scopes
	i=0
	new_scopes=[]
	while i<len(scopes):
		new_scopes.append([scopes[i][0],scopes[i][1],scopes[i][2],i])
		i+=1
	scopes=new_scopes
	#print "Nuevos scopes:", scopes
	
	# Si encuentro scopes que se solapan, entonces los achico a todos para que solamente incluyan sus hedge cues
	solapados=False
	for (start,end,hedge_cue_list,scope_number) in scopes:
		for (start1,end1,hedge_cue_list1,scope_number1) in scopes:
			if scope_number<>scope_number1:
				if  (start1<>start or end1<>end):
					if (start1>=start and start1<=end and end1>end):
						#print "Encontré scopes solapados..."
						solapados=True
						break
	if solapados:
		pos_external_scopes=0
		for (start,end,hedge_cue_list,scope_number) in scopes:
			scopes[pos_external_scopes][0]=scopes[pos_external_scopes][2][0][0]
			#print "Comienzo del scope corregido ",scopes[pos_external_scopes][0]
			scopes[pos_external_scopes][1]=scopes[pos_external_scopes][2][-1][1]
			pos_external_scopes+=1

	for (start,end,hedge_cue_list,scope_number) in scopes:
		#if debug:
		#		print "Proceso el scope:",start,end,hedge_cue_list, scope_number
		is_external_hedge=True
		included_scopes=[]
		for (start1,end1,hedge_cue_list1,scope_number1) in scopes:
			if scope_number<>scope_number1:
				# Si no son iguales, y lo cubre, no es externo
				if start1<=start and end1>=end and (start1<>start or end1<>end):
					is_external_hedge=False
				# Si son iguales, elijo el primero que encontré
				elif start1==start and end1==end and scope_number1<scope_number:
					is_external_hedge=False		
				# Si lo incluye, entonces lo pongo en la lista de los incluidos	
				elif start<=start1 and end>=end1 and (start1<>start or end1<>end):
					#if debug:
				        #		print "Incluyo ", (start1,end1), " como interno"
					included_scopes.append((start1,end1,hedge_cue_list1))
				# Si son iguales, pero el scope_number es mayor, entonces lo consideró incluidos
				elif start1==start and end1==end and scope_number<scope_number1:
					included_scopes.append([start1,end1,hedge_cue_list1])
					
		if is_external_hedge:
			external_scopes.append([start,end,hedge_cue_list,included_scopes])
	
	#print "External antes del ajuste:", sorted(external_scopes, key=itemgetter(0))

	# Antes de devolver los externos
	# Verifico que los incluidos no comprendan a alguna de mis hedge cues
	# Si es así, los achico para que solamente incluyan sus hedge cues
	pos_external_scopes=0
	for (start,end,hedge_cue_list,included_scopes) in external_scopes:
		#print "Analizo:", (start,end,hedge_cue_list,included_scopes)
		for (hcstart,hcend) in hedge_cue_list:
			pos_included_scopes=0
			for (istart,iend,ihedge_cue_list) in included_scopes:
				if hcstart>=istart and hcstart<=iend:
					# Tengo que modificar los included scopes
					# Obtengo la mínima y máxima de las hedge cues
					min_hc=10000
					max_hc=0
					for (hcistart,hciend) in ihedge_cue_list:
						if hcistart<min_hc:
							min_hc=hcistart
						if hciend>max_hc:
							max_hc=hciend
					external_scopes[pos_external_scopes][3][pos_included_scopes]=[min_hc,max_hc,ihedge_cue_list]
				pos_included_scopes+=1
		pos_external_scopes+=1

	#print "External antes de ajustar los scopes:",sorted(external_scopes, key=itemgetter(0))

	# Repaso los scopes externos
	# Si alguno corta a otro scope externo posterior
	# lo reduzco para que solamente incluya su o sus hedge cues
	# Riesgo: el scope podría seguir cruzándose si hay más de una hedge cue y lo que queda se cruza con el otro
	# Espero que no suceda
	#pos_external_scopes=0
	#for (start,end,hedge_cue_list,included_scopes) in external_scopes:
	#	for (istart,iend,ihedge_cue_list,included_scopes) in external_scopes:
	#		if (istart<>start or iend<>end):
	#			if (istart>=start and istart<=end):
	#					external_scopes[pos_external_scopes][0]=external_scopes[pos_external_scopes][2][0]
	#					external_scopes[pos_external_scopes][1]=external_scopes[pos_external_scopes][2][-1]
	#					break
	#	pos_external_scopes+=1

	#print "External ajustado:",sorted(external_scopes, key=itemgetter(0))
	return sorted(external_scopes, key=itemgetter(0))
	
def obtener_texto(tokens,start,end):
	#Devuelve un string con las palabras del array tokens entre start y end
	
	#if 'Jurkat' in [x[1] for x in tokens if (x[0]>=start and x[0]<end)]:
	#	print [x[1] for x in tokens if (x[0]>=start and x[0]<end)]
	#	print "Devuelvo:", ' '.join([x[1] for x in tokens if (x[0]>=start and x[0]<end)])+' ',"#"
	
	text=' '.join([x[1] for x in tokens if (x[0]>=start and x[0]<end)])
	if text:
		return text+' '
	else:
		return text


def get_hc_tail(hc_end, next_hc, next_scope, scope_end,tokens):

	# Devuelve el texto para el tail de una hedge cue
	# Busca la siguiente hedge cue, o el primer scope incluido en el scope actual
	# O el final del scope actual
	
	#print next_hc,next_scope,scope_end+1
	tail_end=min([next_hc,next_scope,scope_end+1])
	tail=obtener_texto(tokens,hc_end+1,tail_end)
	return tail

def get_scope_text(scope_start,next_hc,next_scope,scope_end,tokens):
	text_end=min([scope_end+1,next_hc,next_scope])
	text=obtener_texto(tokens,scope_start,text_end)
	
	return text

def get_scope_tail(scope_end, next_hc, next_scope, parent_end,tokens):
	tail_end=min([next_hc,next_scope,parent_end+1])
	tail=obtener_texto(tokens,scope_end+1,tail_end)
	return tail


# Uso: python gen_evaluation_xml.py dbname evaluation_type hc_type scope_type xml_file
dbname=sys.argv[1]
evaluation_type=sys.argv[2]
hc_type=sys.argv[3]
scope_type=sys.argv[4]
xml_file=sys.argv[5]


if evaluation_type=='HELDOUT':
	instances_table_name='bioscope_train'
	sentence_type='TEST'

	if hc_type=='HC_ORIGINAL':
		scope_table_name='bioscope20_scope'
	else:
		scope_table_name='bioscope20_ghc_scope'


	if scope_type=='SCOPE_ORIGINAL':
		scope_column='scope'
	else:
		scope_column='guessed_scope'
	
else:
	instances_table_name='bioscope_test'
	sentence_type='ALL'

	if hc_type=='HC_ORIGINAL':
		scope_table_name='bioscope_test_scope'
	else:
		scope_table_name='bioscope_test_ghc_scope'


	if scope_type=='SCOPE_ORIGINAL':
		scope_column='scope'
	else:
		scope_column='guessed_scope'


conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c1=conn.cursor()
c2=conn.cursor()
c3=conn.cursor() 
c4=conn.cursor()

# Primero creo el elemento raíz
docset=xml.etree.ElementTree.Element("DocumentSet")

#debug=True
#sentence_debug='S315.12'

sentence_debug=False
debug=False

# Recorro los documentos
if sentence_type=='ALL':
	if sentence_debug:
		c.execute("select document_id from "+instances_table_name+" where sentence_id='"+sentence_debug+"' group by document_id")
	else:
		c.execute("select document_id from "+instances_table_name+" group by document_id")	
else:
	#oracion
	if sentence_debug:
		c.execute("select document_id from "+instances_table_name+" where sentence_type=? and sentence_id='"+sentence_debug+"' group by document_id",(sentence_type,))
	else:
		c.execute("select document_id from "+instances_table_name+" where sentence_type=? group by document_id",(sentence_type,))
	
for row in c:
	# Creo el tag correspondiente al documento
	doc=xml.etree.ElementTree.SubElement(docset,"Document")
	doc.attrib["type"]="Biological_abstract"
	# Creo el DocID
	docid=xml.etree.ElementTree.SubElement(doc,"DocID")
	docid.attrib["type"]="PMID"
	docid.text=row["document_id"]
	# Creo el DocumentPart, que por ahora es una sola con Text
	documentpart=xml.etree.ElementTree.SubElement(doc,"DocumentPart")
	documentpart.attrib["type"]="Text"
	
	
	# Ahora recorro las oraciones del documento
	if sentence_debug:
		c1.execute("select sentence_id from "+instances_table_name+"  where document_id=? and sentence_id='"+sentence_debug+"' group by sentence_id order by sentence_id",(row['document_id'],))
	else:
		c1.execute("select sentence_id from "+instances_table_name+"  where document_id=? group by sentence_id order by sentence_id",(row['document_id'],))		

	for row1 in c1:
	
		# Creo el tag correspondiente a la oración
		#print "Oración ",row1["sentence_id"]
		sentence=xml.etree.ElementTree.SubElement(documentpart,"sentence")
		sentence.attrib["id"]=row1['sentence_id']
		
		# Armo una lista con las palabras y sus posiciones
		c4.execute("select token_num,word from "+instances_table_name+" where document_id=? and sentence_id=? order by token_num",(row['document_id'],row1['sentence_id']))
		tokens=c4.fetchall()

		# Obtengo los diferentes scopes incluidos en la oración
		# Tienen la forma (start,end,hedge_cue_list)
		scopes=get_all_scopes(instances_table_name,scope_table_name,scope_column,row['document_id'],row1['sentence_id'])
		#print "Todos los Scopes:", scopes
		# Pongo en el texto de la oración todo el texto anterior al primer scope
		if scopes:
			external_scopes=find_external_scopes(scopes)
			#print "External scopes:",external_scopes
			comienzo_scope=external_scopes[0][0]
			#print "Comienzo scope:",comienzo_scope
			sentence_text=obtener_texto(tokens,1,comienzo_scope)
		else:
			sentence_text=obtener_texto(tokens,1,10000)			
		sentence.text=sentence_text
		#print "Texto de la oracion:", sentence.text


		if scopes: 
			# Filtro los scopes externos, que es para los que voy a crear elementos
			#external_scopes=find_external_scopes(scopes)
			#print "Scopes externos:",external_scopes
			
			
			# Recorro los external scopes y los pongo como hijos de la oración
			# Primero tengo que ordenarlos, usando start
			scope_num=0
			scope_pos=0
			for (start,end,hedge_cue_list,included_scopes) in external_scopes:
				if debug:
					print "Proceso el scope externo:", start, end, hedge_cue_list
				scope_num+=1
				xcope=xml.etree.ElementTree.SubElement(sentence,"xcope")
				xcope.attrib["id"]="X"+row1['sentence_id']+"."+str(scope_num)

				external_scopes_level2=find_external_scopes(included_scopes)
				#print "External scopes de nivel 2", external_scopes_level2
				#print "Lista de hedge cues ", hedge_cue_list

				if hedge_cue_list:
					first_hc=hedge_cue_list[0][0]
				else:
					first_hc=100000
						
				if external_scopes_level2:
					first_scope=external_scopes_level2[0][0]					 
				else:
					first_scope=1000000
				
				#print "Primera hc:", first_hc
				#print "Primer scope incluido:", first_scope
				# Voy procesando las hedge cues o los included_scopes, en orden
				while hedge_cue_list or external_scopes_level2:
					if hedge_cue_list:
						next_hc=hedge_cue_list[0][0]
					else:
						next_hc=100000
					#print "Next hc:", next_hc
						
					if external_scopes_level2:
						next_scope=external_scopes_level2[0][0]					 
					else:
						next_scope=1000000
					#print "Next scope:", next_scope
						
				
					# Proceso la siguiente hedge cue
					if next_hc<next_scope:
						(hc_start,hc_end)=hedge_cue_list[0]
						del hedge_cue_list[0]
						
						if debug:
							print "Proceso la cue ",hc_start,hc_end	

						hc=xml.etree.ElementTree.SubElement(xcope,"cue")
						hc.attrib["ref"]=xcope.attrib["id"]
						hc.attrib["type"]="speculation"
						# El texto de la hedge cue es simplemente el texto entre start y end
						hc.text=obtener_texto(tokens,hc_start,hc_end+1)
						#print "Texto de la hedge cue:",hc.text
						# El tail es el texto hasta la siguiente hedge cue, hasta el siguiente scope dentro del mismo scope externo, 
						# o hasta el fin del scope
						if hedge_cue_list:
							next_hc=hedge_cue_list[0][0]
						else:
							next_hc=100000
						hc.tail=get_hc_tail(hc_end,next_hc,next_scope,end,tokens)
						#print "Tail  de la hedge cue:",hc.tail
						
					# Proceso el siguiente scope
					if next_scope<next_hc:
						start_level2,end_level2,hedge_cue_list_level2,included_scopes_level2=external_scopes_level2[0]
						del external_scopes_level2[0]
						if debug:
							print "Proceso el scope externo de nivel 2:", start_level2, end_level2, hedge_cue_list_level2, included_scopes_level2

						scope_num+=1
						xcope_level2=xml.etree.ElementTree.SubElement(xcope,"xcope")
						xcope_level2.attrib["id"]="X"+row1['sentence_id']+"."+str(scope_num)

						external_scopes_level3=find_external_scopes(included_scopes_level2)
						#print "Scopes externos de nivel 3:",external_scopes_level3
						#print "Lista de hedge cues de nivel 2:",hedge_cue_list_level2

						if hedge_cue_list_level2:
							first_hc_level2=hedge_cue_list_level2[0][0]
						else:
							first_hc_level2=100000
								
						if external_scopes_level3:
							first_scope_level2=external_scopes_level3[0][0]					 
						else:
							first_scope_level2=1000000
						
						#print "primera hedge cue de nivel 2", first_hc_level2
						#print "siguiente scope:", first_scope_level2
						
						while hedge_cue_list_level2 or external_scopes_level3:
							if hedge_cue_list_level2:
								next_hc_level2=hedge_cue_list_level2[0][0]
							else:
								next_hc_level2=100000
						
							if external_scopes_level3:
								next_scope_level2=external_scopes_level3[0][0]					 
							else:
								next_scope_level2=1000000
	
							if next_hc_level2<next_scope_level2:
								(hc_start_level2,hc_end_level2)=hedge_cue_list_level2[0]
								del hedge_cue_list_level2[0]
						
								#print "Proceso la cue ",hc_start_level2,hc_end_level2	
								hc_level2=xml.etree.ElementTree.SubElement(xcope_level2,"cue")
								hc_level2.attrib["ref"]=xcope_level2.attrib["id"]
								hc_level2.attrib["type"]="speculation"
		
								# El texto de la hedge cue es simplemente el texto entre start y end
								hc_level2.text=obtener_texto(tokens,hc_start_level2,hc_end_level2+1)
								#print "Texto de la hedge cue level 2:",hc_level2.text
								# El tail es el texto hasta la siguiente hedge cue, hasta el siguiente scope dentro del mismo scope externo, 
								# o hasta el fin del scope
								if hedge_cue_list_level2:
									next_hc_level2=hedge_cue_list_level2[0][0]
								else:
									next_hc_level2=100000
								hc_level2.tail=get_hc_tail(hc_end_level2,next_hc_level2,next_scope_level2,end_level2,tokens)
								#print "Tail  de la hedge cue:",hc_level2.tail
							
							#print next_scope_level2,next_hc_level2	
							if next_scope_level2<next_hc_level2:
								start_level3,end_level3,hedge_cue_list_level3,included_scopes_level3=external_scopes_level3[0]
								del external_scopes_level3[0]
								#print "Proceso el scope externo de nivel 3:", start_level3, end_level3, hedge_cue_list_level3, included_scopes_level3
								scope_num+=1
								#print "Armo scope de nivel 3"

								xcope_level3=xml.etree.ElementTree.SubElement(xcope_level2,"xcope")
								xcope_level3.attrib["id"]="X"+row1['sentence_id']+"."+str(scope_num)
								#print "Listo"


								if hedge_cue_list_level3:
									first_hc_level3=hedge_cue_list_level3[0][0]
								else:
									first_hc_level3=100000
								#print "Hedge cue que queda:", first_hc_level3
								
								# Aquí ya solo quedan hedge_cues 
								while hedge_cue_list_level3:
									next_hc_level3=hedge_cue_list_level3[0][0]
									(hc_start_level3,hc_end_level3)=hedge_cue_list_level3[0]
									del hedge_cue_list_level3[0]
						
									#print "Proceso la cue ",hc_start_level3,hc_end_level3	
									hc_level3=xml.etree.ElementTree.SubElement(xcope_level3,"cue")
									hc_level3.attrib["ref"]=xcope_level3.attrib["id"]
									hc_level3.attrib["type"]="speculation"
		
									# El texto de la hedge cue es simplemente el texto entre start y end
									hc_level3.text=obtener_texto(tokens,hc_start_level3,hc_end_level3+1)
									#print "Texto de la hedge cue level 3:",hc_level3.text
									# El tail es el texto hasta la siguiente hedge cue, hasta el siguiente scope dentro del mismo scope externo, 
									# o hasta el fin del scope
									if hedge_cue_list_level3:
										next_hc_level3=hedge_cue_list_level3[0][0]
									else:
										next_hc_level3=100000
									hc_level3.tail=get_hc_tail(hc_end_level3,next_hc_level3,100000,end_level3,tokens)
									#print "Tail  de la hedge cue:",hc_level3.tail


								xcope_level3.text=get_scope_text(start_level3, first_hc_level3,10000,end_level3,tokens)
								#print "text  del scope de nivel 3:",xcope_level3.text						
	
								# Obtengo el siguiente scope
								if len(external_scopes_level3)>0:
									next_scope_level3=external_scopes_level3[0][0]
								else:
									next_scope_level3=10000
						
								# Obtengo la siguiente hedge cue
								if len(hedge_cue_list_level2)>0:
									next_hedge_cue_level2=hedge_cue_list_level2[0][0]
								else:
									next_hedge_cue_level2=10000

								xcope_level3.tail=get_scope_tail(end_level3, next_hedge_cue_level2,next_scope_level3,end_level2,tokens)
	
								#print "tail  del scope de nivel 3:",xcope_level3.tail						
		
							xcope_level2.text=get_scope_text(start_level2, first_hc_level2,first_scope_level2,end_level2,tokens)
							#print "text  del scope de nivel 2:",xcope_level2.text							
	
							# Obtengo el siguiente scope
							if len(external_scopes_level2)>0:
								next_scope_level2=external_scopes_level2[0][0]
							else:
								next_scope_level2=10000
					
							# Obtengo la siguiente hedge cue
							if len(hedge_cue_list)>0:
								next_hedge_cue=hedge_cue_list[0][0]
							else:
								next_hedge_cue=10000

							xcope_level2.tail=get_scope_tail(end_level2, next_hedge_cue,next_scope_level2,end,tokens)
							if debug:
								print "Fin del scope de nivel 2:",end_level2
								print "Next hedge_cue:", next_hedge_cue
								print "Next scope:",next_scope_level2
								print "tail  del scope de nivel 2:",xcope_level2.tail
							
				xcope.text=get_scope_text(start,first_hc,first_scope,end,tokens)
				#print "Texto del scope:",xcope.text
				
				# El tail del scope va desde el final del scope
				# Hasta el siguiente scope, si existe
				# O hasta el final de la oración
				
				# Obtengo el siguiente scope
				if len(external_scopes)>scope_pos+1:
					next_scope=external_scopes[scope_pos+1][0]
				else:
					next_scope=10000
					
				xcope.tail=get_scope_tail(end,10000,next_scope,10000,tokens)
				#print "Tail del scope:",xcope.tail
				
				scope_pos+=1


xml.etree.ElementTree.ElementTree(docset).write(xml_file,encoding='utf-8')
#s=xml.etree.ElementTree.tostring(docset,encoding='UTF-8',method="xml")
#ElementTree(docset).write(xml_file)
