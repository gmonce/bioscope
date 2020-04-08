# Script que realizar el procesamiento del corpus original y genera todos los archivos necesarios para visualizar el corpus (incluyendo imágenes)
# generate_corpus_files.sh $BIOSCOPE
# Documentado

#Opciones
REGENERAR_PARSED_FILES=1
ONLY_HEDGE_AND_NEGATION_IMAGES=0
FILENAMES_TO_PARSE='*.genia'
IMAGE_PREFIX=a
ATTRIBUTE_PREFIX=a

# Especifico el directorio y el corpus a partir de dónde generar
WORKING_DIR=$1

echo "Directorio de trabajo:" $SRC
#python $SRC/scripts/generate_txt_files.py $WORKING_DIR
#python $SRC/scripts/generate_bioscope_files.py $WORKING_DIR
#python $SRC/scripts/generate_genia_files.py $WORKING_DIR 'a*.txt' 
#python $SRC/scripts/copy_genia_event_files.py $WORKING_DIR 
#python $SRC/scripts/generate_parsed_files.py $WORKING_DIR $FILENAMES_TO_PARSE $REGENERAR_PARSED_FILES
python $SRC/scripts/generate_image_files.py $WORKING_DIR  $IMAGE_PREFIX $ONLY_HEDGE_AND_NEGATION_IMAGES
python $SRC/scripts/generate_attribute_table_files.py $WORKING_DIR $ATTRIBUTE_PREFIX
