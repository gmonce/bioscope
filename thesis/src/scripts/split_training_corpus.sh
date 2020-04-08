# Genera el corpus held out a partir del principal
#
# uso: split_training_corpus.sh {$BIOSCOPE | $BIOSCOPED}

WORKING_DIR=$1

echo "$0: Generating held out corpus..."
python $SRC/scripts/split_training_corpus.py $WORKING_DIR

