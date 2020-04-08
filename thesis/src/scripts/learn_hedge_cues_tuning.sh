# Número de corrida: ojo que si se mantiene el número se sobreescriben los logs
WORKING_DIR=$1
RUNNING_DIR=$1/crf_corpus/hc/final
CONF_FILE=$2
LOG_FILE=$3

# Escenarios que indican qué campos se van a utilizar: scenario para el HC
# Si se agregan atributos al aprendizaje de la HC   cambia el escenario correspondiente
grep 'xs:' $RUNNING_DIR/$CONF_FILE > $RUNNING_DIR/run.yaml
grep 'y:' $RUNNING_DIR/$CONF_FILE >> $RUNNING_DIR/run.yaml

# Template CRF para el aprendizaje de la HC
sed -n '/#CRF-BEGIN/,$p' $RUNNING_DIR/$CONF_FILE > $RUNNING_DIR/run.crf_template


# Genero archivos de entrenamiento y testeo
#echo "$0: Generate training and evaluation files..."	
#python $SRC/scripts/gen_hc_learning_files.py $WORKING_DIR/bioscope.db $RUNNING_DIR/train.data $RUNNING_DIR/test.data  $RUNNING_DIR/run.yaml
#echo "$0: Cleaning data..."
#$SRC/scripts/clean_data.sh $RUNNING_DIR/train.data
#$SRC/scripts/clean_data.sh $RUNNING_DIR/test.data
# Entrenar sobre el 80% del corpus y evaluar sobre el 20% restante, con el objetivo de aprender la hedge cue
echo "Train on the 80% of the training corpus and test over the remaining 20%, trying to learn hedge cues"
echo "$0:CRF train..."
crf_learn $RUNNING_DIR/run.crf_template $RUNNING_DIR/train.data $RUNNING_DIR/model.final
echo "$0:CRF test..."
crf_test -v 1 -m $RUNNING_DIR/model.final  $RUNNING_DIR/test.data > $RUNNING_DIR/test.data.crf_results
echo "$0:Generating results..."
cat $RUNNING_DIR/test.data.crf_results | egrep -v '#' | sed 's/\/0\.[0-9]*$//' | $SRC/scripts/conlleval.pl -d '\t' | grep -v 'SPECCUE'   >> $LOG_FILE




