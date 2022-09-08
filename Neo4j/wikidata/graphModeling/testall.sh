for f in $(ls ~/Library/Application\ Support/Neo4j\ Desktop/Application/relate-data/dbmss/dbms-3b0e1ab2-d23e-4f05-a18e-78c491411645/import);\
do \
  java -jar graphModeling.jar --inputFile=$f --inference=false; \
  java -jar graphModeling.jar --inputFile=$f --inference=true --noDelete; \
done;
