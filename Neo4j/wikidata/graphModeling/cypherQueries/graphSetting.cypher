//dataset loading
LOAD CSV WITH HEADERS FROM "file:/<<FILE>>" as l FIELDTERMINATOR ';'
MERGE (ID_s:Concept{ID:l.ID_s})
MERGE (ID_o:Concept{ID:l.ID_o})
MERGE (ID_p:Concept{ID:l.ID_p})
MERGE (tf:TF{ID:l.ID_TF,date_start:datetime(l.date_start),date_end:datetime(l.date_end),weight:toFloat(l.proba),valid:toBoolean(l.valid),polarity:toBoolean(l.polarity)})
MERGE (ID_s) <-[:s]- (tf)
MERGE (ID_o) <-[:o]- (tf)
MERGE (ID_p) <-[:p]- (tf);

//concepts name
MERGE(ID_b:Concept{ID:"P569"}) ON MATCH SET ID_b.name = "birthDate";
MERGE(ID_d:Concept{ID:"P570"}) ON MATCH SET ID_d.name = "deathDate";
MERGE(ID_t:Concept{ID:"P54"}) ON MATCH SET ID_t.name = "teamPlayer";
MERGE(ID_c:Concept{ID:"P286"}) ON MATCH SET ID_c.name = "teamCoach";
MERGE(ID_m:Concept{ID:"P26"}) ON MATCH SET ID_m.name = "marriage";
MERGE(ID_w:Concept{ID:"P108"}) ON MATCH SET ID_w.name = "workCompany";

//persons
MATCH (p) <-[:o]- (:TF) -[:p]-> (c:Concept)
WHERE c.name IN ["teamCoach", "marriage"]
SET p.name = "Person_"+p.ID;

//dates
MATCH (p) <-[:o]- (:TF) -[:p]-> (c:Concept)
WHERE c.name IN ["birthDate", "deathDate"]
SET p.name = "Date_"+p.ID;

//persons
MATCH (p) <-[:s]- (:TF) -[:p]-> (c:Concept)
WHERE c.name IN ["teamPlayer", "marriage", "workCompany", "birthDate", "deathDate"]
SET p.name = "Person_"+p.ID;