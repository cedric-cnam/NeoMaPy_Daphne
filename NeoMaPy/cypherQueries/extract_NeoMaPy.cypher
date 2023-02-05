//Predicate nodes
MATCH (c:Concept) <-[:p]- () return c.ID as Node_id, c.name as Node_name, "p" as Node_type;

//Subject nodes
MATCH (c:Concept) <-[:s]- () return c.ID as Node_id, c.name as Node_name, "s" as Node_type;

//Object nodes
MATCH (c:Concept) <-[:o]- () return c.ID as Node_id, c.name as Node_name, "o" as Node_type;

//TF links
MATCH (tf:TF) RETURN id(tf) as neo4jID, tf.ID as Node_id, tf.date_start as date_start, tf.date_end as date_end, tf.s as s, tf.o as o, tf.p as p, tf.polarity as polarity, tf.valid as valid, tf.weight as weight;

//TF conflict links
MATCH p=(tf1)-[r:conflict]->(tf2) RETURN tf1.ID as from, tf2.ID as to, r.type as type, r.pCon as pCon, r.pInc as pInc, r.tInc as tInc;

//TF inference links
MATCH p=(tf1)-[r:rule]->(tf2) RETURN tf1.ID as from, tf2.ID as to;
