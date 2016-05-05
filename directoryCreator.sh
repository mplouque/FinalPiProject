#!/bin/bash
for i in $(cat PokemonList.txt)
	do
		echo $i
		q=$(echo $i|tr -d '\r')
		#echo $q
		mkdir /home/Kanto/Pokemon/$q
		#mkdir /home/abkmp/testing/$q
		#rm -r /home/abkmp/dirTest/$i
		done

