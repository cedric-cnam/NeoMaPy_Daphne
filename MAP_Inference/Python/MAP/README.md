# Process:
  ## Data Manipulation
1) Apply cleanData.py to remove the obvious bad nodes, i.e. if a node A is in conflict with another node B that has:
    - the same conflict or a subset (set_A >= set_B), and
    - with a better weight (score_A < score_B),
then A is an obvious bad node and it must be deleted. 
2) Apply divideDico.py to split the nodes into two files:
    - one with all nodes without conflict and 
    - the second with conflict.
3) Apply dicoToNdico.py from the conflicted nodes file. It builds a list of dictionaries where:
    - each dictionary has connected nodes and 
    - it orders the nodes from most to least conflicting (i.e. in decreasing order of the number of conflicts).
  ## Algorithm 
4) [Option 1] Apply map_opti3.py to use the buildSol algorithm which has 2 optimizations:
    - deletInclude eliminates from the current list of solutions those that are included,
    - use a threshold (experimental optimization of the calculation around 0.6, i.e. after 60% of the dictionary nodes) to start searching and removing bad solutions which, even adding the (sum of the) last nodes, cannot have a better score than the current best solution.
4) [Option 2] For big data set, use the function parallelization to parallelize buildSol on the different dico.
  

---------------------------------------------------------------------------------
 # Compare NeoMaPy vs n-RockIt
|    File                     | NeoMaPy | n-RockIt  |
| ------------------          | :--:    | :--:      |
|dicotIncConf_100_50k.json // |  1720s  |  574s     |
| dicotIncConf_50_50k.json // |  529s   |  352s     |
| dicotIncConf_10_50k.json // |  175s   |  220s     |
| dicotIncConf_0_50k.json     |  5.4s   |  160s     |
|-----------------------------|---------|-----------|
| dicotIncConf_0_25k.json     |  5.3s   |  76s      |
|-----------------------------|---------|-----------|
| dicotIncConf_0_10k.json     |  3.8s   |  42s      |
|-----------------------------|---------|-----------|
| dicotIncConf_100_5k.json    |  385s   |  78s      |
| dicotIncConf_50_5k.json //  |  339s   |  57s      |
| dicotIncConf_10_5k.json     |  6.8s   |  29s      |
| dicotIncConf_0_5k.json      |  2.4s   |  25s      |



 # Results in Time of the Process   

|    File                     | cleanData.py | divideDico.py | dicoToNdico.py | map_opti3.py | Total  |
| ------------------          | :----:       | :----:        | :----:         |   :----:     | :--:   |
|dicotIncConf_100_50k.json // |  Not Used    |   Not Used    |     8.7s       |    1711s     |  1720s |
|-----------------------------|--------------|---------------|----------------|--------------|--------|
| dicotIncConf_50_50k.json // |    415s      |      1s       |     3.7s       |    533s      |  953s  |
| dicotIncConf_50_50k.json // |  Not Used    |   Not Used    |     3.6s       |    525s      |  529s  |
| dicotIncConf_50_50k.json    |    415s      |      1s       |     3.6s       |    812s      |  1230s |
| dicotIncConf_50_50k.json    |  Not Used    |   Not Used    |     3.6s       |    887s      |  891s  |
| dicotIncConf_10_50k.json // |  Not Used    |   Not Used    |     1s         |    174s      |  175s  |
| dicotIncConf_0_50k.json     |    18.7s     |     0.07s     |     0.13s      |    3.7s      |  22s   |
| dicotIncConf_0_50k.json     |  Not Used    |   Not Used    |     0.15s      |    5.4s      |  5.4s  |
|-----------------------------|--------------|---------------|----------------|--------------|--------|
| dicotIncConf_0_25k.json     |  Not Used    |   Not Used    |     0.08s      |    5.3s      |  5.3s  |
|-----------------------------|--------------|---------------|----------------|--------------|--------|
| dicotIncConf_0_10k.json     |  Not Used    |   Not Used    |     0.04s      |    3.8s      |  3.8s  |
|-----------------------------|--------------|---------------|----------------|--------------|--------|
| dicotIncConf_100_5k.json    |  Not Used    |   Not Used    |     1.1s       |    385s      |  386s  |
| dicotIncConf_50_5k.json //  |  7.5s        |   0.14s       |     0.6s       |    316s      |  324s  |
| dicotIncConf_50_5k.json //  |  Not Used    |   Not Used    |     0.6s       |    339s      |  339s  |
| dicotIncConf_50_5k.json     |  7.5s        |   0.14s       |     0.6s       |    361s      |  369s  |
| dicotIncConf_50_5k.json     |  Not Used    |   Not Used    |     0.6s       |    405s      |  405s  |
| dicotIncConf_10_5k.json     |  0.95s       |   0.02s       |     0.04s      |    4.7s      |  5.7s  |
| dicotIncConf_10_5k.json     |  Not Used    |   Not Used    |     0.05s      |    6.8s      |  6.8s  |
| dicotIncConf_0_5k.json      |  Not Used    |   Not Used    |     0.02s      |    2.4s      |  2.4s  |
|-----------------------------|--------------|---------------|----------------|--------------|--------|
| dicoConfNodes.json          |    0.75s     |     0.01s     |     0.015s     |    1.1s      |  1.8s  |
| dicoConfNodes.json          |  Not Used    |   Not Used    |     0.015s     |    1.55s     |  1.6s  |


