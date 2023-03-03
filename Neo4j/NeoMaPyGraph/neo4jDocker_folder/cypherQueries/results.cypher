//mapping_Neo4j_wikidata
MATCH (s:Concept) <-[:s]-(tf1:TF)-[:o]->(o:Concept), (tf1)-[:p]->(p:Concept)
where tf1.ID is not null
RETURN id(tf1) as Node_id, tf1.ID as wikiID, s.ID as s, o.ID as o, p.ID as p, tf1.weight AS weight, apoc.temporal.format(tf1.date_start, "yyyyMM") as date_start, apoc.temporal.format(tf1.date_end, "yyyyMM") as date_end, tf1.polarity as polarity, valid
ORDER BY Node_id ASC;

//noConflicts
MATCH (tf1:TF)
WHERE NOT (tf1) -[:conflict]- (:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight;

//conflicts
MATCH (tf1:TF) -[c:conflict]- (tf2:TF)
RETURN id(tf1) AS Node_id, tf1.weight AS weight, collect(distinct id(tf2)) AS Conflicts_node_ids
ORDER BY size(Conflicts_node_ids) DESC, Node_id ASC;
