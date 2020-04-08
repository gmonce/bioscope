WORKING_DIR=$BIOSCOPE
RUN=11
RUNX=38
SOURCE_FILE=testx.data.crf_results
DEST_FILE=testx.data.crf_results_pp
python $SRC/scripts/scope_postprocess.py $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/$SOURCE_FILE $WORKING_DIR/crf_corpus/scope/$RUN.$RUNX/$DEST_FILE
