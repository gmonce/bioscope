# Levanta el corpus y genera la base de datos de aprendizaje
#
# uso: generate_corpus_db.sh {$BIOSCOPE | $BIOSCOPED}

WORKING_DIR=$1

# Recreo las tablas
# Genero las tablas vacías, borrándolas si existían
echo "$0: Generating table structure..."
cat $SRC/scripts/create_db.sql | sqlite3 $WORKING_DIR/bioscope.db
cat $SRC/scripts/create_error_log_db.sql | sqlite3 $WORKING_DIR/bioscope.db

# Cargo las tablas
echo "$0: populating corpus tables"
python $SRC/scripts/gen_corpus_db.py $WORKING_DIR
# Actualizo los valores para los hedge_cues discontinuos
python $SRC/scripts/update_discontinuous_hc.py $WORKING_DIR


