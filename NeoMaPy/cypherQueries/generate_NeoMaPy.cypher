//Drop Database
MATCH (n)
OPTIONAL MATCH (n) -[r]- ()
DELETE n, r;

//indices
CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON c.ID;
CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON c.name;
CREATE INDEX IF NOT EXISTS FOR (t:TF) ON t.ID;
CREATE INDEX IF NOT EXISTS FOR (t:TF) ON t.date_start;
CREATE INDEX IF NOT EXISTS FOR (t:TF) ON t.date_end;
CREATE INDEX IF NOT EXISTS FOR (t:TF) ON t.polarity;
CREATE INDEX IF NOT EXISTS FOR (t:TF) ON t.s;
CREATE INDEX IF NOT EXISTS FOR (t:TF) ON t.o;
CREATE INDEX IF NOT EXISTS FOR (t:TF) ON t.p;

//Load CSV
LOAD CSV WITH HEADERS FROM "file:/pinstConf_rockit_wikidata_10_5k_polarity_0.05.csv" as l FIELDTERMINATOR ';'
WITH l WHERE datetime(l.date_start) <= datetime(l.date_end)
MERGE (ID_s:Concept{ID:l.ID_s})
MERGE (ID_o:Concept{ID:l.ID_o})
MERGE (ID_p:Concept{ID:l.ID_p})
MERGE (tf:TF{ID:l.ID_TF,date_start:datetime(l.date_start),date_end:datetime(l.date_end),weight:toFloat(l.proba),valid:toBoolean(l.valid),polarity:toBoolean(l.polarity),
	p:l.ID_p, o:l.ID_o, s:l.ID_s})
MERGE (ID_s) <-[:s]- (tf)
MERGE (ID_o) <-[:o]- (tf)
MERGE (ID_p) <-[:p]- (tf);

//Concept names
MERGE(ID_b:Concept{ID:"P569"}) ON MATCH SET ID_b.name = "birthDate";
MERGE(ID_d:Concept{ID:"P570"}) ON MATCH SET ID_d.name = "deathDate";
MERGE(ID_t:Concept{ID:"P54"}) ON MATCH SET ID_t.name = "teamPlayer";
MERGE(ID_c:Concept{ID:"P286"}) ON MATCH SET ID_c.name = "teamCoach";
MERGE(ID_m:Concept{ID:"P26"}) ON MATCH SET ID_m.name = "marriage";
MERGE(ID_w:Concept{ID:"P108"}) ON MATCH SET ID_w.name = "workCompany";

MATCH (o) <-[:o]- (:TF) -[:p]-> (c:Concept), (s) <-[:s]- (t)
WHERE c.name = "teamCoach"
SET o.name = "Person"
SET s.name = "Team";

MATCH (o) <-[:o]- (:TF) -[:p]-> (c:Concept), (s) <-[:s]- (t)
WHERE c.name = "marriage"
SET o.name = "Person"
SET s.name = "Person";

MATCH (o) <-[:o]- (t:TF) -[:p]-> (c:Concept), (s) <-[:s]- (t)
WHERE c.name IN ["birthDate", "deathDate"]
SET o.name = "Date"
SET s.name = "Person";

MATCH (o) <-[:o]- (:TF) -[:p]-> (c:Concept), (s) <-[:s]- (t)
WHERE c.name = "teamPlayer"
SET s.name = "Person"
SET o.name = "Team";

MATCH (o) <-[:o]- (:TF) -[:p]-> (c:Concept), (s) <-[:s]- (t)
WHERE c.name = "workCompany"
SET s.name = "Person"
SET o.name = "Company";

//Inference UncertainRule-teams-Q495299-Q3873511
MATCH p1=(c:Concept{name:"teamPlayer"}) <-[:p]- (tf1:TF) -[:s]-> (s), (tf1) -[:o]-> (o1:Concept{ID:"Q495299"}), (o2:Concept{ID:"Q3873511"})
WHERE tf1.polarity = true
UNWIND [tf1.weight, 0.9] as var_min
WITH c, s, o1, o2, tf1, min(var_min) as var_min
MERGE (c) <-[:p]- (new_tf:TF{
	ID:"R1_"+s.ID+"_"+o1.ID+"-"+o2.ID+"_"+tf1.ID,date_start:tf1.date_end, date_end:datetime("9999-12-01"),
	valid:true,weight:var_min, polarity:false, type:"R1", s:s.ID, o:o2.ID, p:c.ID}) -[:s]-> (s)
