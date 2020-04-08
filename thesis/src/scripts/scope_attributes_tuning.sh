# Pruebo los atributos de los scopes
# El archivo 100.scope.conf tiene una versión igual a la mejor hasta el momento

WORKING_DIR=$BIOSCOPE
ORIGINAL_FILE=100.scope.conf
LOG_FILE=$WORKING_DIR/crf_corpus/scope/final/log

prueba1=0
prueba2=0
prueba3=0
prueba4=0
prueba5=0
prueba6=0
prueba7=0
prueba8=0
prueba9=0
prueba10=1


#cat /dev/null > $LOG_FILE

# Empiezo trabajando la ventana word
if [ $prueba1 = 1 ]; then
echo "---">> $LOG_FILE
echo "Prueba 1: modifico ventana de  hedge cues, primero en 4..." >> $LOG_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana de en 3" >>  $LOG_FILE
sed -i " " 's/^U08/#U08/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U09/#U09/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana de en 2" >> $LOG_FILE
sed -i " " 's/^U06/#U06/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U07/#U07/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana de en 1"  >>  $LOG_FILE
sed -i " " 's/^U01/#U01/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U05/#U05/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i " " 's/^U02/#U02/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U04/#U04/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i " " 's/^U03/#U03/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo " " >> $LOG_FILE
fi



# parent scope
if [ $prueba2 = 1 ]; then
echo "---" >> $LOG_FILE
echo "Prueba 2: modifico ventana de  parent scope, primero en 4..." >> $LOG_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i " " 's/^U108/#U108/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U109/#U109/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i " " 's/^U106/#U106/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U107/#U107/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i " " 's/^U101/#U101/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U105/#U105/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i " " 's/^U102/#U102/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U104/#U104/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i " " 's/^U103/#U103/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo " " >> $LOG_FILE
fi


# gparent scope
if [ $prueba3 = 1 ]; then
echo "---"
echo "Prueba 3: modifico ventana de  gparent scope, primero en 4..." >> $LOG_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i " " 's/^U208/#U208/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U209/#U209/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i " " 's/^U206/#U206/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U207/#U207/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i " " 's/^U201/#U201/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U205/#U205/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i " " 's/^U202/#U202/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U204/#U204/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i " " 's/^U203/#U203/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo " " >> $LOG_FILE
fi

# ggparent scope
if [ $prueba4 = 1 ]; then
echo "---"
echo "Prueba 4: modifico ventana de  gparent scope, primero en 4..." >> $LOG_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i " " 's/^U308/#U308/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U309/#U309/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i " " 's/^U306/#U306/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U307/#U307/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i " " 's/^U301/#U301/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U305/#U305/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i " " 's/^U302/#U302/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U304/#U304/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i " " 's/^U303/#U303/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo " " >> $LOG_FILE
fi

# lemma
if [ $prueba5 = 1 ]; then
echo "---"
echo "Prueba 5: modifico ventana de  lemma, primero en 4..." >> $LOG_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i " " 's/^U408/#U408/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U409/#U409/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i " " 's/^U406/#U406/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U407/#U407/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i " " 's/^U401/#U401/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U405/#U405/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i " " 's/^U402/#U402/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U404/#U404/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i " " 's/^U403/#U403/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo " " >> $LOG_FILE
fi

# pos
if [ $prueba6 = 1 ]; then
echo "---"
echo "Prueba 6: modifico ventana de  pos, primero en 4..." >> $LOG_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i " " 's/^U508/#U508/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U509/#U509/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i " " 's/^U506/#U506/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U507/#U507/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i " " 's/^U501/#U501/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U505/#U505/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i " " 's/^U502/#U502/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U504/#U504/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i " " 's/^U503/#U503/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo " " >> $LOG_FILE
fi



# nextS
if [ $prueba7 = 1 ]; then
echo "---"
echo "Prueba 7: modifico ventana de  nextS, primero en 4..." >> $LOG_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 3" >>  $LOG_FILE
sed -i " " 's/^U608/#U608/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U609/#U609/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 2" >> $LOG_FILE
sed -i " " 's/^U606/#U606/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U607/#U607/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo `date +%T` "Ventana en 1"  >>  $LOG_FILE
sed -i " " 's/^U601/#U601/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U605/#U605/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Ventana en 0"  >>  $LOG_FILE
sed -i " " 's/^U602/#U602/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
sed -i " " 's/^U604/#U604/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo echo `date +%T`  "Sin el atributo"  >>  $LOG_FILE
sed -i " " 's/^U603/#U603/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
echo " " >> $LOG_FILE
fi


if [ $prueba8 = 1 ]; then
echo "---"
echo "Prueba 8a: elimino el pos del padre"
sed -i " " 's/^U1001/#U1001/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
fi

if [ $prueba9 = 1 ]; then
echo "---"
echo "Prueba 8a: elimino el pos del gparent"
sed -i " " 's/^U1002/#U1002/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
fi

if [ $prueba10 = 1 ]; then
echo "---"
echo "Prueba 8a: elimino el pos del ggparent"
sed -i " " 's/^U1003/#U1003/' $WORKING_DIR/crf_corpus/scope/final/$ORIGINAL_FILE
./learn_scopes_tuning.sh $WORKING_DIR $ORIGINAL_FILE $LOG_FILE
fi



