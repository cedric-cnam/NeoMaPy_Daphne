# Import the sample

After creating a graph database on Neo4j. You might set the maximum heap memory to 4G (or more).

## Create indices to make the creation/search efficient. For this, use ID
```
CREATE INDEX ON :Concept(ID);
CREATE INDEX ON :TF(ID);
CREATE INDEX ON :Concept(name);
```

## Graph instanciation

File to load the CSV file provided by the *wikidata_extractor* Java program. The file has to be put in the "*import*" folder of your Neo4j database.
It creates **Concept**s (if not exists) and Temporal Formulas (**TF**) with a unique ID (appended values)
```
LOAD CSV WITH HEADERS FROM "file:/pinstConf_rockit_wikidata_0_5k.csv" as l FIELDTERMINATOR ';'
MERGE (ID_s:Concept{ID:l.ID_s})
MERGE (ID_o:Concept{ID:l.ID_o})
MERGE (ID_p:Concept{ID:l.ID_p})
MERGE (tf:TF{ID:l.ID_TF,date_start:datetime(l.date_start),date_end:datetime(l.date_end),weight:toFloat(l.proba),valid:toBoolean(l.valid),polarity:toBoolean(l.polarity)})
MERGE (ID_s) <-[:s]- (tf)
MERGE (ID_o) <-[:o]- (tf)
MERGE (ID_p) <-[:p]- (tf)
```

- **Date**s are typed input the system for temporal consistency computation. Since the wiki data set as no "days", the first day of the month is set
- **Weight**s corresponds to the certainty of the Temporal Formula
- **Valid** corresponds to randomly generated wrong TF (used during the validation process)
- **Polarity** corresponds to negative TF that could occur (*this field has been added automatically*)

Nodes **Concept** are created with *ID*. Merge creates only if the nodes (with this id) does not exists
Creates **TF** relationships between *concepts* (use IDs to find them). The time interval and the weight is associated to this relationship

## Specific objects extracted from "tsub_map.mln"
```
MERGE(ID_b:Concept{ID:"P569"}) ON MATCH SET ID_b.name = "birthDate"
MERGE(ID_d:Concept{ID:"P570"}) ON MATCH SET ID_d.name = "deathDate"
MERGE(ID_t:Concept{ID:"P54"}) ON MATCH SET ID_t.name = "teamPlayer"
MERGE(ID_c:Concept{ID:"P286"}) ON MATCH SET ID_c.name = "teamCoach"
MERGE(ID_m:Concept{ID:"P26"}) ON MATCH SET ID_m.name = "marriage"
MERGE(ID_w:Concept{ID:"P108"}) ON MATCH SET ID_w.name = "workCompany"
```



# Graph Management

## Delete the database
```
MATCH (n)
OPTIONAL MATCH (n) -[r]-> ()
DELETE n, r
```

Remove infered TF.
```
MATCH (n:TF)
OPTIONAL MATCH (n) -[r]-> ()
DELETE n, r
```

## GET the whole graph
```
MATCH (n)
OPTIONAL MATCH (n) -[r]->()
RETURN n,r
```