---------------------------------------------------------------------------------


 # Results in Time and Score of the different Algorithms      

|    File            | Time Algo 1 | Time Algo 2 | Time Algo 3 | Time Algo 3+ | Time Algo 3* |  Score Algo 1 | Score Algo 2 | Score Algo 3 | Score Algo 3+ and 3* |
| ------------------ | :----: | :----:      | :----:        | :-----:    | :-----:   | :----:   | :----:  | :----:   | :------: | 
| dicoConfNodes.json | 0.25s  | ?           | ?             | 1.1s       | 1.2s      | 406.1858 |  ?      | ?        | 433.02028 |
| 1kDico.json        | 0.03s  | ?           | ?             | 0.01s      | 0.3s      | 158.421  |  ?      | ?        | 175.1238 |
| 100Dico.json       | 0s     | ?           | ?             | 0s         | 0.25s     | 18.077   |  ?      | ?        | 20.0265  |
| 80Dico.json        | 0s     | ?           | ?             | 0s         | 0.25s     | 14.814   |  ?      | ?        | 15.6493  |
| 60Dico.json        | 0s     | ?           | 1093s (18min) | 0s         | 0.25s     | 10.3632  |  ?      | 10.9541  | 10.9541  |
| 55Dico.json        | 0s     | ?           | 41s           | 0s         | 0.25s     | 9.79568  |  ?      | 10.2861  | 10.2861  |
| 50Dico.json        | 0s     | ?           | 3.8s          | 0s         | 0.25s     | 9.08248  |  ?      | 9.43362  | 9.43362  |
| 12Dico.json        | 0s     | 466s (8min) | 0s            | 0s         | 0.25s     | 2.31822  | 2.34025 | 2.34025  | 2.34025  |
| 11Dico.json        | 0s     | 36s         | 0s            | 0s         | 0.25s     | 2.08734  | 2.10937 | 2.10937  | 2.10937  |
| 10Dico.json        | 0s     | 13s         | 0s            | 0s         | 0.25s     | 0.86158  | 1.31749 | 1.31749  | 1.31749  |

Where: 
- Algo 1 is First Solution,
- Algo 2 is Brute Force,
- Algo 3 is Opti 1 (deleteInclude + Threshold), 
- Algo 3+ is Opti 1 + 2 (Clean data + Dico in connected partition + Dico in decreasing conflicts order),
- Algo 3* is Opti 1 + 2 + 3 (Parallelization).


Stats:
- Number of conflicted nodes initially (dicoConfNodes.json): 2480
- 469 dico with max length = 115
- average time 1.55s (without parallelization)
- average time 1.75s (with parallelization)
-------------------------------------------------------------------
- Number of conflicted nodes after cleanData and divideDico: 1414 
- 66 dico with max length = 109
- avg time 1.1s (without parallelization)
- average time 1.2s (with parallelization)
-------------------------------------------------------------------
- Sum of the nodes without conflict initially = 575.3432406800008 
- Sum of the MAP = 1008.36352068


---------------------------------------------------------------------------------

# NeoMaPy:
- 0_5k:
    - Time without clear data and without parallelization : 2.4 sec
    - Score conflicts = 317.80555020000025
    - Score no conflicts = 721.7768804300002
    - Score total = 1039.5824306300005
    - listOfDicotInc_0_5k contains 1700 nodes, 86 dico with max length = 115
    - DicotIncNoConf_0_5k contains 2942 nodes
    - Total nodes = 4642

- 10_5k:
    - Time without clear data and without parallelization : 6.8 sec
    - Score conflicts = 376.3193302000005
    - Score no conflicts = 677.5936404393991
    - Score total = 1053.912970639399
    - listOfDicotInc_10_5k contains 2259 nodes, 145 dico with max length = 143 
    - (indice, size, time) = [(0, 143, 6.06s), (1, 134, 0.19s), (2, 106, 0.07s)]
    - distrib = [133, 9, 3, 0, 0, 0, 0, 0, 0, 0]
    - DicotIncNoConf_10_5k contains 2814 nodes
    - Total nodes = 5073

