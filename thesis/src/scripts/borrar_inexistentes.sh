while read line
do
	echo $line
	TOTAL=`grep $line $CONLL/*xml`
	echo $TOTAL
	if [ "$TOTAL" = "" ];then
		echo $line no existe
		rm $CONLL/bioscope/$line.bioscope
		rm $CONLL/genia/$line.*.genia
		rm $CONLL/genia_articles/$line.genia
		rm $CONLL/parsed/$line.parsed
	else
		echo $line sí existe
	fi
done

