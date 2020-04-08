# Agrega atributos adicionales a las tablas ya generadas
#
# uso: add_hc_corpus_occurrences.sh {$BIOSCOPE | $BIOSCOPED}

WORKING_DIR=$1

echo "$0: Marking occurence of the word in the training corpus as hedge cue..."
python $SRC/scripts/add_hc_corpus_occurrences.py $WORKING_DIR

