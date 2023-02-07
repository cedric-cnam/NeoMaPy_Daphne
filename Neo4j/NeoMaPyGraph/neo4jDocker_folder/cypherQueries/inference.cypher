//UncertainRule-teams-Q495299-Q3873511
MATCH p1=(c:Concept{name:"teamPlayer"}) <-[:p]- (tf1:TF) -[:s]-> (s), (tf1) -[:o]-> (o1:Concept{ID:"Q495299"}), (o2:Concept{ID:"Q3873511"})
WHERE tf1.polarity = true
UNWIND [tf1.weight, 0.9] as var_min
WITH c, s, o1, o2, tf1, min(var_min) as var_min
MERGE (c) <-[:p]- (new_tf:TF{
	ID:"R1_"+s.ID+"_"+o1.ID+"-"+o2.ID+"_"+tf1.ID,date_start:tf1.date_end, date_end:datetime("9999-12-01"),
	valid:true,weight:var_min, polarity:false, type:"R1", s:s.ID, o:o2.ID, p:c.ID}) -[:s]-> (s)
MERGE (new_tf) -[:o]-> (o2)
MERGE (tf1) -[:rule]-> (new_tf);
