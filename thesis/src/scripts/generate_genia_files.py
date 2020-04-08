# -*- coding: utf-8 -*- 
# A partir de los archivos de texto, los analiza con el tagger genia y genera los archivos .genia con el resultado del análisis
# Recibe como parámetros el directorio de trabajo,  el pattern con los archivos a analizar
# Ejemplo python generate_genia_files.py $BIOSCOPE 'a*.txt'

import sys
import pln_inco.genia_tagger
import pln_inco.penn_treebank
import pln_inco.bioscope
import nltk.corpus
import xml
import string
import fnmatch
import os

working_dir=sys.argv[1]
pattern=sys.argv[2]

bcp=pln_inco.bioscope.BioscopeCorpusProcessor(working_dir, 'abstracts_train.xml')
output=''
print >> sys.stderr, "Genero archivo temporal para genia..."
for fileName in os.listdir(bcp.txt_dir):
		if fnmatch.fnmatch(fileName,pattern):
			f=open(os.path.join(bcp.txt_dir,fileName),'r')
			output=output+'========='+fileName+'=========\n'+f.read()
temp=open(os.path.join(bcp.genia_home,'temp.genia'),"w")
temp.write(output)
temp.close()
print >> sys.stderr, "Tag!..."
result=pln_inco.genia_tagger.tag('temp.genia',bcp.genia_home)
print >> sys.stderr, "Paso a escribir..."
temp=open('genia_results',"w")
temp.write(result)
temp.close()

# Leo el archivo temporal
f=open('genia_results','r')
lineas=f.readlines()

# Proceso las oraciones
sentence_id=None
s='' # Texto generado para la oración
s_articulo='' # Texto generado para el artículo
position=0
# Indica si tengo que omitir procesar una línea porque la junté con la línea anterior
saltar_lineas=0
for l in lineas:
	if saltar_lineas > 0:
		saltar_lineas = saltar_lineas-1
	elif l.startswith('========='):
		# Obtengo el id del artículo
		l=l.replace('=========','')
		index=l.find('\t')
		docId=l[0:index].replace('.txt','')

		# Obtengo el arbolito xml corrpondiente al artículo, a partir del .bioscope
		bioscope_doc=bcp.bioscope_files_corpus.xml(docId+'.bioscope')
		sentences=bioscope_doc.getchildren()
		sentence_pos=0
		s_articulo=''
		after_linea=True
	elif l=='\n' and not after_linea:
		# Estoy en un enter separador de oraciones
		# Genero el archivo correspondiente a la oración que ven??a procesando
		geniaFileName=docId+'.'+sentence_id+'.genia'
		print >> sys.stderr, "Genero archivo ...", geniaFileName
		f=open(os.path.join(bcp.genia_files_dir,geniaFileName),'w+')
		f.write(s)
		f.close()

		# Inserto un enter en la salida del artículo
		s_articulo+= '\n'

		# Incremento el número de oración
		try:
			sentence_pos += 1
			sentence_id=sentences[sentence_pos].get('id')				
			s=''				
		except IndexError:
			# Como ya no quedan oraciones, genero el .genia del artículo
			geniaFileName=docId+'.genia'
			print >> sys.stderr, "Genero archivo ...", geniaFileName
			f=open(os.path.join(bcp.genia_articles_dir,geniaFileName),'w+')
			f.write(s_articulo)
			f.close()
			s_articulo=''
	elif l=='\n':
		# Estoy en el primer enter, incremento el n??mero de oración
		after_linea=False
		sentence_id=sentences[sentence_pos].get('id')				
		s=''				
	else:
		# Incremento la oración hasta el momento con la palabra
		#s += l
		# Para el caso de lo generado para el artículo, proceso la línea para que 
		# quede pronta para ser utilizada por el parser
		# El formato que genero es palabra/tag, con procesamiento para que quede como el penntreebank
		# Primero me quedo con las columnas 1 y 3
		(word,lemma,pos,chunk,ne)=string.split(l,'\t')
		# Quito el enter al ne
		ne=ne[0:len(ne)-1]

		#print >> sys.stderr, "Position vale",position
		#print >> sys.stderr, "Largo de lineas ",len(lineas)
		#print >> sys.stderr, "split(lineas[position+1],'\t') ",split(lineas[position+1],'\t')
		#print >> sys.stderr, "split(lineas[position+2],'\t') ",split(lineas[position+2],'\t')
		# Genia, en la ??ltima palabra de la oración, no tokeniza bien
		# Por lo que si la oración termina en un ., hay que generar dos tokens
		if pos=='.' and lemma<>'.' and word.endswith('.'):
			# Genia tiene un bug, que hace que en algunos casos si es la última palabra
			# No s??lo la pega con el punto (como hace en general)
			# Sino que además le pone el tag '.'
			# Ver la oración S19.8, del documento a91187647

			# Lo que hago es separar en palabra y punto
			# Y ponerle a prepo el tag "NN" a la palabra que genia omiti?? clasificar

			word=word[0:len(word)-1]
			lemma=word[0:len(word)-1]
			pos='NN'
			chunk='O'
			ne='O'

			s_articulo += '/'.join([word,pos])
			s_articulo += ' '
			s_articulo += '/'.join(['.','.'])
			s_articulo += ' '


			s += '\t'.join([word,lemma,pos,chunk,ne])
			s += '\n'
			s += '\t'.join(['.','.','.','O','O'])
			s += '\n'					
		elif word.endswith('.') and pos<>'.' and lineas[position+1]=='\n':
			# Si termina en punto, pero el lemma no es punto, y es la ??ltima palabra
			# Genia peg?? la ??ltima palabra con el punto
			# por lo que los separo en dos
			lemma=lemma[0:len(lemma)-1]
			word=word[0:len(word)-1]

			s_articulo += '/'.join([word,pos])
			s_articulo += ' '
			s_articulo += '/'.join(['.','.'])
			s_articulo += ' '

			s += '\t'.join([word,lemma,pos,chunk,ne])
			s += '\n'
			s += '\t'.join(['.','.','.','O','O'])
			s += '\n'					
		elif pos=='CD' and position<=len(lineas)-3 and lineas[position+1]<>'\n' and lineas[position+2]<>'\n' and string.split(lineas[position+1],'\t')[2]==',' and string.split(lineas[position+2],'\t')[2]=='CD':
			# Si estoy en una situacion de numero,numero, genia lo separa err??neamente
			# tengo que juntarlas
			# el pos, chunk y el ne quedan como el primero
			# tengo luego que saltarme las dos lineas siguientes
			siguiente_numero=string.split(lineas[position+2],'\t')[0]
			word=word+','+siguiente_numero
			lemma=lemma+','+siguiente_numero
			s_articulo +='/'.join([pln_inco.penn_treebank.ptb_conversion_word(word),pln_inco.penn_treebank.ptb_conversion_pos(pos)])
			s_articulo += ' '

			s += '\t'.join([pln_inco.penn_treebank.ptb_conversion_word(word),lemma,pln_inco.penn_treebank.ptb_conversion_pos(pos),chunk,ne])
			s +='\n'
			saltar_lineas=2					
		else:					
			# Caso general
			s_articulo +='/'.join([pln_inco.penn_treebank.ptb_conversion_word(word),pln_inco.penn_treebank.ptb_conversion_pos(pos)])
			s_articulo += ' '

			s += '\t'.join([pln_inco.penn_treebank.ptb_conversion_word(word),lemma,pln_inco.penn_treebank.ptb_conversion_pos(pos),chunk,ne])
			s +='\n'
	position=position+1
