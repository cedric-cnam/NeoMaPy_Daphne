This repository contains:
- The [**data**](data) folder with the wikidata dataset provided by Chekol
- The [**NeoMaPyGraph**](NeoMaPyGraph) folder with a Java program for automatic computation of all input graphs (see data folder), and produce different list of conflictual nodes. The setting has been put on a *Docker* environment in order to ease the installation of *Neo4j*, configurations, program execution and output files (volumes are also provided)
- The [**translate2Neo4j**](translate2Neo4j) folder, a Java program that transforms the Wikidata/Rockit dataset into a CSV file to be imported in *Neo4j*
