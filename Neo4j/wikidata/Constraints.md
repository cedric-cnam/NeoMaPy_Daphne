# **Rules** implementation for inference

This are *Cypher* queries that produce relationships between *TF* to express the fact it exists a conflict between to Temporal Formulas.
To achieve this, each query corresponds to the expression of a Constraint.

## Constraint rules

Translation & adaptation from Chekol's rules
- Adaptation according to the polarity of TF that did not exist previously
- Intersection of date intervals are embedded directly into the query instead of a separated rule

### 1. A person cannot have two birth dates
!pinst(x, "P569", y, i1, i2, valid) v !pinst(x, "P569", z, i3, i4, valid) v sameAs(y, z).

```
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"birthDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start <> tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C1", error:"birthDateConflict"}]- (tf2)
```

Addon with different polarities with the same date
```
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"birthDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
MERGE (tf1) -[:conflict{type:"C1-1", error:"birthDateConflictPolarity"}]- (tf2)
```


Becareful, it's possible to have several TF with predicate **birthDate** for a single person with the same *date*
```
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"birthDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
RETURN p1, p2
```


### 2. A person cannot have two death dates
!pinst(x, "P570", y, i1, i2, valid) v !pinst(x, "P570", z, i3, i4, valid) v sameAs(y, z).

```
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"birthDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start <> tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C2", error:"deathDateConflict"}]- (tf2)
```

Addon with different polarities with the same date
```
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"deathDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity <> tf2.polarity
MERGE (tf1) -[:conflict{type:"C2-1", error:"deathDateConflictPolarity"}]- (tf2)
```


Becareful, it's possible to have several TF with predicate **birthDate** for a single person with the same *date*
```
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"deathDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1 <> tf2 AND tf1.date_start = tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
RETURN p1, p2
```

### 3. A person's birth date is before his/her death date
> !pinst(x, "P569", y, i1, i2, valid) v !pinst(x, "P570", z, i3, i4, valid) v before(i1,i2,i3,i4).
> !pinst(x, "P569", y, i1, i2, valid) v !pinst(x, "P570", z, i3, i4, valid) v validLifeSpan(i1, i3).

```
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"deathDate"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE (tf1.date_start > tf2.date_start
  OR tf1.date_start + duration({years: 150}) <= tf2.date_start) AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C3", error:"birthDeathConflict"}]- (tf2)
```


### 4. A person must be born before playing for a team.
> !pinst(x, "P569", y, i1, i2, valid) v !pinst(x, "P54", z, i3, i4, valid) v before(i1, i2, i3, i4).

```
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C4", error:"birthPlayerConflict"}]- (tf2)
```

### 5. A person must be alive to play for a team.
> !pinst(x, "P570", y, i1, i2, valid) v !pinst(x, "P54", z, i3, i4, valid) v before(i3, i4, i1, i2).


```
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start < tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C5", error:"deathPlayerConflict"}]- (tf2)
```


### 6. A person must be atleast 16 before playing for a premier league club.
> !pinst(x, "P569", y, i1, i2, valid) v !pinst(x, "P54", z, i3, i4, valid) v aboveSixteen(i1, i3)

```
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start + duration({years: 16}) > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C6", error:"playerAgeConflict"}]- (tf2)
```


### 7. Someone who is older than 50 years does not play in a club.
> !pinst(x, "P569", y, i1, i2, valid) v !pinst(x, "P54", z, i3, i4, valid) v belowFifty(i1, i4)


```
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start + duration({years: 50}) < tf2.date_end AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C7", error:"playerTooOldConflict"}]- (tf2)
```

### 8. A footballer cannot play for two different clubs at the same time/period.
> !pinst(x, "P54", y, i1, i2, valid) v !pinst(x, "P54", z, i3, i4, valid) v sameAs(y, z) v disjoint(i1,i2,i3,i4).

```
MATCH p1=(:Concept{name:"teamPlayer"}) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o1),
  p2=(:Concept{name:"teamPlayer"}) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o2)
WHERE o1 <> o2 AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C8", error:"twoTeamsConflict"}]- (tf2)
```

### 14. A person cannot be married to two distinct individuals.
> !pinst(x, "P26", y, i1, i2, valid) v !pinst(x, "P26", z, i3, i4, valid) v sameAs(y, z) v disjoint(i1,i2,i3,i4).

```
MATCH p1=(:Concept{name:"marriage"}) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o1),
  p2=(:Concept{name:"marriage"}) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o2)
WHERE o1 <> o2 AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C14", error:"marriageConflict"}]- (tf2)
```

### 16. A person must be born before getting married.
> !pinst(x, "P569", y, i1, i2, valid) v !pinst(x, "P26", z, i3, i4, valid) v before(i1, i2, i3, i4).


```
MATCH p1=(:Concept{name:"birthDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"marriage"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C16", error:"birthMarriageConflict"}]- (tf2)
```

### 17. A person must be alive to be married.
> !pinst(x, "P570", y, i1, i2, valid) v !pinst(x, "P26", z, i3, i4, valid) v before(i3, i4, i1, i2).

```
MATCH p1=(:Concept{name:"deathDate"}) <-[:p]- (tf1) -[:s]-> (s),
  p2=(:Concept{name:"marriage"}) <-[:p]- (tf2) -[:s]-> (s)
WHERE tf1.date_start > tf2.date_start AND tf1.polarity = true AND tf2.polarity = true
MERGE (tf1) -[:conflict{type:"C17", error:"deathMarriageConflict"}]- (tf2)
```

### 18. A person cannot be both a player and a coach at the same time.
>	!pinst(x, "P54", y, i1, i2, valid) v !pinst(x, "P286", z, i3, i4, valid) v disjoint(i1,i2,i3,i4)

```
MATCH p1=(:Concept{name:"teamPlayer"}) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o1),
  p2=(:Concept{name:"teamCoach"}) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o2)
WHERE o1 <> o2 AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C18", error:"playerCoachConflict"}]- (tf2)
```

### 19. A person cannot work for two companies at the same time.
>	!pinst(x, "P108", y, i1, i2, valid) v !pinst(x, "P108", z, i3, i4, valid) v sameAs(y, z) v disjoint(i1,i2,i3,i4)

```
MATCH p1=(:Concept{name:"workCompany"}) <-[:p]- (tf1) -[:s]-> (s), (tf1) -[:o]-> (o1),
  p2=(:Concept{name:"workCompany"}) <-[:p]- (tf2) -[:s]-> (s), (tf2) -[:o]-> (o2)
WHERE o1 <> o2 AND tf1.polarity = true AND tf2.polarity = true AND
    ( (tf1.date_start < tf2.date_start and tf2.date_start < tf1.date_end)
    OR (tf2.date_start < tf1.date_start and tf1.date_start < tf2.date_end) )
MERGE (tf1) -[:conflict{type:"C19", error:"twoCompaniesConflict"}]- (tf2)
```
