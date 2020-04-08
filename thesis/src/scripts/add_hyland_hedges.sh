#Agrega atributos adicionales a las tablas ya generadas
#
# uso: add_hyland_hedges.sh {$BIOSCOPE | $BIOSCOPED}

WORKING_DIR=$1

echo "$0: Adding Hyland hedges..."
python $SRC/scripts/add_hyland_hedges.py $WORKING_DIR

