#!/bin/bash
for i in $(cat PokemonList.txt| grep '\n')
	do
		q=$(echo $i|tr -d '\r')
		mkdir /home/Kanto/Pokemon/$q
		#rm -r /home/abkmp/dirTest/$i
		done

