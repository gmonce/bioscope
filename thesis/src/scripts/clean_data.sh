#!/bin/bash
#Limpia los datos mal generados por genia en el corpus de entrenamiento
#Así no ando tocando el árbol

#Esencialmente, lo que hace es borrar las líneas donde no tenemos Lema
#Por ahora, pasa solamente en los que empieza con una sola letra
sed '/^.*[[:space:]][[:space:]]/d' $1 > $1.temp
mv $1.temp $1

