#
# Script que entrena en el corpus de entrenamiento y evalúa en el heldout
# scope_rules_tuning $VERSION

##### PARAMETRIZACION

# Número de corrida: ojo que si se mantiene el número se sobreescriben los logs
VERSION=$1 
WORKING_DIR=$BIOSCOPE

grep "VERSION:" $WORKING_DIR/crf_corpus/scope/final/scope_postprocess.$VERSION.py >> $WORKING_DIR/crf_corpus/scope/final/log
python $WORKING_DIR/crf_corpus/scope/final/scope_postprocess.$VERSION.py $WORKING_DIR/crf_corpus/scope/final/testx.data.crf_results $WORKING_DIR/crf_corpus/scope/final/testx.data.crf_results_pp
python $SRC/scripts/update_guessed_scope.py $WORKING_DIR/bioscope.db $WORKING_DIR/crf_corpus/scope/final/testx.data.crf_results_pp bioscope20_scope
python $SRC/scripts/gen_evaluation_xml.py $WORKING_DIR/bioscope.db HELDOUT HC_ORIGINAL SCOPE_GUESSED $WORKING_DIR/crf_corpus/scope/final/guessed_scope.xml
java -jar $SRC/scorer_task2_cue.jar $WORKING_DIR/crf_corpus/scope/final/gold_standard.xml $WORKING_DIR/crf_corpus/scope/final/guessed_scope.xml | grep -v "cue_" | tr '\n' ' ' >> $WORKING_DIR/crf_corpus/scope/final/log
echo " ">> $WORKING_DIR/crf_corpus/scope/final/log
cat $WORKING_DIR/crf_corpus/scope/final/log
