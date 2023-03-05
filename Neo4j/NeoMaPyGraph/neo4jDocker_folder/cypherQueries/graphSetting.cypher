//dataset loading
CALL {LOAD CSV WITH HEADERS FROM "file:/<<FILE>>" as l FIELDTERMINATOR ';'
WITH l WHERE datetime(l.date_start) <= datetime(l.date_end)
MERGE (ID_s:Concept{ID:l.ID_s})
MERGE (ID_o:Concept{ID:l.ID_o})
MERGE (ID_p:Concept{ID:l.ID_p})
MERGE (tf:TF{ID:l.ID_TF,date_start:datetime(l.date_start),date_end:datetime(l.date_end),weight:toFloat(l.proba),valid:toBoolean(l.valid),polarity:toBoolean(l.polarity),
	p:l.ID_p, o:l.ID_o, s:l.ID_s})
MERGE (ID_s) <-[:s]- (tf)
MERGE (ID_o) <-[:o]- (tf)
MERGE (ID_p) <-[:p]- (tf);}
