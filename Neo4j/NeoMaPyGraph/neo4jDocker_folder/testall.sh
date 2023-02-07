#!/bin/sh
cd /root
for f in $(ls /var/lib/neo4j/import/$1);\
do \
  date; >> log \
  java -jar graphModeling.jar --inputFile=$f --inference=false; >> log \
  date; \
#  java -jar graphModeling.jar --inputFile=$f --inference=true --noDelete; >> log \
#  tail -n 10 log; \
#  date ; sleep 5; \
done;
