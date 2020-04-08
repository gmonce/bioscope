# -*- coding: utf-8 -*- 
# Script que lee un archivo en formato conll y calcula token precision 
# Uso: calc_token_accuracy source_file

import pln_inco.bioscope as bioscope
import pln_inco.bioscope.util
import os.path
import time
import sys
import yaml
from string import *

source_filename=sys.argv[1]
token_type=sys.argv[2]
script_name=os.path.join(sys.path[0],sys.argv[0])



t0=time.clock()
print script_name," Calculating token accuracy...", source_filename
#pln_inco.bioscope.scripts.postprocess_scope_learning_results(evaluation_file,target_file)

source=open(source_filename,'r')
	
sentence=[]
confidences=[]

if token_type=='HC':
	tp={'B-SPECCUE':0.0,'I-SPECCUE':0.0,'O':0.0}
	fp={'B-SPECCUE':0.0,'I-SPECCUE':0.0,'O':0.0}
	fn={'B-SPECCUE':0.0,'I-SPECCUE':0.0,'O':0.0}
	tn={'B-SPECCUE':0.0,'I-SPECCUE':0.0,'O':0.0}
	tag_list=['B-SPECCUE','I-SPECCUE','O']

else:
	tp={'F':0.0,'X':0.0,'L':0.0,'O':0.0}
	fp={'F':0.0,'X':0.0,'L':0.0,'O':0.0}
	fn={'F':0.0,'X':0.0,'L':0.0,'O':0.0}
	tn={'F':0.0,'X':0.0,'L':0.0,'O':0.0}
	tag_list=['F','X','L','O']

scope_tp=0.0
scope_tpx=0.0
ok_F=False
ok_L=False
ok_X=False
cant=0.0
cantx=0.0
cant_F=0
cant_L=0
for line in source:
	#Cargo toda una oración
	if line.startswith('#'):
		pass
	elif line != '\n':
		attributes=split(line.rstrip(),'\t')
		if '/' in attributes[-1]:		
			(tag,confidence)=attributes[-1].split('/')
			attributes[-1]=tag
		original=attributes[-2]
		predicted=attributes[-1]
		predicted_original=predicted

		
		for tag in tag_list: 
			if predicted=='X' or predicted=='Y':
				predicted='F'
			if original==tag:	
				if predicted==tag:
					tp[tag]+=1
				else:
					fn[tag]+=1
			elif predicted==tag:
				fp[tag]+=1
			else:
				tn[tag]+=1

		if original=='F' and predicted=='F':
			ok_F=True
		elif original=='L' and predicted=='L':
			ok_L=True

		if original=='F' and predicted_original in ('X','Y'):
			ok_X=True

		if predicted=='F':
			cant_F+=1
		if predicted=='L':
			cant_L+=1


	else:
		cant=cant+1
		if ok_F and ok_L:
			scope_tp+=1

		if ok_X and ok_L:
			scope_tpx+=1

		if ok_X:
			cantx+=1

		if cant_L!=1 or cant_F!=1:
			scope_tp-=1

		# Cambio de línea
		ok_F=False
		ok_L=False
		ok_X=False
		cant_F=0
		cant_L=0


for tag in tag_list: 
	if tp[tag]+fp[tag]>0:
		print 'Tag:',tag
		print 'TP:',tp[tag],' FN:',fn[tag],' FP:',fp[tag],' TN:',tn[tag]
		precision=tp[tag]/(tp[tag]+fp[tag])
		print 'Precision:', precision
		recall=tp[tag]/(tp[tag]+fn[tag])
		print 'Recall:', recall 
		print 'F-Score:',  precision*recall*2/(precision+recall)
		print 'Accuracy:', (tp[tag]+tn[tag])/(tp[tag]+fp[tag]+tn[tag]+fn[tag])
			
print "Scope accuracy...", scope_tp/cant
if cantx!=0:
	print "X accuracy...",scope_tpx/cantx
print "X part...",scope_tpx/cant
