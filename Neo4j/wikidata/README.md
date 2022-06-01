


### stats on conflicts
Each rule generates **conflict relationships** "type = Cx" (x is the rule number) and "error" is the name. To watch existing conflicts:
```
MATCH p= () -[:conflict]- ()
RETURN p
LIMIT 20
```

```
MATCH () -[c:conflict]- ()
RETURN c.type, c.error, count(distinct c)
```

#### Potential Conflict example
Count number of conflict types
```
MATCH (c:Concept{ID:"Q10869"}) <-[:s]- (tf1:TF) -[:p]-> (tp:Concept{name:"teamPlayer"}),
    (c) <-[:s]- (tf2:TF) -[:p]-> (tp)
OPTIONAL MATCH (tf1) -[conf:conflict]-> (tf2)
RETURN conf.type, count(distinct tf1)
```

Extract the TF graph with and without conflicts
```
MATCH (c:Concept{ID:"Q10869"}) <-[:s]- (tf1:TF) -[:p]-> (tp:Concept{name:"teamPlayer"}), o1 = (tf1) -[:o]-> (),
    (c) <-[:s]- (tf2:TF) -[:p]-> (tp),  o2 = (tf2) -[:o]-> ()
OPTIONAL MATCH (tf1) -[conf:conflict]-> (tf2)
RETURn tf1, tf2, conf, o1, o2
```

Extract conflict graph
```
MATCH (c:Concept{ID:"Q10869"}) <-[:s]- (tf1:TF) -[:p]-> (tp:Concept{name:"teamPlayer"}),
    (c) <-[:s]- (tf2:TF) -[:p]-> (tp), (tf1) -[conf:conflict]-> (tf2)
RETURN tf1.ID, tf1.weight, tf2.ID, tf2.weight
```

extract inscreasing conflict nodes
```
MATCH (c:Concept{ID:"Q10869"}) <-[:s]- (tf1:TF) -[:p]-> (tp:Concept{name:"teamPlayer"}),
    (c) <-[:s]- (tf2:TF) -[:p]-> (tp), (tf1) -[conf:conflict]-> (tf2)
RETURN tf1.ID, count(*) as NB, collect(tf2.ID) AS conflicts
ORDER BY NB ASC
```

### Subject nodes
```
MATCH (s:Concept) <-[:s]- () RETURN distinct s.ID
```

Avg nb of conflicts per node (for TeamPlayer)
```
MATCH (c:Concept) <-[:s]- (tf1:TF) -[:p]-> (tp:Concept{name:"teamPlayer"}),
    (c) <-[:s]- (tf2:TF) -[:p]-> (tp), (tf1) -[conf:conflict]-> (tf2)
WITH c, count(distinct conf) as NB
RETURN avg(NB)
```

## Temporal Uncertain Rules

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