- 10_5k:
    - Time with clear data and without parallelization : 4.7 sec
    - Score conflicts = 310.53924002000014
    - Score clear conflicts = 65.78009018000003
    - Score no conflicts = 677.5936404393991
    - Score total = 1053.912970639399
    - listOfDicotInc_10_5kClear contains 1861 nodes (less 398 nodes), 59 dico with max length = 140
    - DicotIncNoConfClear_10_5k contains 250 nodes
    - DicotIncNoConf_10_5k contains 2814 nodes
    - Total nodes = 4925 (148 bad nodes deleted)

- 50_5k without clear:
    - Time without clear data and without parallelization : 405 sec
    - Score conflicts = 563.2840405795994
    - Score no conflicts = 549.1886800916598
    - Score total = 1112.472720671259
    - listOfDicotInc_50_5k contains 4347 nodes, 355 dico with max length = 419
    - DicotIncNoConf_50_5k contains 2491 nodes
    - Total nodes = 6838 

- 50_5k with clear:
    - Time with clear data and with parallelization : 316 sec
    - Time with clear data and without parallelization : 361 sec
    - Score conflicts = 444.7572303775998
    - Score clear conflicts = 118.526810202
    - Score no conflicts = 549.1886800916598
    - Score total = 1112.472720671259
    - listOfDicotInc_50_5kClear contains 3506 nodes, 75 dico with max length = 416
    - DicotIncNoConfClear_50_5k contains 460 nodes
    - DicotIncNoConf_50_5k contains 2491 nodes
    - Total nodes = 6457 

- 100_5k without clear:
    - Time without clear data and with parallelization : 384.4s
    - Score conflicts = 870.5461207135
    - Score no conflicts = 310.56638963602006
    - Score total = 1181.11251034952

- 0_10k:
    - Time without clear data and without parallelization : 3.8 sec
    - Score conflicts = 601.5846702499992
    - Score no conflicts = 1500.7107203200044
    - Score total = 2102.2953905700037
    - listOfDicotInc_0_10k contains 3263 nodes, 199 dico with max length = 117
    - DicotIncNoConf_0_10k contains 6074 nodes
    - Total nodes = 9337

- 0_25k:
    - Time without clear data and without parallelization : 5.3 sec
    - Score conflicts = 1124.3495005700006
    - Score no conflicts = 4454.232609100002
    - Score total = 5578.582109670003
    - listOfDicotInc_0_25k contains 6 124 nodes, 450 dico with max length = 133
    - DicotIncNoConf_0_25k contains 17 898 nodes
    - Total nodes = 24 022

- 0_50k:
    - Time without clear data and without parallelization : 5.4 sec
    - Score conflicts = 1987.274360180002
    - Score no conflicts = 9428.338059280117
    - Score total = 11415.612419460118
    - listOfDicotInc_0_50k contains 10 767 nodes, 843 dico with max length = 348 
    - (indice, size, time) = [(0, 348, 0.64s), (1, 194, 0.21s), (2, 123, 0.08s), (3, 89, 0.02s), (4, 86, 0.69s), (5, 111, 1.90s)]
    - distribution with a gap of 50 = [809, 27, 5, 1, 0, 0, 1, 0, 0, 0]
    - DicotIncNoConf_0_50k contains 37 838 nodes
    - Total nodes = 48 605

- 10_50k:
    - Time without clear data and with parallelization : 174 sec
    - approx : 46.5sec with score = 11499.86382898
    - Score conflicts = 2559.32257055
    - Score no conflicts = 9010.019988558492
    - Score total = 11569.342559108089
    - listOfDicotInc_10_50k contains - nodes, - dico with max length = ? 
    - DicotIncNoConf_10_50k contains - nodes
    - Total nodes = 

- 50_50k without clear:
    - Time without clear data and without parallelization : 887 sec
    - Time without clear data and with parallelization : 525 sec
    - Score conflicts = 5117.00397999309
    - Score no conflicts = 7288.239498509248
    - Score total = 12405.24347850234
    - listOfDicotInc_50_50k contains 39 909 nodes, 5393 dico with max length = 461 
    - DicotIncNoConf_50_50k contains 32 718 nodes
    - Total nodes = 72 627

- 50_50k with clear:
    - Time with clear data and without parallelization : 812 sec
    - Time without clear data and with parallelization : 533 sec
    - Score conflicts = 3518.037851
    - Score clear = 1598.9661291441232
    - Score no conflicts = 7288.239498509248
    - Score total = 12405.24347850234
    - listOfDicotInc_50_50kClear contains 28 169 nodes, 743 dico with max length = 461
    - DicotIncNoConfClear_50_50k contains 6 029 nodes
    - DicotIncNoConf_50_50k contains 32 718 nodes
    - Total nodes = 66 916

