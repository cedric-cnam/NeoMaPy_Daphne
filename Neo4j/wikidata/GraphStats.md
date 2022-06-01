# Statistics on the graph content

Cypher queries to extract global information from the graph.

## Global statistics
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

## stats on conflicts
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

### Potential Conflict example
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

### Temporal Conflict
Count number of temporal inconsistency
```
MATCH (:TF) -[c:conflict{type:"TC1"}]- (:TF)
RETURN SUM(CASE WHEN c.pCon=true THEN 1 ELSE 0 END) AS nb_pCon,
    SUM(CASE WHEN c.pInc=true THEN 1 ELSE 0 END) AS nb_pInc,
    SUM(CASE WHEN c.tInc=true THEN 1 ELSE 0 END) AS nb_tInc,
    SUM(CASE WHEN c.pInc=true AND c.pCon=true THEN 1 ELSE 0 END) AS nb_pConpInc,
    COUNT(*)
```

Extract subgraph of temporal conflict
```
MATCH p=(:TF) -[:conflict{type:"TC1"}]- (:TF)
RETURN p
LIMIT 3
```

## Subject nodes
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
