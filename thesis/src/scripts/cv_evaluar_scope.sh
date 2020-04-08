WORKING_DIR=$1 
RUN=$2
RUNX=$3
echo " "> $WORKING_DIR/logs/cv.$RUN.$RUNX.log
for SPLIT in 1 2 3 4 5 6 7 8 9 10
#for SPLIT in 1
#for SPLIT in  3 4 5 
do
	echo "SPLIT:$SPLIT" >> $WORKING_DIR/logs/cv.$RUN.$RUNX.log
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
        # Borro archivos que no me van a servir más
        rm $WORKING_DIR/crf_models/model.total.$RUN

	echo "$0: Generating scope analysis tables..."
	python $SRC/scripts/gen_scope_corpus_db.py $WORKING_DIR Y
	echo "$0: Adding syntax  atributtes..."
	cat $SRC/scripts/add_scope_att_hc_parent.sql | sqlite3 $WORKING_DIR/bioscope.db  2>/dev/null
	python $SRC/scripts/cv_add_scope_att_hc_parent.py $WORKING_DIR $RUNX 
	echo "$0: Updating passive voice..."
	python $SRC/scripts/add_passive_voice.py $WORKING_DIR Y
	echo "$0: Updating scope2..."
	python $SRC/scripts/update_scope_2.py $WORKING_DIR $RUNX Y

	grep 'xs:' $SRC/runs/$RUNX.scope.conf > $WORKING_DIR/run_config/$RUN.$RUNX.scope_attributes.yaml
	grep 'y:' $SRC/runs/$RUNX.scope.conf >>  $WORKING_DIR/run_config/$RUN.$RUNX.scope_attributes.yaml

	# Template CRF para el aprendizaje de la HC y los scopes
	sed -n '/#CRF-BEGIN/,$p' $SRC/runs/$RUNX.scope.conf > $WORKING_DIR/run_config/$RUN.$RUNX.crf_template

	echo "$0: generating scope corpus..."
        python $SRC/scripts/gen_scope_learning_files.py $WORKING_DIR/bioscope.db  $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data.total $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.total $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.total $WORKING_DIR/run_config/$RUN.$RUNX.scope_attributes.yaml Y
        echo "$0: cleaning data..."
        ./clean_data.sh $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data.total
        ./clean_data.sh $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.total
        echo "Generating Gold Standard XML from evaluation data"
        python $SRC/scripts/gen_evaluation_xml.py $WORKING_DIR/bioscope.db TOTAL HC_ORIGINAL SCOPE_ORIGINAL $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/gold_standard_total.xml

        echo "$0:CRF train on $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data.total "
        # Aprende el modelo desde trainx.data.total
	if [ $RUNX = 48 ]
	then
	 		echo "Corrida 48"
	        crf_learn -c 0.4 $WORKING_DIR/run_config/$RUN.$RUNX.crf_template $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data.total $WORKING_DIR/crf_models/modelx.total.$RUN.$RUNX
	else
		echo "Corrida diferente a la 48"
	       crf_learn $WORKING_DIR/run_config/$RUN.$RUNX.crf_template $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/trainx.data.total $WORKING_DIR/crf_models/modelx.total.$RUN.$RUNX
	fi	


        # Evaluo utilizando la hedge cue original
        # Evalua los resultados sobre testx.data.total y deja los resultados en testx.data.crf_results. Postprocesa la última columna con las reglas de MOrante
        echo "$0: CRF test, original hedge cue..."
        crf_test -v 1 -m $WORKING_DIR/crf_models/modelx.total.$RUN.$RUNX $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.total > $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.total.crf_results
        echo "$0:Postprocessing scopes..."
        python $SRC/scripts/scope_postprocess.py $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.total.crf_results $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.total.crf_results_pp $RUNX
        echo "$0:Updating evaluation results..."
        python $SRC/scripts/update_guessed_scope.py $WORKING_DIR/bioscope.db $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx.data.total.crf_results_pp bioscope_test_scope
        echo "$0:Generating Evaluation XML from original hedge cue and guessed scope..."
        python $SRC/scripts/gen_evaluation_xml.py $WORKING_DIR/bioscope.db TOTAL HC_ORIGINAL SCOPE_GUESSED $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_scope_total.xml
        echo "Evaluating scope detection on testing corpus using original hedge cue..." >> $WORKING_DIR/logs/cv.$RUN.$RUNX.log
        java -jar $SRC/scorer_task2_cue.jar $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/gold_standard_total.xml $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_scope_total.xml >> $WORKING_DIR/logs/cv.$RUN.$RUNX.log

        # Evaluo utilizando la guessed hedge cue en vez de la hedge cue. El resultado queda en testx_ghc.data.crf_results_pp.total
        echo "$0:CRF test, guessed hedge cue..."
        crf_test -v 1 -m $WORKING_DIR/crf_models/modelx.total.$RUN.$RUNX $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.total > $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.total.crf_results
        echo "Postprocessing scopes..."
        python $SRC/scripts/scope_postprocess.py $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.total.crf_results $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.total.crf_results_pp $RUNX
        echo "Updating evaluation results..."
        python $SRC/scripts/update_guessed_scope.py $WORKING_DIR/bioscope.db $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/testx_ghc.data.total.crf_results_pp bioscope_test_ghc_scope
        echo "Generating Evaluation XML from guessed hedge cue and guessed scope..."    
        python $SRC/scripts/gen_evaluation_xml.py $WORKING_DIR/bioscope.db TOTAL HC_GUESSED SCOPE_GUESSED $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_hc_and_scope_total.xml   
        echo "Evaluating scope detection on testing corpus with guessed hedge cue..." >> $WORKING_DIR/logs/cv.$RUN.$RUNX.log
        java -jar $SRC/scorer_task2_cue.jar $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/gold_standard_total.xml $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/guessed_hc_and_scope_total.xml >> $WORKING_DIR/logs/cv.$RUN.$RUNX.log

done

