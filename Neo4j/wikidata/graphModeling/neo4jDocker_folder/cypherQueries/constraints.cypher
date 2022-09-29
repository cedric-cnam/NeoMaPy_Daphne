//Temporal Uncertain Rules
//Strict Temporal Consistency
MATCH (s:Concept) <-[:s]- (tf1:TF) -[:o]-> (o:Concept), (tf1)-[:p]->(p:Concept), (s) <--(tf2:TF) --> (o), (tf2) --> (p)
WHERE tf1 <> tf2 AND (tf1.date_end < tf2.date_start OR tf2.date_end < tf1.date_start)
MERGE (tf1) -[:conflict{type:"C0"}]- (tf2);

//C1 - birthDateConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P569"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start <> tf2.date_start
MERGE (tf1) -[:conflict{type:"C1"}]- (tf2);

//C2 - deathDateConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P569"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start < tf2.date_start
MERGE (tf1) -[:conflict{type:"C2"}]- (tf2);

//C3 - birthDeathConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P570"}) -[:s]-> (s:Concept)
WHERE (tf1.date_start > tf2.date_start
  OR tf1.date_start + duration({years: 150}) <= tf2.date_start)
MERGE (tf1) -[:conflict{type:"C3"}]- (tf2);

//C4 - birthPlayerConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start > tf2.date_start
MERGE (tf1) -[:conflict{type:"C4"}]- (tf2);

//C5 - deathPlayerConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start < tf2.date_start
MERGE (tf1) -[:conflict{type:"C5"}]- (tf2);

//C6 - playerAgeConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start + duration({years: 16}) > tf2.date_start
MERGE (tf1) -[:conflict{type:"C6"}]- (tf2);

//C7 - playerTooOldConflict
MATCH (tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  (tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start + duration({years: 50}) < tf2.date_end
MERGE (tf1) -[:conflict{type:"C7"}]- (tf2);

//C8 - twoTeamsConflict
MATCH (s:Concept)
WHERE (:TF{p:"P54"}) -[:s]->  (s)
MATCH (tf1:TF{p:"P54"}) -[:s]->  (s) <-[:s]- (tf2:TF{p:"P54"})
WHERE tf1.o <> tf2.o and ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C8"}]- (tf2);

//C14 - marriageConflict
MATCH p1=(tf1:TF{p:"P26"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.o <> tf2.o AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end)
    OR (tf1.date_start = tf2.date_start and tf1.date_end = tf2.date_end))
MERGE (tf1) -[:conflict{type:"C14"}]- (tf2);

//C16 - birthMarriageConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.date_start > tf2.date_start
MERGE (tf1) -[:conflict{type:"C16"}]- (tf2);

//C17 - deathMarriageConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.date_start < tf2.date_start
MERGE (tf1) -[:conflict{type:"C17"}]- (tf2);

//C18 - playerCoachConflict
MATCH p1=(tf1:TF{p:"P54"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P286"}) -[:o]-> (s:Concept)
WHERE
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C18"}]- (tf2);

//C19 - twoCompaniesConflict
MATCH p1=(tf1:TF{p:"P108"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P108"}) -[:s]-> (s:Concept)
WHERE tf1.o <> tf2.o AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C19"}]- (tf2);
