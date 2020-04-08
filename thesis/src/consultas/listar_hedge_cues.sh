# Lista las hedge cues en el xml
egrep -o '<cue type="speculation" ref="X[0-9\.]*">[a-zA-Z ]*</cue>' $BIOSCOPE/abstracts.xml | grep -o '>.*<' | sed 's/[<>]//g' | sort | uniq -c | sort -r 
