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
> ***TODO***: Integrate time intervals for validity (weights)
> min([t1.time[0], t2.time[0], t3.time[0]]), max([t1.time[1], t2.time[1], t3.time[1]])
```
MATCH (c1:Concept{ID:"Person"})<-[:head]-(t1) -[:body]-> (x:Concept),
  (c2:Concept{ID:"LivePeriod"}) <-[:head]- (t2) -[:body]-> (x),
  (c3:Concept{ID:"Studied"}) <-[:head]- (t3) -[:body]-> (x),
  (t3) -[:body]-> (c3:Concept{ID:"CollegeOfNavarre"})
UNWIND [t1.time[0], t2.time[0], t3.time[0]] as t_min
UNWIND [t1.time[1], t2.time[1], t3.time[1]] as t_max
MERGE (pf:Concept{ID:"PeasantFamily"})
MERGE (pf) <-[:head]- (R1:TF{ID:"R1_"+x.ID, time:[0,0], weight:0.6}) -[:body]-> (x)
```
