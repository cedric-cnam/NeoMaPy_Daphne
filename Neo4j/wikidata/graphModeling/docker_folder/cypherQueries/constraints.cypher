//Temporal Uncertain Rules
//Partial Temporal Consistency
MATCH p1=(p:Concept) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o),
  p2=(p) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o)
WHERE tf1 <> tf2 AND tf1.polarity = true AND tf2.polarity = false AND
    (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end AND
      tf1.date_end < tf2.date_end)
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.error="TemporalConflict", c.pCon=true
ON MATCH SET c.pCon=true;

//Partial Temporal Inconsistency
MATCH p1=(p:Concept) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o),
  p2=(p) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o)
WHERE tf1 <> tf2 AND tf1.polarity = true AND tf2.polarity = false AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.error="TemporalConflict", c.pInc=true
ON MATCH SET c.pInc=true;

//Total Temporal Inconsistency
MATCH p1=(p:Concept) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o),
  p2=(p) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o)
WHERE tf1 <> tf2 AND tf1.polarity = true AND tf2.polarity = false AND
    (tf1.date_start = tf2.date_start and tf1.date_end = tf2.date_end)
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.error="TemporalConflict", c.tInc=true
ON MATCH SET c.tInc=true;

//C1
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"birthDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start <> tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C1", error:"birthDateConflict"}]- (tf2);

//C1-1
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"birthDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
MERGE (tf1) -[:conflict{type:"C1-1", error:"birthDateConflictPolarity"}]- (tf2);

//C2
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"birthDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C2", error:"deathDateConflict"}]- (tf2);

//C2-1
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"deathDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
MERGE (tf1) -[:conflict{type:"C2-1", error:"deathDateConflictPolarity"}]- (tf2);

//C3
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"deathDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE (tf1.date_start > tf2.date_start
  OR tf1.date_start + duration({years: 150}) <= tf2.date_start) AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C3", error:"birthDeathConflict"}]- (tf2);

//C4
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C4", error:"birthPlayerConflict"}]- (tf2);

//C4
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C4", error:"birthPlayerConflict"}]- (tf2);

//C5
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C5", error:"deathPlayerConflict"}]- (tf2);

//C6
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start + duration({years: 14}) > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C6", error:"playerAgeConflict"}]- (tf2);

//C7
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start + duration({years: 50}) < tf2.date_end AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C7", error:"playerTooOldConflict"}]- (tf2);

//C8
MATCH p1=(:Concept{name:"teamPlayer"}) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o1),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o2)
WHERE o1 <> o2 AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C8", error:"twoTeamsConflict"}]- (tf2);

//C14
MATCH p1=(:Concept{name:"marriage"}) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o1),
  p2=(:Concept{name:"marriage"}) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o2)
WHERE o1 <> o2 AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) 
    OR (tf1.date_start = tf2.date_start and tf1.date_end = tf2.date_end))
MERGE (tf1) -[:conflict{type:"C14", error:"marriageConflict"}]- (tf2);

//C16
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"marriage"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C16", error:"birthMarriageConflict"}]- (tf2);

//C17
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"marriage"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C17", error:"deathMarriageConflict"}]- (tf2);

//C18
MATCH p1=(:Concept{name:"teamPlayer"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamCoach"}) <-[:p]- (tf2) -[:o]-> (s)
WHERE tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C18", error:"playerCoachConflict"}]- (tf2);

//C19
MATCH p1=(:Concept{name:"workCompany"}) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o1),
  p2=(:Concept{name:"workCompany"}) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o2)
WHERE o1 <> o2 AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C19", error:"twoCompaniesConflict"}]- (tf2);

//C6
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start + duration({years: 16}) > tf2.date_start AND tf1.date_start + duration({years: 14}) < tf2.date_start
  AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C6", error:"playerAgeConflict", weight:0.5}]- (tf2);

