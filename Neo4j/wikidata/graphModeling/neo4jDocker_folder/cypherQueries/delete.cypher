//delete nodes
MATCH (n)
OPTIONAL MATCH (n) -[r]- ()
DELETE n, r;