- 100_50k:
    - 1711.7s
    - 8513.251010129014
    - 5046.633859383296
    - Score total = 13559.884869512309

----------------------------------------------------------------------------------------------------
# TEST 

- 10_5k:
    - Time without clear data and without parallelization : 6.8 sec
    - Score conflicts = 376.3193302000005
    - Score no conflicts = 677.5936404393991
    - Score total = 1053.912970639399
    - listOfDicotInc_10_5k contains 2259 nodes, 145 dico with max length = 143 
    - (indice, size, time) = [(0, 143, 6.06s), (1, 134, 0.19s), (2, 106, 0.07s)]
    - distrib = [133, 9, 3, 0, 0, 0, 0, 0, 0, 0]
    - DicotIncNoConf_10_5k contains 2814 nodes
    - Total nodes = 5073

0 / 145 with length = 143
temps de comp à indice 0 = 1.8977432250976562
temps de inc à indice 0 = 3.888690710067749
taille moyenne de list_sol dans inc à indice 0 = 332.2464788732394
Temps d'exécution 0 : 6.747s

1 / 145 with length = 134
temps de comp à indice 1 = 0.09781098365783691
temps de inc à indice 1 = 0.045911312103271484
taille moyenne de list_sol dans inc à indice 1 = 47.63157894736842
Temps d'exécution 1 : 0.16157s

- 0_50k:
    - Time without clear data and without parallelization : 5.4 sec
    - Score conflicts = 1987.274360180002
    - Score no conflicts = 9428.338059280117
    - Score total = 11415.612419460118
    - listOfDicotInc_0_50k contains 10 767 nodes, 843 dico with max length = 348 
    - (indice, size, time) = [(0, 348, 0.64s), (1, 194, 0.21s), (2, 123, 0.08s), (3, 89, 0.02s), (4, 86, 0.69s), (5, 111, 1.90s)]
    - distribution with a gap of 50 = [809, 27, 5, 1, 0, 0, 1, 0, 0, 0]
    - DicotIncNoConf_0_50k contains 37 838 nodes
    - Total nodes = 48 605

0 / 843 with length = 348
temps de comp à indice 0 = 0.5567188262939453
temps de inc à indice 0 = 0.04073143005371094
taille moyenne de list_sol dans inc à indice 0 = 24.270893371757925
Temps d'exécution 0 : 0.61449s

4 / 843 with length = 86
temps de comp à indice 4 = 0.14849162101745605
temps de inc à indice 4 = 0.4060025215148926
taille moyenne de list_sol dans inc à indice 4 = 109.17647058823529
Temps d'exécution 4 : 0.66025s

5 / 843 with length = 111
temps de comp à indice 5 = 0.523388147354126
temps de inc à indice 5 = 0.9915013313293457
taille moyenne de list_sol dans inc à indice 5 = 248.38181818181818
Temps d'exécution 5 : 1.7832s

----------------------------------------------------------------------------------------------------------------------------

# n-RockIt:
  - 8 hidden Predicates
  - 9 observed Predicates
  - 18 number of formulas

|    File                     | Time                | evidence atoms | constrains     |
| ------------------          | :----:              | :----:         | :----:         |  
| 0_5k                        |  25 s               |   24 037       |   199 573      |
| 10_5k                       |  29 s               |   25 680       |   227 496      |  
| 50_5k                       |  57 s               |   32 217       |   557 083      |
| 100_5k                      |  1 min 18 (78s)     |   40 339       |   816 094      | 
|-----------------------------|---------------------|----------------|----------------|
| 0_10k                       |  42 s               |   47 614       |   344 713      |
|-----------------------------|---------------------|----------------|----------------|
| 0_25k                       |  76 s               |   139 019      |   613 779      | 
|-----------------------------|---------------------|----------------|----------------|
| 0_50k                       |  2 min 40 (160s)    |   284 732      |   1 097 073    |
| 10_50k                      |  3 min 40 (220s)    |   301 034      |   1 713 594    |
| 50_50k                      |  5 min 52 (352s)    |   370 596      |   3 041 768    |  
| 100_50k                     |  9 min 34 (574s)    |   459 073      |   4 711 701    |
    


---------------------------------------------------------------------------------

# Algorithm 3 - Optimisation 1:

<p align="center">
  <img src="https://github.com/cedric-cnam/Daphne-UTKG/blob/main/MAP_Inference/Img/compatible_merge.jpg"/>
</p>

<p align="center">
  <img src="https://github.com/cedric-cnam/Daphne-UTKG/blob/main/MAP_Inference/Img/build_solutions.jpg"/>
</p>
