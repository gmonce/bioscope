
# Agrega atributos relacionados con la sintaxis
# uso add_scope_att_hc_parent_total.sh {$BIOSCOPE | $BIOSCOPED}

WORKING_DIR=$1
RUNX=$2

# Agrego hc parent
echo "$0: Adding syntax  atributtes..."
cat add_scope_att_hc_parent.sql | sqlite3 $WORKING_DIR/bioscope.db 2>/dev/null
python add_scope_att_hc_parent.py $WORKING_DIR $RUNX Y
echo "$0: Updating scope2..."
python update_scope_2.py $WORKING_DIR $RUNX Y
echo "$0: Updating passive voice..."
python $SRC/scripts/add_passive_voice.py $WORKING_DIR Y

