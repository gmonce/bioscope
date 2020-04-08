
# Entrena, evalúa y aprende hedge cues, entrena sobre el corpus total de entrenamiento y evalúa sobre el de evaluación
# Formato learn_hedge_cues.sh {$BIOSCOPE | $BIOSCOPED$} $RUN

############ Configuración de la corrida

# Número de corrida: ojo que si se mantiene el número se sobreescriben los logs
WORKING_DIR=$1
RUN=$2


# Escenarios que indican qué campos se van a utilizar: scenario para el HC
# Si se agregan atributos al aprendizaje de la HC   cambia el escenario correspondiente
grep 'xs:' $SRC/runs/$RUN.hc.conf > $WORKING_DIR/run_config/$RUN.hc_attributes.yaml
grep 'y:' $SRC/runs/$RUN.hc.conf >>  $WORKING_DIR/run_config/$RUN.hc_attributes.yaml

# Template CRF para el aprendizaje de la HC
sed -n '/#CRF-BEGIN/,$p' $SRC/runs/$RUN.hc.conf > $WORKING_DIR/run_config/$RUN.crf_template

# Control de la ejecución del script, solamente para debugging
gen_hc_corpus=1; # Regenerar los archivos de entrenamiento
learn_hc=1 # Ejecutar el proceso de aprendizaje de hedge cue y reportar resultados

##### FIN DEL PROCESO DE CONFIGURACION DE LA CORRIDA ###


# Creamos el directorio para almacenar los archivos de la corrida
if [ ! -d $WORKING_DIR/crf_corpus/hc/$RUN ]; then
	mkdir $WORKING_DIR/crf_corpus/hc/$RUN
fi

# Genero archivos de entrenamiento y testeo
if [ $gen_hc_corpus = 1 ]; then
	echo "$0: Generate training and evaluation files..."	
	python $SRC/scripts/gen_hc_learning_files.py $WORKING_DIR/bioscope.db $WORKING_DIR/crf_corpus/hc/$RUN/train.total.data $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data $WORKING_DIR/run_config/$RUN.hc_attributes.yaml Y
	echo "$0: Cleaning data..."
	./clean_data.sh $WORKING_DIR/crf_corpus/hc/$RUN/train.total.data
	./clean_data.sh $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data
fi

# Entrenar sobre el 100% del corpus de entrenamiento  y evaluar sobre el corpus de evaluación, con el objetivo de aprender la hedge cue

if [ $learn_hc = 1 ]; then
	echo "Train on the full of the training corpus and test over the evaluation corpus, trying to learn hedge cues"
	echo "$0:CRF train..."
	crf_learn $WORKING_DIR/run_config/$RUN.crf_template $WORKING_DIR/crf_corpus/hc/$RUN/train.total.data $WORKING_DIR/crf_models/model.total.$RUN
	echo "$0:CRF test..."
	crf_test -v 1 -m $WORKING_DIR/crf_models/model.total.$RUN $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data > $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data.crf_results
	echo "$0: adding hedge_cue prediction to BIOSCOPE_TRAIN table"
	python $SRC/scripts/add_hedge_cue_prediction.py $WORKING_DIR $RUN Y
	echo "$0:Evaluating hedge_cue prediction results to log.total.$RUN"
	echo " ">> $WORKING_DIR/logs/log.total.$RUN
	echo "Prediction results" > $WORKING_DIR/logs/log.total.$RUN
	echo "------------------" >> $WORKING_DIR/logs/log.total.$RUN
	echo " ">> $WORKING_DIR/logs/log.total.$RUN
	# Antes de evaluar tengo que eliminar los valores de confidence en la predicción
	cat $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data.crf_results | egrep -v '#' | sed 's/\/0\.[0-9]*$//' | ./conlleval.pl -d '\t' | grep -v 'SPECCUE'   >> $WORKING_DIR/logs/log.total.$RUN

	# Cargo en las tablas de errores las instancias que tuvieron problemas de clasificación
	python $SRC/scripts/insert_hc_errors.py $WORKING_DIR $RUN Y


	# Borro archivos que no me van a servir más
	rm $WORKING_DIR/crf_models/model.total.$RUN
fi
