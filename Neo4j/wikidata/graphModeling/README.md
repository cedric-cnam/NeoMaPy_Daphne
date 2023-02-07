This folder runs scripts for importing the CSV file into the Neo4j database.
To remain stable, a docker environment is set.
To run the process :
- put CSV files into the *import* folder (files can be found in *Neo4j/wikidata/data/wikidata2graphModeling/pol-0.0_normalizedWeights-false_lowWeights-true*
- execute : '*sudo docker-compose create*'
- execute : '*sudo docker-compose up*'
- execute : '*./extractConflicts.sh*'. This step scan the import folder, for each it imports it, applies cypher queries, extract files, and proceed with next one
- output files will be found in *docker_folder/output*

/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