MERGE (new_tf) -[:o]-> (o2)
MERGE (tf1) -[:rule]-> (new_tf);

//Conflict - Partial Temporal Consistency
MATCH (tf1:TF) -[:s]-> (:Concept) <-[:s]- (tf2:TF)
WHERE tf1.p=tf2.p and tf1.o=tf2.o and tf1.polarity = true AND tf2.polarity = false AND
    (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end AND tf1.date_end < tf2.date_end)
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.pCon=true
ON MATCH SET c.pCon=true;

//Conflict - Partial Temporal Inconsistency
MATCH (tf1:TF) -[:s]-> (:Concept) <-[:s]- (tf2:TF)
WHERE tf1.p=tf2.p and tf1.o=tf2.o and tf1.polarity = true AND tf2.polarity = false AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.pInc=true
ON MATCH SET c.pInc=true;

//Conflict - Total Temporal Inconsistency
MATCH (tf1:TF) -[:s]-> (:Concept) <-[:s]- (tf2:TF)
WHERE tf1.p=tf2.p and tf1.o=tf2.o and tf1.polarity = true AND tf2.polarity = false AND
    (tf1.date_start = tf2.date_start and tf1.date_end = tf2.date_end)
MERGE (tf1) -[c:conflict]- (tf2)
ON CREATE SET c.type="TC1", c.tInc=true
ON MATCH SET c.tInc=true;

//Conflict - C1 - birthDateConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P569"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start <> tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C1"}]- (tf2);

//Conflict - C1_1 - birthDateConflictPolarity
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P569"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
MERGE (tf1) -[:conflict{type:"C1_1"}]- (tf2);

//Conflict - C2 - deathDateConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P570"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C2"}]- (tf2);

//Conflict - C2_1 - deathDateConflictPolarity
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P570"}) -[:s]-> (s:Concept)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
MERGE (tf1) -[:conflict{type:"C2_1"}]- (tf2);

//Conflict - C3 - birthDeathConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P570"}) -[:s]-> (s:Concept)
WHERE (tf1.date_start > tf2.date_start OR tf1.date_start + duration({years: 150}) <= tf2.date_start)
  AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C3"}]- (tf2);

//Conflict - C4_1 - birthPlayerConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2:TF) -[:s]-> (s:Concept)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C4_1"}]- (tf2);

//Conflict - C4_2 - birthPlayerConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C4_2"}]- (tf2);

//Conflict - C5 - deathPlayerConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C5"}]- (tf2);

//Conflict - C6 - playerAgeConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start + duration({years: 16}) > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C6"}]- (tf2);

//Conflict - C7 - playerTooOldConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start + duration({years: 50}) < tf2.date_end AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C7"}]- (tf2);

//Conflict - C8 - twoTeamsConflict
MATCH (tf1:TF{p:"P54", polarity:true}) -[:s]->  (s) <-[:s]- (tf2:TF{p:"P54", polarity:true})
WHERE tf1.o <> tf2.o and ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C8"}]- (tf2);

//Conflict - C14 - marriageConflict
MATCH p1=(tf1:TF{p:"P26"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.o <> tf1.o AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end)
    OR (tf1.date_start = tf2.date_start and tf1.date_end = tf2.date_end))
MERGE (tf1) -[:conflict{type:"C14"}]- (tf2);

//Conflict - C16 - birthMarriageConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C16"}]- (tf2);

//Conflict - C17 - deathMarriageConflict
MATCH p1=(tf1:TF{p:"P570"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P26"}) -[:s]-> (s:Concept)
WHERE tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C17"}]- (tf2);

//Conflict - C18 - playerCoachConflict
MATCH p1=(tf1:TF{p:"P54"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P286"}) -[:o]-> (s:Concept)
WHERE tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C18"}]- (tf2);

//Conflict - C19 - twoCompaniesConflict
MATCH p1=(tf1:TF{p:"P108"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P108"}) -[:s]-> (s:Concept)
WHERE tf1.o <> tf2.o AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C19"}]- (tf2);



//Weighted Rule - C6-1 - playerAgeConflict
MATCH p1=(tf1:TF{p:"P569"}) -[:s]-> (s:Concept),
  p2=(tf2:TF{p:"P54"}) -[:s]-> (s:Concept)
WHERE tf1.date_start + duration({years: 16}) > tf2.date_start AND tf1.date_start + duration({years: 14}) < tf2.date_start
  AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C6", weight:0.5}]- (tf2);
