//mapping_Neo4j_wikidata
MATCH (s:Concept) <-[:s]-(tf1:TF)-[:o]->(o:Concept), (tf1)-[:p]->(p:Concept)
where tf1.ID is not null
RETURN id(tf1) as Node_id, tf1.ID as wikiID, s.ID as s, o.ID as o, p.ID as p, tf1.weight AS weight, apoc.temporal.format(tf1.date_start, "yyyyMM") as date_start, apoc.temporal.format(tf1.date_end, "yyyyMM") as date_end, tf1.polarity as polarity
ORDER BY Node_id ASC;

//inferredNodes
MATCH p= (tf1:TF) -[:rule*]-> (:TF)
UNWIND [n in nodes(p) WHERE id(n)<>id(tf1) | id(n)] as ids
RETURN id(tf1) as Node_id, collect(distinct ids) as Inferred_node_ids;

//tCon_noConflicts_threshold_0
MATCH (tf1:TF)
WHERE NOT (tf1) -[:conflict]- (:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight;

//tCon_conflicts_threshold_0
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//pCon_noConflicts_threshold_0
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf:TF)
WHERE c.pCon<>true OR c.pInc is not null OR c.tInc is not null OR c.type <> "TC1"
WITH distinct id(tf1) AS Node_id, collect(id(tf)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//pCon_conflicts_threshold_0
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc is not null OR c.tInc is not null OR c.type <> "TC1"
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//pInc_noConflicts_threshold_0
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc is not null OR c.type <> "TC1"
WITH distinct id(tf1) AS Node_id, collect(id(tf)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//pInc_conflicts_threshold_0
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc is not null OR c.type <> "TC1"
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//tInc_noConflicts_threshold_0
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc<>true OR c.type <> "TC1"
WITH distinct id(tf1) AS Node_id, collect(id(tf)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//tInc_conflicts_threshold_0
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc<>true OR c.type <> "TC1"
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;



//tCon_noConflicts_threshold_0.5
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[:conflict]- (tf2:TF)
WHERE tf2.weight > 0.5
WITH id(tf1) as Node_id, tf1.weight as weight, count(distinct tf2) as nb_conflicts
WHERE weight > 0.5 and nb_conflicts =0
RETURN Node_id, weight;

//tCon_conflicts_threshold_0.5
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE tf1.weight > 0.5 AND tf2.weight > 0.5
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//pCon_noConflicts_threshold_0.5
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf2:TF)
WHERE (c.pCon<>true OR c.pInc is not null OR c.tInc is not null OR c.type <> "TC1") AND tf1.weight > 0.5 AND tf2.weight > 0.5
WITH distinct id(tf1) AS Node_id, collect(id(tf2)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//pCon_conflicts_threshold_0.5
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc is not null OR c.tInc is not null OR c.type <> "TC1" AND tf1.weight > 0.5 AND tf2.weight > 0.5
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//pInc_noConflicts_threshold_0.5
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc is not null OR c.type <> "TC1" AND tf1.weight > 0.5 AND tf2.weight > 0.5
WITH distinct id(tf1) AS Node_id, collect(id(tf2)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//pInc_conflicts_threshold_0.5
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc is not null OR c.type <> "TC1" AND tf1.weight > 0.5 AND tf2.weight > 0.5
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//tInc_noConflicts_threshold_0.5
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc<>true OR c.type <> "TC1" AND tf1.weight > 0.5 AND tf2.weight > 0.5
WITH distinct id(tf1) AS Node_id, collect(id(tf2)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//tInc_conflicts_threshold_0.5
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc<>true OR c.type <> "TC1" AND tf1.weight > 0.5 AND tf2.weight > 0.5
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;




//tCon_noConflicts_threshold_1
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[:conflict]- (tf2:TF)
WHERE tf2.weight > 1
WITH id(tf1) as Node_id, tf1.weight as weight, count(distinct tf2) as nb_conflicts
WHERE weight > 1 and nb_conflicts =0
RETURN Node_id, weight;

//tCon_conflicts_threshold_1
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE tf1.weight > 1 AND tf2.weight > 1
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//pCon_noConflicts_threshold_1
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf2:TF)
WHERE (c.pCon<>true OR c.pInc is not null OR c.tInc is not null OR c.type <> "TC1") AND tf1.weight > 1 AND tf2.weight > 1
WITH distinct id(tf1) AS Node_id, collect(id(tf2)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//pCon_conflicts_threshold_1
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc is not null OR c.tInc is not null OR c.type <> "TC1" AND tf1.weight > 1 AND tf2.weight > 1
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//pInc_noConflicts_threshold_1
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc is not null OR c.type <> "TC1" AND tf1.weight > 1 AND tf2.weight > 1
WITH distinct id(tf1) AS Node_id, collect(id(tf2)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//pInc_conflicts_threshold_1
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc is not null OR c.type <> "TC1" AND tf1.weight > 1 AND tf2.weight > 1
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;

//tInc_noConflicts_threshold_1
MATCH (tf1:TF)
OPTIONAL MATCH (tf1) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc<>true OR c.type <> "TC1" AND tf1.weight > 1 AND tf2.weight > 1
WITH distinct id(tf1) AS Node_id, collect(id(tf2)) as conflicts, tf1.weight AS weight
WHERE size(conflicts) =0
RETURN Node_id, weight;

//tInc_conflicts_threshold_1
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.pCon<>true OR c.pInc<>true OR c.tInc<>true OR c.type <> "TC1" AND tf1.weight > 1 AND tf2.weight > 1
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;
