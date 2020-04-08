# Pruebo los atributos de palabras
# El archivo 100.hc.conf tiene una versión donde están todos comentados
# Descomento primero los 106

WORKING_DIR=$BIOSCOPE
ORIGINAL_FILE=100.hc.conf
LOG_FILE=$WORKING_DIR/crf_corpus/hc/final/log

prueba1=0
prueba2=0
prueba3=0
prueba4=0
prueba5=1

#cat /dev/null > $LOG_FILE

if [ $prueba1 = 1 ]; then
# Empiezo trabajando la ventana word
# Empieza con una ventana de más menos 4
echo "Prueba 1: modifico ventana de word..." >> $LOG_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana de word en 3" >>  $LOG_FILE
sed -i "" 's/^U107/#U107/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U108/#U108/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana de word en 2" >> $LOG_FILE
sed -i "" 's/^U100/#U100/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U101/#U101/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana de word en 1"  >>  $LOG_FILE
sed -i "" 's/^U102/#U102/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U103/#U103/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana de word en 0"  >>  $LOG_FILE
sed -i "" 's/^U104/#U104/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U105/#U105/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i "" 's/^U106/#U106/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo " " >> $LOG_FILE
fi


if [ $prueba2 = 1 ]; then
# Ventana lemma
# Empieza con una ventana de más menos 4
echo `date +%T` "Prueba 2: modifico ventana de lemma... " >>  $LOG_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i "" 's/^U207/#U207/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" ""'s/^U208/#U208/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana de lemma en 2" >> $LOG_FILE
sed -i "" ""'s/^U200/#U200/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" ""'s/^U201/#U201/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana de lemma en 1"  >>  $LOG_FILE
sed -i "" ""'s/^U202/#U202/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" ""'s/^U203/#U203/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana de lemma en 0"  >>  $LOG_FILE
sed -i "" ""'s/^U204/#U204/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" ""'s/^U205/#U205/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i "" ""'s/^U206/#U206/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
fi


if [ $prueba3 = 1 ]; then
# Ventana pos
# Empieza con una ventana de más menos 4
echo `date +%T` "Ventana de pos  en 4" >>  $LOG_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i "" ""'s/^U307/#U307/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" ""'s/^U308/#U308/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i "" ""'s/^U300/#U300/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" ""'s/^U301/#U301/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i "" ""'s/^U302/#U302/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" ""'s/^U303/#U303/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i "" ""'s/^U304/#U304/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" ""'s/^U305/#U305/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i "" ""'s/^U306/#U306/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
fi


if [ $prueba4 = 1 ]; then
# Ventana hc_candidate
# Empieza con una ventana de más menos 4
echo `date +%T` "Ventana de hc_candidate  en 4" >>  $LOG_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i "" ""'s/^U407/#U407/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U408/#U408/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i "" 's/^U400/#U400/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U401/#U401/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i "" 's/^U402/#U402/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U403/#U403/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i "" 's/^U404/#U404/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U405/#U405/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i "" 's/^U406/#U406/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
fi



if [ $prueba5 = 1 ]; then
# Ventana cooccurs
# Empieza con una ventana de más menos 4
echo `date +%T` "Ventana de hc_coocurrs en 4" >>  $LOG_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i "" 's/^U507/#U507/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U508/#U508/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i "" 's/^U500/#U500/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U501/#U501/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i "" 's/^U502/#U502/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U503/#U503/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i "" 's/^U504/#U504/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
sed -i "" 's/^U505/#U505/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i "" 's/^U506/#U506/' $WORKING_DIR/crf_corpus/hc/final/$ORIGINAL_FILE
./learn_hedge_cues_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
fi











