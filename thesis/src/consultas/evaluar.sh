WORKING_DIR=$BIOSCOPE
RUN=11
RUNX=36
GOLD_FILE=gold_standard.xml
EVALUATION_FILE=guessed_scope.xml
#java -jar $SRC/scorer_task2_cue.jar $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/$GOLD_FILE $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/$EVALUATION_FILE 
java -jar $SRC/ScopeEval.jar -A $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/$GOLD_FILE -B $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/$EVALUATION_FILE -ES $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/eval.diff
 

