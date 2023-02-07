## NeoMaPyGraph
**NeoMaPyGraph** is a Java Program that computes the experiments for NeoMaPy. It allows:
- The setting of a full docker environment (Neo4j, NeoMaPyGraph, config, volumes input/output)
- Import graphs from CSV files extracted by [**translate2Neo4j**](https://github.com/cedric-cnam/NeoMaPy_Daphne/tree/main/Neo4j/translate2Neo4j) and available [here](https://github.com/cedric-cnam/NeoMaPy_Daphne_Data/tree/main/translate2Neo4j)).
- Apply *Cypher* queries for rules of the TMLN (queries are given in config files in folder [*cypherQueries*](neo4jDocker_folder/cypherQueries))
- Extract conflictual nodes with different temporal consistencies (tCon, pCon, pInc, tInc). Already processed graphs are available [here](https://github.com/cedric-cnam/NeoMaPy_Daphne_Data/tree/main/NeoMaPy_Graph_export).
- The processing time and statistics of the graph are also provided

## Docker environment
To run the Docker environment
- Put your CSV files in the [*neo4jDocker_import/*](https://github.com/cedric-cnam/NeoMaPy_Daphne/tree/main/Neo4j/NeoMaPyGraph/neo4jDocker_import) folder.
- Install the [*Docker-engine*](https://www.docker.com/)
- Create the NeoMaPyGraph image : '*sudo docker-compose create*'
- Create and launch the NeoMaPyGraph container : '*sudo docker-compose up*' (other executions will be with *start* instead of *up*)
- Launch the experiments : '*./extractConflicts.sh*'. This step scan the import folder, for each it imports it, applies cypher queries, extract files, and proceed with next one
- Output files will be found in *docker_folder/output*

### Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
