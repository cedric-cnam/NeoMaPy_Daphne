//mapping_Neo4j_wikidata
MATCH (s:Concept) <-[:s]-(tf1:TF)-[:o]->(o:Concept), (tf1)-[:p]->(p:Concept)
where tf1.ID is not null
RETURN id(tf1) as Node_id, tf1.ID as wikiID, s.ID as s, o.ID as o, p.ID as p, tf1.weight AS weight, apoc.temporal.format(tf1.date_start, "yyyyMM") as date_start, apoc.temporal.format(tf1.date_end, "yyyyMM") as date_end, tf1.polarity as polarity
ORDER BY Node_id ASC;

//inferredNodes
MATCH p= (tf1:TF) -[:rule*]-> (:TF)
UNWIND [n in nodes(p) WHERE id(n)<>id(tf1) | id(n)] as ids
RETURN id(tf1) as Node_id, collect(distinct ids) as Inferred_node_ids;

//noConflicts
MATCH (tf1:TF)
WHERE NOT (tf1) -[:conflict]- (:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight;

//n-rockit_temporal_conflicts
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.type = "C0"
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids;

//conflicts
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
WHERE c.type <> "C0"
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;
