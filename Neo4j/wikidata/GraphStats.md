# Statistics on the graph content

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