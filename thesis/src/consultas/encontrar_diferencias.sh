# Encuentra oraciones que no fueron parseadas comparando con genia
grep -c 'ROOT' $BIOSCOPE/parsed/*.parsed | sed 's/\.parsed//g' | sed 's/:/ /' | sed 's/^.*parsed\///' | sort > lines_parsed.txt
wc -l $BIOSCOPE/genia_articles/*.genia | sed 's/\.genia//g' | sed 's/\/.*articles\///' | grep -v total | awk '{print $2,$1}' | sort > lines_genia.txt
TO_DELETE=`paste lines_genia.txt lines_parsed.txt | egrep -v '^(a[0-9]*) ([0-9]*)	\1 \2' | awk '{print $1}' | sed 's/$/.parsed/'`
echo $TO_DELETE
#cd $BIOSCOPE/parsed
#rm $TO_DELETE
