
# Agrega atributos relacionados con la sintaxis
# uso add_scope_att_hc_parent.sh {$BIOSCOPE | $BIOSCOPED}

WORKING_DIR=$1

# Agrego hc parent
echo "$0: Adding syntax  atributtes..."
#cat $SRC/scripts/add_scope_att_hc_parent.sql | sqlite3 $WORKING_DIR/bioscope.db  2>/dev/null
python $SRC/scripts/add_scope_att_hc_parent.py $WORKING_DIR


