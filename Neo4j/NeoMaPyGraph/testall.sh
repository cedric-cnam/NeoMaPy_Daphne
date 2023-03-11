#!/bin/sh
sudo chmod 777 neo4jDocker_import;
for f in $(cd neo4jDocker_import;ls -Sr $1);\
do \
  docker-compose down;
  docker-compose up &
  echo "wait docker container for '$f'";
  sleep 45;
  sudo docker exec -it neo4j_graphModeling bash -c "/root/testall.sh $f"
#  java -jar graphModeling.jar --inputFile=$f --inference=true --noDelete; >> log \
#  tail -n 10 log; \
#  date ; sleep 5; \
done;
