WORKING_DIR=$1 
RUN=$2
echo " "> $WORKING_DIR/logs/cv.$RUN.log
for SPLIT in 1 2 3 4 5 6 7 8 9 10
do
	echo "SPLIT:"$SPLIT >> $WORKING_DIR/logs/cv.$RUN.log
	echo "$0:Generating learning sets..."
	python $SRC/scripts/cv_generate_learning_sets.py $WORKING_DIR $SPLIT
	echo "$0: Adding Hyland hedges..."
	python $SRC/scripts/add_hyland_hedges.py $WORKING_DIR
	echo "$0: adding corpus occurrences..."
	python $SRC/scripts/add_hc_corpus_occurrences.py $WORKING_DIR Y

	# Escenarios que indican qué campos se van a utilizar: scenario para el HC
	grep 'xs:' $SRC/runs/$RUN.hc.conf > $WORKING_DIR/run_config/$RUN.hc_attributes.yaml
	grep 'y:' $SRC/runs/$RUN.hc.conf >>  $WORKING_DIR/run_config/$RUN.hc_attributes.yaml

	# Template CRF para el aprendizaje de la HC
	sed -n '/#CRF-BEGIN/,$p' $SRC/runs/$RUN.hc.conf > $WORKING_DIR/run_config/$RUN.crf_template

	# Genero archivos de entrenamiento y testeo
	echo "$0: Generate training and evaluation files..."    
	python $SRC/scripts/gen_hc_learning_files.py $WORKING_DIR/bioscope.db $WORKING_DIR/crf_corpus/hc/$RUN/train.total.data $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data $WORKING_DIR/run_config/$RUN.hc_attributes.yaml Y
	echo "$0: Cleaning data..."
	./clean_data.sh $WORKING_DIR/crf_corpus/hc/$RUN/train.total.data
	./clean_data.sh $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data

	echo "Train on the full of the training corpus and test over the evaluation corpus, trying to learn hedge cues"
	echo "$0:CRF train..."
	crf_learn $WORKING_DIR/run_config/$RUN.crf_template $WORKING_DIR/crf_corpus/hc/$RUN/train.total.data $WORKING_DIR/crf_models/model.total.$RUN
	echo "$0:CRF test..."
	crf_test -v 1 -m $WORKING_DIR/crf_models/model.total.$RUN $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data > $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data.crf_results
	echo "$0: adding hedge_cue prediction to BIOSCOPE_TRAIN table"
	python $SRC/scripts/add_hedge_cue_prediction.py $WORKING_DIR $RUN Y
	echo "$0:Evaluating hedge_cue prediction results"
	# Antes de evaluar tengo que eliminar los valores de confidence en la predicción
	cat $WORKING_DIR/crf_corpus/hc/$RUN/test.total.data.crf_results | egrep -v '#' | sed 's/\/0\.[0-9]*$//' | ./conlleval.pl -d '\t' | grep 'accuracy'   >> $WORKING_DIR/logs/cv.$RUN.log
	# Borro archivos que no me van a servir más
	rm $WORKING_DIR/crf_models/model.total.$RUN
done


