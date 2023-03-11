#!/bin/sh
export folder=$1
for f in $(ls -t $folder);\
do
	echo "============== $f ==============";
	cp $folder/$f/withoutInference/*.zip .;
	unzip -oq mapping_Neo4j_wikidata.zip;
	unzip -oq conflicts.zip;
	unzip -oq noConflicts.zip;
	./mapy.sh conflicts.json noConflicts.json
	mkdir $f
	mv conflicts.json $f/
	mv noConflicts.json $f/
	mv mapping_Neo4j_wikidata.json $f/
	mv statistics_MaPy.txt $f/
	mv dicoConf.json $f/
	mv dicoNoConf.json $f/
	mv listOfDico.json $f/
	mv solutions_MaPy.txt $f/
	zip -q $f.zip $f/*
	mv $f.zip output/
	rm -rf $f
done;
