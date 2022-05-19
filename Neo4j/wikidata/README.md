# Creation of the sample
## Create indices to make the creation/search efficient. For this, use ID
```
CREATE INDEX ON :Concept(ID);
CREATE INDEX ON :TF(ID);
```

## Graph instanciation

File to load the CSV file provided by the *wikidata_extractor* Java program. The file has to be put in the "*import*" folder of your Neo4j database.

```
LOAD CSV WITH HEADERS FROM "file:/pinstConf_rockit_wikidata_0_5k.csv" as l FIELDTERMINATOR ';'
MERGE (ID_s:Concept{ID:l.ID_s})
MERGE (ID_o:Concept{ID:l.ID_o})
MERGE (ID_p:Concept{ID:l.ID_p})
MERGE (tf:TF{ID:l.ID_TF,date_start:datetime(l.date_start),date_end:datetime(l.date_end),weight:toFloat(l.proba),valid:l.valid,polarity:l.polarity})
MERGE (ID_s) <-[:s]- (tf)
MERGE (ID_o) <-[:o]- (tf)
MERGE (ID_p) <-[:p]- (tf)
```

Nodes **Concept** are created with *ID*. Merge creates only if the nodes (with this id) does not exists
Creates **TF** relationships between *concepts* (use IDs to find them). The time interval and the weight is associated to this relationship

Specific objects extracted from "tsub_map.mln"
```
MERGE(ID_b:Concept{ID:"P569"}) ON MATCH SET ID_b.name = "birthDate"
MERGE(ID_d:Concept{ID:"P570"}) ON MATCH SET ID_d.name = "deathDate"
MERGE(ID_t:Concept{ID:"P54"}) ON MATCH SET ID_t.name = "teamPlayer"
MERGE(ID_c:Concept{ID:"P286"}) ON MATCH SET ID_t.name = "teamCoach"
MERGE(ID_m:Concept{ID:"P26"}) ON MATCH SET ID_m.name = "marriage"
MERGE(ID_w:Concept{ID:"P108"}) ON MATCH SET ID_w.name = "workCompany"
```

# **Rules** implementation for inference

**TO BE MODIFIED**

## R1
Match: pattern of the rule to find. Provides different instances
WHERE: "is null" allows to apply the rule only on *true* TF (not negative is "*not = true*"
UNWIND: gather values to aggregate them (time intervals / weights)
WITH: provides the output of the previous clauses in the following (TF + intervals + weights)
MERGE: create the head of the rule + new TF + the body with links to matched pattern
```
MATCH (c1:Concept{ID:"Person"})<-[:head]-(t1:TF) -[:body]-> (x:Concept),
  (c2:Concept{ID:"LivePeriod"}) <-[:head]- (t2:TF) -[:body]-> (x), (c3:Concept{ID:"MiddleAges"}) <-[:body]- (t2),
  (c4:Concept{ID:"Studied"}) <-[:head]- (t3:TF) -[:body]-> (x), (c5:Concept{ID:"CollegeOfNavarre"}) <-[:body]- (t3)
WHERE t1.not is null AND t2.not is null and t3.not is null
UNWIND [t1.time[0], t2.time[0], t3.time[0]] as t_min
UNWIND [t1.time[1], t2.time[1], t3.time[1]] as t_max
UNWIND [t1.weight, t2.weight, t3.weight] as w_min
WITH x, t1, t2, t3, min(t_min) as t_min, max(t_max) as t_max, min(w_min) as w_min
MERGE (pf:Concept{ID:"PeasantFamily"})
MERGE (pf) <-[:head]- (R1:TF{ID:"R1_"+x.ID+"_P"+t1.ID+"_LP"+t2.ID+"_S"+t3.ID}) -[:body]-> (x)
MERGE (R1) -[:body]-> (t1)
MERGE (R1) -[:body]-> (t2)
MERGE (R1) -[:body]-> (t3)
  ON CREATE SET R1.time=[t_min, t_max], R1.weight=w_min, R1.rule=true
```
> J'ai rajouté le lien vers les TF d'origine dans le body. Je trouvais cela plus pertinent

## Disjonctive query
With several types of concepts ID (Studied OR Worked)
And a negative constraint (Renaissance)
```
MATCH (c1:Concept{ID:"Person"})<-[:head]-(t1:TF) -[:body]-> (x:Concept),
  (c2:Concept{ID:"LivePeriod"}) <-[:head]- (t2:TF) -[:body]-> (x), (c3:Concept{ID:"MiddleAges"}) <-[:head]- (t2:TF) -[:body]-> (x),
  (c4:Concept) <-[:head]- (t3:TF) -[:body]-> (x), (t3) -[:body]-> (c5:Concept{ID:"CollegeOfNavarre"})
WHERE NOT (:Concept{ID:"Renaissance"}) <-- (:TF) --> (x)
  AND t1.not is null AND t2.not is null and t3.not is null
  AND C4.ID IN ["Studied", "Worked]
UNWIND [t1.time[0], t2.time[0], t3.time[0]] as t_min
UNWIND [t1.time[1], t2.time[1], t3.time[1]] as t_max
UNWIND [t1.weight, t2.weight, t3.weight] as w_min
WITH t1, t2, t3, min(t_min) as t_min, max(t_max) as t_max, min(w_min) as w_min
MERGE (pf:Concept{ID:"PeasantFamily"})
MERGE (pf) <-[:head]- (R1:TF{ID:"R1_"+x.ID+"_P"+t1.ID+"_LP"+t2.ID+"_S"+t3.ID}) -[:body]-> (x), (R1) -[:body]-> (t1), (R1) -[:body]-> (t2), (R1) -[:body]-> (t3)
  ON CREATE SET R1.time=[t_min, t_max], R1.weight=w_min
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
MATCH (n:TF{rule:true})
OPTIONAL MATCH (n) -[r]-> ()
DELETE n, r
```

## GET the whole graph
```
MATCH (n)
OPTIONAL MATCH (n) -[r]->()
RETURN n,r
```



## stat queries
Number of triplets
```
MATCH (ns:Concept) <-[:s]- (tf:TF) -[:o]-> (no), (tf) -[:p]-> (np)
RETURN COUNT(*)
```

Nb links per node linked to "o" - 6
```
MATCH (tf:TF) -[:o]-> (no)
RETURN no.ID, count(*)
```

Nb "s" - 796
```
MATCH (tf:TF) -[:s]-> (ns)
RETURN COUNT(distinct ns)
```

nb distinct p - 1620
```
MATCH (tf:TF) -[:p]-> (np)
RETURN COUNT(distinct np)
```

Nb "p" links distribution
```
MATCH (tf:TF) -[:p]-> (np)
RETURN np.ID, count(*) as NB
ORDER BY NB DESC
```
