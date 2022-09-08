for f in $(ls /var/lib/neo4j/import);\
do \
  java -jar graphModeling.jar --inputFile=$f --inference=false; \
  java -jar graphModeling.jar --inputFile=$f --inference=true --noDelete; \
  sleep 5; \
done;
