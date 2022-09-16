//UncertainRule-teams-Q495299-Q3873511
MATCH p1=(c:Concept{name:"teamPlayer"}) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o1{ID:"Q495299"}), (o2{ID:"Q3873511"})
WHERE tf1.polarity = true
UNWIND [tf1.weight, 0.9] as var_min
WITH c, s, o2, tf1, min(var_min) as var_min
MERGE (c) <-[:p]- (new_tf:TF{date_start:tf1.date_end, date_end:datetime("9999-12-01"), valid:true,weight:var_min, polarity:false, type:"R1"}) -[:s]-> (s)
MERGE (new_tf) -[:o]-> (o2)
MERGE (tf1) -[:rule]-> (new_tf);
