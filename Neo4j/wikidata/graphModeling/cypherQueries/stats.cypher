//Nb triplets
MATCH (ns:Concept) <-[:s]- (tf:TF) -[:o]-> (no), (tf) -[:p]-> (np)
RETURN COUNT(*) as NB_triplets;

//Nb "o"
MATCH (tf:TF) -[:o]-> (ns)
RETURN COUNT(distinct ns) as NB_o;

//Nb "s"
MATCH (tf:TF) -[:s]-> (ns)
RETURN COUNT(distinct ns) as NB_s;

//nb "p"
MATCH (tf:TF) -[:p]-> (np)
RETURN COUNT(distinct np) as NB_p;

//Nb "p" links distribution
MATCH (tf:TF) -[:p]-> (np)
RETURN np.ID as ID, np.name as NAME, count(*) as NB
ORDER BY NB DESC;

//Nb conflicts distribution
MATCH () -[c:conflict]- ()
RETURN c.type as TYPE, c.error as CONFLICT_CODE, count(distinct c) as NB;

//Nb temporal conflicts
MATCH (:TF) -[c:conflict{type:"TC1"}]- (:TF)
RETURN SUM(CASE WHEN c.pCon=true THEN 1 ELSE 0 END) AS NB_pCon,
    SUM(CASE WHEN c.pInc=true AND c.pCon=true THEN 1 ELSE 0 END) AS NB_pConpInc,
    SUM(CASE WHEN c.pInc=true THEN 1 ELSE 0 END) AS NB_pInc,
    SUM(CASE WHEN c.tInc=true THEN 1 ELSE 0 END) AS NB_tInc,
    COUNT(*) as NB_total;

    
//Distribution of linked "o"
MATCH (tf:TF) -[:o]-> (no)
RETURN no.ID as o_ID, count(*) as NB
ORDER BY NB DESC;
    