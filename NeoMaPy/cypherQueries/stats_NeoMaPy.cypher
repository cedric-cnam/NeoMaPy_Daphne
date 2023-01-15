//Concepts
MATCH (c:Concept) <-- () return count(*) as NB;

//TFs
MATCH (tf:TF) -- () return count(*) as NB;

//Conflicts
MATCH p=(tf1)-[r:conflict]->(tf2) RETURN count(*) as NB;

//Inferences
MATCH p=(tf1)-[r:rule]->(tf2) RETURN count(*) as NB;
