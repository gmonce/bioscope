# Ejecuta el proceso completo de aprendizaje 

WORKING_DIR=$1
RUN=$2
RUNX=$3

#$SRC/scripts/add_hyland_hedges.sh $WORKING_DIR
#$SRC/scripts/add_hc_corpus_occurrences_total.sh $WORKING_DIR $RUN
#$SRC/scripts/learn_hedge_cues_total.sh $WORKING_DIR $RUN
#cat $WORKING_DIR/logs/log.total.$RUN | egrep 'accuracy|processed'
#$SRC/scripts/gen_scope_corpus_db_total.sh $WORKING_DIR
#$SRC/scripts/add_scope_att_hc_parent_total.sh $WORKING_DIR $RUNX
$SRC/scripts/learn_scopes_total.sh $WORKING_DIR $RUN $RUNX
cat $WORKING_DIR/logs/log.total.$RUN.$RUNX  

