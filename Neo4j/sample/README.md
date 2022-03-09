# Creation of the sample
## Create indices to make the creation/search efficient. For this, use ID
```
CREATE INDEX ON :Concept(ID);
CREATE INDEX ON :TF(ID);
```

## Nodes **Concept** are created with *ID*. Merge creates only if the nodes (with this id) does not exists
```
MERGE (no:Concept{ID:"NO"})
MERGE (p:Concept{ID:"Person"})
MERGE (ma:Concept{ID:"MiddleAges"})
MERGE (cn:Concept{ID:"CollegeOfNavarre"})
MERGE (phi:Concept{ID:"Philosopher"})
MERGE (lp:Concept{ID:"LivePeriod"})
MERGE (st:Concept{ID:"Studied"})
```

## Creates **TF** relationships between *concepts* (use IDs to find them). The time interval and the weight is associated to this relationship
```
MERGE (p) <-[:head]- (f1:TF{ID:"F1", time:[1320,1382], weight:1})
MERGE (f1) -[:body]-> (no)
MERGE (phi) <-[:head]- (f2:TF{ID:"F2", time:[1320,1382], weight:1})
MERGE (f2) -[:body]-> (no)
MERGE (lp) <-[:head]- (f3:TF{ID:"F3", time:[1320,1382], weight:1})
MERGE (f3) -[:body]-> (no)
MERGE (ma) <-[:body]- (f3)
MERGE (st) <-[:head]- (f4:TF{ID:"F4", time:[1340,1356], weight:0.7})
MERGE (f4) -[:body]-> (no)
MERGE (cn) <-[:body]- (f4)
MERGE (st) <-[:head]- (f5:TF{ID:"F5", not:true, time:[1350,1360], weight:0.3})
MERGE (f5) -[:body]-> (no)
MERGE (cn) <-[:body]- (f5)
MERGE (st) <-[:head]- (f6:TF{ID:"F6", not:true, time:[1350,1355], weight:0.4})
MERGE (f6) -[:body]-> (no)
MERGE (cn) <-[:body]- (f6)
```

# **Rules** implementation for inference

## R1

> ***TODO***: Need to change the rule for every instance (x.ID ?)
> ***TODO***: Integrate time intervals for validity (min weights dans unwind)
> min([t1.time[0], t2.time[0], t3.time[0]]), max([t1.time[1], t2.time[1], t3.time[1]])
```
MATCH (c1:Concept{ID:"Person"})<-[:head]-(t1:TF) -[:body]-> (x:Concept),
  (c2:Concept{ID:"LivePeriod"}) <-[:head]- (t2:TF) -[:body]-> (x), (c3:Concept{ID:"MiddleAges"}) <-[:body]- (t2),
  (c4:Concept{ID:"Studied"}) <-[:head]- (t3:TF) -[:body]-> (x), (c5:Concept{ID:"CollegeOfNavarre"}) <-[:body]- (t3)
WHERE t1.not is null AND t2.not is null and t3.not is null
UNWIND [t1.time[0], t2.time[0], t3.time[0]] as t_min
UNWIND [t1.time[1], t2.time[1], t3.time[1]] as t_max
UNWIND [t1.weight, t2.weight, t3.weight] as w_min
MERGE (pf:Concept{ID:"PeasantFamily"})
MERGE (pf) <-[:head]- (R1:TF{ID:"R1_"+x.ID+"_P"+t1.ID+"_LP"+t2.ID+"_S"+t3.ID}) -[:body]-> (x)
  ON CREATE SET R1.time=[t_min, t_max], R1.weight=w_min
```

```
MATCH (c1:Concept{ID:"Person"})<-[:head]-(t1:TF) -[:body]-> (x:Concept),
  (c2:Concept{ID:"LivePeriod"}) <-[:head]- (t2:TF) -[:body]-> (x), (c3:Concept{ID:"MiddleAges"}) <-[:head]- (t2:TF) -[:body]-> (x),
  (c4:Concept) <-[:head]- (t3:TF) -[:body]-> (x), (t3) -[:body]-> (c5:Concept{ID:"CollegeOfNavarre"})
WHERE NOT (:Concept{ID:"Renaissance"}) <-- (:TF) --> (x)
  AND C4.ID IN ["Studied", "Worked]
UNWIND min([t1.time[0], t2.time[0], t3.time[0]]) as t_min
UNWIND max([t1.time[1], t2.time[1], t3.time[1]]) as t_max
UNWIND min([t1.weight, t2.weight, t3.weight]) as w_min
MERGE (pf:Concept{ID:"PeasantFamily"})
MERGE (pf) <-[:head]- (R1:TF{ID:"R1_"+x.ID+"_P"+t1.ID+"_LP"+t2.ID+"_S"+t3.ID}) -[:body]-> (x)
  ON CREATE SET R1.time=[t_min, t_max], R1.weight=w_min
```




## Delete the database
```
MATCH (n)
OPTIONAL MATCH (n) -[r]-> ()
DELETE n, r
```
