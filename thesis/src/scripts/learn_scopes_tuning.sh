
# Número de corrida: ojo que si se mantiene el número se sobreescriben los logs
WORKING_DIR=$1
RUNNING_DIR=$1/crf_corpus/scope/final
CONF_FILE=$2
LOG_FILE=$3

# Escenarios que indican qué campos se van a utilizar: scenario para el HC
# Si se agregan atributos al aprendizaje de la HC   cambia el escenario correspondiente
grep 'xs:' $RUNNING_DIR/$CONF_FILE > $RUNNING_DIR/run.yaml
grep 'y:' $RUNNING_DIR/$CONF_FILE >> $RUNNING_DIR/run.yaml

# Template CRF para el aprendizaje de la HC
sed -n '/#CRF-BEGIN/,$p' $RUNNING_DIR/$CONF_FILE > $RUNNING_DIR/run.crf_template

echo "$0:CRF train on $RUNNING_DIR/trainx.data "
crf_learn $RUNNING_DIR/run.crf_template $RUNNING_DIR/trainx.data $RUNNING_DIR/modelx.final

# Evaluo utilizando la hedge cue original
# Evalua los resultados sobre testx.data y deja los resultados en testx.data.crf_results. Postprocesa la última columna con las reglas de MOrante
echo "$0: CRF test, original hedge cue..."
crf_test -v 1 -m $RUNNING_DIR/modelx.final $RUNNING_DIR/testx.data > $RUNNING_DIR/testx.data.crf_results
echo "Postprocessing scopes..."
python $SRC/scripts/scope_postprocess.py $RUNNING_DIR/testx.data.crf_results $RUNNING_DIR/testx.data.crf_results_pp
echo "Updating evaluation results..."
python $SRC/scripts/update_guessed_scope.py $WORKING_DIR/bioscope.db $RUNNING_DIR/testx.data.crf_results_pp bioscope20_scope
echo "Generating Evaluation XML from original hedge cue and guessed scope..."
python $SRC/scripts/gen_evaluation_xml.py $WORKING_DIR/bioscope.db HELDOUT HC_ORIGINAL SCOPE_GUESSED $RUNNING_DIR/guessed_scope.xml
echo "Evaluating..."
java -jar $SRC/scorer_task2_cue.jar $RUNNING_DIR/gold_standard.xml $RUNNING_DIR/guessed_scope.xml | grep -v "cue_" | tr '\n' ' ' >> $LOG_FILE
echo " ">> $LOG_FILE
echo "OK"
