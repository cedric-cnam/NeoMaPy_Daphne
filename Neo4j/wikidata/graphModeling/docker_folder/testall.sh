#!/bin/sh
# cd /root
# for f in $(ls /var/lib/neo4j/import);\

for f in $(ls /Users/ntravers/Library/Application\ Support/Neo4j\ Desktop/Application/relate-data/dbmss/dbms-3b0e1ab2-d23e-4f05-a18e-78c491411645/import)
do \
  date; >> log \
  java -jar graphModeling.jar --inputFile=$f --inference=false; >> log \
  date; tail -n 10 log; \
#  java -jar graphModeling.jar --inputFile=$f --inference=true --noDelete; >> log \
#  tail -n 10 log; \
#  date ; sleep 5; \
done;
