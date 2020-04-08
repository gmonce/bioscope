# Entrena, evalúa y aprende hedge cues 
# Formato learn_hedge_cues.sh {$BIOSCOPE | $BIOSCOPED } $RUN
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
	python $SRC/scripts/gen_hc_learning_files.py $WORKING_DIR/bioscope.db $WORKING_DIR/crf_corpus/hc/$RUN/train.data $WORKING_DIR/crf_corpus/hc/$RUN/test.data  $WORKING_DIR/run_config/$RUN.hc_attributes.yaml
	echo "$0: Cleaning data..."
	./clean_data.sh $WORKING_DIR/crf_corpus/hc/$RUN/train.data
	./clean_data.sh $WORKING_DIR/crf_corpus/hc/$RUN/test.data
fi


# Entrenar sobre el 80% del corpus y evaluar sobre el 20% restante, con el objetivo de aprender la hedge cue
if [ $learn_hc = 1 ]; then

	echo "Train on the 80% of the training corpus and test over the remaining 20%, trying to learn hedge cues"
	
	echo "$0:CRF train..."

	crf_learn $WORKING_DIR/run_config/$RUN.crf_template $WORKING_DIR/crf_corpus/hc/$RUN/train.data $WORKING_DIR/crf_models/model.$RUN

	echo "$0:CRF test..."
	crf_test -v 1 -m $WORKING_DIR/crf_models/model.$RUN $WORKING_DIR/crf_corpus/hc/$RUN/test.data > $WORKING_DIR/crf_corpus/hc/$RUN/test.data.crf_results
	echo "$0: adding hedge_cue prediction to BIOSCOPE_TRAIN table"
	python $SRC/scripts/add_hedge_cue_prediction.py $WORKING_DIR $RUN
	echo "$0:Evaluating hedge_cue prediction results to log.$RUN"
	echo "Prediction results" > $WORKING_DIR/logs/log.$RUN
	echo "------------------" >> $WORKING_DIR/logs/log.$RUN
	echo " ">> $WORKING_DIR/logs/log.$RUN
	# Antes de evaluar tengo que eliminar los valores de confidence en la predicción
	cat $WORKING_DIR/crf_corpus/hc/$RUN/test.data.crf_results | egrep -v '#' | sed 's/\/0\.[0-9]*$//' | ./conlleval.pl -d '\t' | grep -v 'SPECCUE'   >> $WORKING_DIR/logs/log.$RUN
	echo " ">> $WORKING_DIR/logs/log.$RUN
	echo "Atributes">> $WORKING_DIR/logs/log.$RUN
	echo "---------" >> $WORKING_DIR/logs/log.$RUN
	cat $WORKING_DIR/run_config/$RUN.hc_attributes.yaml  >> $WORKING_DIR/logs/log.$RUN
	echo " ">> $WORKING_DIR/logs/log.$RUN
	echo " ">> $WORKING_DIR/logs/log.$RUN
	echo "CRF Template" >> $WORKING_DIR/logs/log.$RUN
	echo "------------" >> $WORKING_DIR/logs/log.$RUN
	grep -v '#CRF' $WORKING_DIR/run_config/$RUN.crf_template  >> $WORKING_DIR/logs/log.$RUN
	
	# Cargo en las tablas de errores las instancias que tuvieron problemas de clasificación
	python $SRC/scripts/insert_hc_errors.py $WORKING_DIR $RUN
	
	
	# Borro archivos que no me van a servir más
	rm $WORKING_DIR/crf_models/model.$RUN
fi



