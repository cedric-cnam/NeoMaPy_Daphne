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