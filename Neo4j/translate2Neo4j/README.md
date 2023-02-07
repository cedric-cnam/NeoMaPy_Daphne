## Translate2Neo4j

This Java program transforms data from Wikidata provided to be used by *n-rockit* to model a TMLN. The program provides CSV files with corresponding attributes used in NeoMaPyGraph (on *Neo4j*)

Some parameters can be used to process files and extend the TMLN:
- *--input=* gives the input folder location
- *--output=* gives the ouput folder location
- *--ratio=* set the ratio of negative polarities (initially n-rockit cannot process negative polarities in TMLN). Default is 0.05 (5%)
- *--lowWeight=* are negative polarities picked up from low weights TF? (true/false)

Data must be put in the "../data/input/" folder



### Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
