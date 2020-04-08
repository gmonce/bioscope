# -*- coding: utf-8 -*- 
# Uso: cv_generate_bioscope_table.py $BIOSCOPE 

import os.path
import time
import sys
import sqlite3
import random

working_dir=sys.argv[1]
dbname=os.path.join(working_dir,'bioscope.db')


# Inicializo la conexión a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()

script_name=os.path.join(sys.path[0],sys.argv[0])
bioscope_table='BIOSCOPE'

t0=time.clock()
# Inicializo la conección a la base de datos
conn= sqlite3.connect(dbname)	
conn.text_factory = str
conn.row_factory=sqlite3.Row
c=conn.cursor()
c2=conn.cursor()

c.execute('select document_id from bioscope group by document_id')
for row in c:
        #Sorteo
	split=str(random.uniform(1,10.99)).split('.')[0]
        c2.execute('update bioscope set split=?  where document_id=?',(split,row['document_id']))


conn.commit()
