# Asuma que en $1 está el $BIOSCOPE
# y en $2 el nombre del documento a[xxxxxx]

# Primera regla: convierto las [n,n-] en [n_n-] para que genia los tokenize bien
#cat $1/abstracts_train_original.xml | sed -f ./tokens_adjust.rules > $1/abstracts_train.xml
#cat $1/abstracts_test_original.xml | sed  -f ./tokens_adjust.rules > $1/abstracts_test.xml

# Genera los txt de nuevo 
#python generate_txt_files.py $1
#python generate_bioscope_files.py $1
python generate_genia_files.py $1 $2.txt
python gen_parsed_files.py $1 $2.genia 1

# Verifico que carga bien ahora
python load_enriched_corpus.py $1 $2






