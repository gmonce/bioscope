#
# Script que entrena en el corpus de entrenamiento y evalúa en el heldout
# learn_scopes {$WORKING_DIR | $WORKING_DIRD} $RUN $RUNX

##### PARAMETRIZACION

# Número de corrida: ojo que si se mantiene el número se sobreescriben los logs
WORKING_DIR=$1 
RUN=$2 # Número de corrida para el aprendizaje de la HC
RUNX=$3 # Número de corrida para el aprendizaje de los scopes
HYPER=$4

# Escenarios que indican qué campos se van a utilizar: scenario para el HC, scenariox para el scope
# Si se agregan atributos al aprendizaje de la HC o el scope,  cambia el escenario correspondiente
grep 'xs:' $SRC/runs/$RUNX.scope.conf > $WORKING_DIR/run_config/$RUN.$RUNX.scope_attributes.yaml
grep 'y:' $SRC/runs/$RUNX.scope.conf >>  $WORKING_DIR/run_config/$RUN.$RUNX.scope_attributes.yaml

# Template CRF para el aprendizaje de la HC y los scopes
sed -n '/#CRF-BEGIN/,$p' $SRC/runs/$RUNX.scope.conf > $WORKING_DIR/run_config/$RUN.$RUNX.crf_template

# Control de la ejecución del script
learn_model=1 # Aprender un modelo	
gen_files=1 #Ver si tengo que generar los archivos de entrenamiento

##### FIN DEL PROCESO DE CONFIGURACION DE LA CORRIDA ###

# Creamos el directorio para almacenar los archivos de la corrida
if [ ! -d $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX ]; then
	mkdir $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX
fi

# Genera los archivos de entrenamiento y evaluación a partir de las tablas
if [ $gen_files = 1 ]; then

	# Toma BIOSCOPE80_SCOPE y genera trainx.data
	# Toma BIOSCOPE20_SCOPE y genera testx.data
	echo "$0: generating scope corpus..."
	python $SRC/scripts/gen_scope_learning_files.py $WORKING_DIR/bioscope.db  $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data $WORKING_DIR/run_config/$RUN.$RUNX.scope_attributes.yaml
	echo "$0: cleaning data..."
	./clean_data.sh $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data
	./clean_data.sh $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data
	echo "Generating Gold Standard XML from evaluation data"
	python $SRC/scripts/gen_evaluation_xml.py $WORKING_DIR/bioscope.db HELDOUT HC_ORIGINAL SCOPE_ORIGINAL $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/gold_standard.xml
fi

# Entrenar sobre los datos de entrenamiento y evaluar la detección del alcance
if [ $learn_model = 1 ]; then
	echo "$0:CRF train on $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data "
	# Aprende el modelo desde trainx.data 
	crf_learn -c $HYPER $WORKING_DIR/run_config/$RUN.$RUNX.crf_template $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data $WORKING_DIR/crf_models/modelx.$RUN.$RUNX

fi

	echo "Prediction results" > $WORKING_DIR/logs/log.$RUN.$RUNX
	echo "------------------" >> $WORKING_DIR/logs/log.$RUN.$RUNX
	echo " ">> $WORKING_DIR/logs/log.$RUN.$RUNX

	# Evaluo utilizando la hedge cue original

	# Evalua los resultados sobre testx.data y deja los resultados en testx.data.crf_results. Postprocesa la última columna con las reglas de MOrante
	echo "$0: CRF test, original hedge cue..."
	crf_test -v 1 -m $WORKING_DIR/crf_models/modelx.$RUN.$RUNX $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data > $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.crf_results
	echo "Postprocessing scopes..."
	python $SRC/scripts/scope_postprocess.py $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.crf_results $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.crf_results_pp $RUNX
	# Actualizo resultados de la evaluación
	echo "Updating evaluation results..."
	python $SRC/scripts/update_guessed_scope.py $WORKING_DIR/bioscope.db $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.crf_results_pp bioscope20_scope
	# Cargo en las tablas de errores las instancias que tuvieron problemas de clasificación
	echo "Generating error log..."
	python $SRC/scripts/insert_scope_errors.py $WORKING_DIR $RUNX

	
	echo "Generating Evaluation XML from original hedge cue and guessed scope..."
	python $SRC/scripts/gen_evaluation_xml.py $WORKING_DIR/bioscope.db HELDOUT HC_ORIGINAL SCOPE_GUESSED $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_scope.xml
	echo "Evaluating scope detection on testing corpus using original hedge cue..." >> $WORKING_DIR/logs/log.$RUN.$RUNX
	java -jar $SRC/scorer_task2_cue.jar $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/gold_standard.xml $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_scope.xml >> $WORKING_DIR/logs/log.$RUN.$RUNX
	# Genero tabla de diferencias
	java -jar $SRC/ScopeEval.jar -A $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/gold_standard.xml -B $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_scope.xml -ES $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/error_list.diff

	# Evaluo utilizando la guessed hedge cue en vez de la hedge cue. El resultado queda en testx_ghc.data.crf_results_pp
	echo "$0:CRF test, guessed hedge cue..."
	crf_test -v 1 -m $WORKING_DIR/crf_models/modelx.$RUN.$RUNX $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data > $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.crf_results
	echo "Postprocessing scopes..."
	python $SRC/scripts/scope_postprocess.py $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.crf_results $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.crf_results_pp $RUNX
	echo "Updating evaluation results..."
	python $SRC/scripts/update_guessed_scope.py $WORKING_DIR/bioscope.db $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.crf_results_pp bioscope20_ghc_scope
	echo "Generating Evaluation XML from guessed hedge cue and guessed scope..."	
	python $SRC/scripts/gen_evaluation_xml.py $WORKING_DIR/bioscope.db HELDOUT HC_GUESSED SCOPE_GUESSED $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_hc_and_scope.xml	
	echo " ">> $WORKING_DIR/logs/log.$RUN.$RUNX
	echo "Evaluating scope detection on testing corpus with guessed hedge cue..." >> $WORKING_DIR/logs/log.$RUN.$RUNX
	java -jar $SRC/scorer_task2_cue.jar $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/gold_standard.xml $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_hc_and_scope.xml >> $WORKING_DIR/logs/log.$RUN.$RUNX
	# Genero tabla de diferencias
	java -jar $SRC/ScopeEval.jar -A $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/gold_standard.xml -B $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_hc_and_scope.xml -ES $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/error_list_guessed.diff



	
	echo " ">> $WORKING_DIR/logs/log.$RUN.$RUNX
	echo "Atributes">> $WORKING_DIR/logs/log.$RUN.$RUNX
	echo "---------" >> $WORKING_DIR/logs/log.$RUN.$RUNX
	cat $WORKING_DIR/run_config/$RUN.$RUNX.scope_attributes.yaml  >> $WORKING_DIR/logs/log.$RUN.$RUNX
	echo " ">> $WORKING_DIR/logs/log.$RUN.$RUNX
	echo " ">> $WORKING_DIR/logs/log.$RUN.$RUNX
	echo "CRF Template" >> $WORKING_DIR/logs/log.$RUN.$RUNX
	echo "------------" >> $WORKING_DIR/logs/log.$RUN.$RUNX
	grep -v '#CRF' $WORKING_DIR/run_config/$RUN.$RUNX.crf_template  >> $WORKING_DIR/logs/log.$RUN.$RUNX
