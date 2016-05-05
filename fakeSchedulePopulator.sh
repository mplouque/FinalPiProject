#!/bin/bash

for i in /home/Kanto/Pokemon/*/
	do 
		cd $i
		python /home/abkmp/Populate\ schedule.py
		python /home/abkmp/b64coder.py e schedule.csv encoded.csv
		rm schedule.csv
		mv encoded.csv ./-
		done

