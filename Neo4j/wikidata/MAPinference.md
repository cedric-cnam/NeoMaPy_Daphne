To compute the MAP inference, it requires to extract for each TF the list of conflicts that can be found according to a given parametric semantics.

## Examples of conflicts that can be found:

# List of conflicts with a temporality consistency
Types of temporal consistency conflicts: **pCon, pInc, tInc**

```
MATCH p=()-[r:conflict{type:"TC1"}]->()
WHERE r.pInc = true
RETURN p
LIMIT 25
```

# List of conflicts with a weight (uncertain constraint)
```
MATCH p=()-[r:conflict]->() 
WHERE r.weight > 0
RETURN p
LIMIT 25
```

# For each TF, give a simple list of conflicts
```
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf2:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) ASC, Node_id ASC
LIMIT 25
```

# For each TF, list of those with at least one conflict
```
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) ASC, Node_id ASC
LIMIT 25
```


## List of TF without any conflicts
For temporal semantics we need to take into account non temporal conflicts wrt. to the chosen semantics

tCon: nothing
pCon: OR (tf1) -[:conflict{pCon:true}]- (:TF)
pInc: OR (tf1) -[:conflict{pCon:true}]- (:TF) OR (tf1) -[:conflict{pInc:true}]- (:TF)
tInc: OR (tf1) -[:conflict{type:"TC1"}]- (:TF)
  (Any kind of temporal inconsistency is accepted)
```
MATCH (tf1:TF)
WHERE NOT (tf1) -[:conflict]- (:TF) OR (tf1) -[:conflict{pCon:true}]- (:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight
```

## List of inferred TF
Inference rules use relationships with :**body** and :**head**. If a TF is involved in a body, it can have an impact during the MAP inference (rule). We need to get the chain.
```
MATCH p= (tf1:TF) <-[:body*]- (:TF)
UNWIND [n in nodes(p) WHERE id(n)<>id(tf1) | id(n)] as ids
RETURN id(tf1), collect(distinct ids) as Inferred_node_ids
```

## Parametric semantics

tCon: *nothing*
  (every temporal conflict is kept)
pCon: *c.pCon<>true OR not exists(c.pCon)*
  (any pCon = true conflict is accepted)
pInc: *c.pInc<>true OR not exists(c.pInc)*
  (if pCon=true, then pInc=true. no need to remove then)
tInc: *c.type<>"TC1"*
  (Any kind of temporal inconsistency is accepted)

```
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pInc<>true OR not exists(c.pInc)
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) ASC, Node_id ASC
```

