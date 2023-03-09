//delete nodes
MATCH (n)
OPTIONAL MATCH (n) -[r]- ()
DELETE n, r;

MATCH (n) -[r:conflict{type:"C0"}]- ()
DELETE r;
