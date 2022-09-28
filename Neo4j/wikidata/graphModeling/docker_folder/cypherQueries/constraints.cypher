//Temporal Uncertain Rules
//Partial Temporal Consistency
MATCH (tf1:TF) -[:s]-> (:Concept) <-[:s]- (tf2:TF)
WHERE tf1.p=tf2.p and tf1.o=tf2.o and tf1.polarity = true AND tf2.polarity = false AND
    (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end AND tf1.date_end < tf2.date_end)
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.pCon=true
ON MATCH SET c.pCon=true;

//Partial Temporal Inconsistency
MATCH (tf1:TF) -[:s]-> (:Concept) <-[:s]- (tf2:TF)
WHERE tf1.p=tf2.p and tf1.o=tf2.o and tf1.polarity = true AND tf2.polarity = false AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.pInc=true
ON MATCH SET c.pInc=true;

//Total Temporal Inconsistency
MATCH (tf1:TF) -[:s]-> (:Concept) <-[:s]- (tf2:TF)
WHERE tf1.p=tf2.p and tf1.o=tf2.o and tf1.polarity = true AND tf2.polarity = false AND
    (tf1.date_start = tf2.date_start and tf1.date_end = tf2.date_end)
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.tInc=true
ON MATCH SET c.tInc=true;

//C1 - birthDateConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P569"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start <> tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C1"}]- (tf2);

//C1-1 - birthDateConflictPolarity
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P569"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
MERGE (tf1) -[:conflict{type:"C1-1"}]- (tf2);

//C2 - deathDateConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P569"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C2"}]- (tf2);

//C2-1 - deathDateConflictPolarity
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P570"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
MERGE (tf1) -[:conflict{type:"C2-1"}]- (tf2);

//C3 - birthDeathConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P570"}) -[:s]-> (s:Concept)
WHERE (tf1.date_start > tf2.date_start OR tf1.date_start + duration({years: 150}) <= tf2.date_start)
  AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C3"}]- (tf2);

//C4 - birthPlayerConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2:TF) -[:s]-> (s:Concept)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C4"}]- (tf2);

//C4 - birthPlayerConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C4"}]- (tf2);

//C5 - deathPlayerConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C5"}]- (tf2);

//C6 - playerAgeConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start + duration({years: 16}) > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C6"}]- (tf2);

//C7 - playerTooOldConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start + duration({years: 50}) < tf2.date_end AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C7"}]- (tf2);

//C8 - twoTeamsConflict
MATCH (s:Concept)
WHERE (:TF{p:"P54", polarity:true}) -[:s]->  (s)
MATCH (tf1:TF{p:"P54", polarity:true}) -[:s]->  (s) <-[:s]- (tf2:TF{p:"P54", polarity:true})
WHERE tf1.o <> tf2.o and ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C8"}]- (tf2)

//C14 - marriageConflict
MATCH p1=(tf1:TF{p:"P26"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.o <> tf1.o AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end)
    OR (tf1.date_start = tf2.date_start and tf1.date_end = tf2.date_end))
MERGE (tf1) -[:conflict{type:"C14"}]- (tf2);

//C16 - birthMarriageConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C16"}]- (tf2);

//C17 - deathMarriageConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C17"}]- (tf2);

//C18 - playerCoachConflict
MATCH p1=(tf1:TF{p:"P54"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P286"}) -[:o]-> (s:Concept)
WHERE tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C18"}]- (tf2);

//C19 - twoCompaniesConflict
MATCH p1=(tf1:TF{p:"P108"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P108"}) -[:s]-> (s:Concept)
WHERE tf1.o <> tf2.o AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C19"}]- (tf2);



//C6-1 - playerAgeConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start + duration({years: 16}) > tf2.date_start AND tf1.date_start + duration({years: 14}) < tf2.date_start
  AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C6", weight:0.5}]- (tf2);
