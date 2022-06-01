This repository contains:
- The **data** folder with the wikidata dataset provided by Chekol
- The **wikidata_extractor** folder, a Java program that transforms the dataset into a CSV file to be imported in *Neo4j*
- [GraphSetting.md](GraphSetting.md) gives the instruction to import CSV files and generate the graph database in *Neo4j*
- [Constrains.md](Constraints.md) gives the *Cypher* queries that generates all the conflicts related to expressed constraints on the dataset
- [GraphStats.md](GraphStats.md) gives the *Cypher* queries that extracts statistics from the graph database (Concepts, TF, conflicts, etc.)
- [Inference.md](Inference.md) gives the *Cypher* queries that generates new TF by inference (rules)
