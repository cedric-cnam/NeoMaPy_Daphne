//noConflicts
MATCH (tf1:TF)
WHERE NOT (tf1) -[:conflict]- (:TF) OR (tf1) -[:conflict{pCon:true}]- (:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight;

//inferredNodes
MATCH p= (tf1:TF) <-[:body*]- (:TF)
UNWIND [n in nodes(p) WHERE id(n)<>id(tf1) | id(n)] as ids
RETURN id(tf1), collect(distinct ids) as Inferred_node_ids;

//conflicts_pInc
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pInc<>true OR not exists(c.pInc)
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) ASC, Node_id ASC;