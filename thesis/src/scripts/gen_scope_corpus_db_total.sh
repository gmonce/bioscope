
# Genera las tablas de los scopes 
# uso gen_scope_corpus_db_total.sh {$BIOSCOPE | $BIOSCOPED}

WORKING_DIR=$1 

# Genera las tablas para el análisis de los scopes
echo "$0: Generating scope analysis tables..."
python $SRC/scripts/gen_scope_corpus_db.py $WORKING_DIR Y

