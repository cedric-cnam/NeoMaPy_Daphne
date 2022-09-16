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

  - 8 hidden Predicates
  - 9 observed Predicates
  - 18 number of formulas

| File | Neo4J | MaPy   | NeoMaPy   | n-RockIt | NeoMaPy nodes | n-RockIt atoms | NeoMaPy conflicts | n-RockIt constraints |
| :--: | :--:  | :--:   |  :--:     |  :--:    |     :--:      |      :--:      |    :--:           |       :--:           | 
| tInc_100_50k |  469s     |  766s  |  1235s  |<p>142 + 432 = <br>574s</p>|  97 212  | 459 073  | 2 209 199  |<p>4 711 701 => <br> 1 179 014</p>|
| tInc_75_50k  |  308s     |  329s  |   637s  |<p>70.5+ 317.5=<br>388s</p>|  84 930  | 417 500  | 1 364 024  |<p> 3 318 794 => <br> 828 688 </p>|
| tInc_50_50k  |  266.4s   |  148s  |   414s  |<p>63 + 289 = <br>352s </p>|  72 627  | 370 596  | 1 193 834  |<p> 3 041 768 => <br> 758 414 </p>|
| tInc_25_50k  |  208.23s  |  227s  |   435s  |<p>64 + 253 = <br>317s </p>|  60 407  | 325 353  |   877 939  |<p> 2 576 245 => <br> 640 546 </p>|
| tInc_10_50k  |  126.46s  |   87s  |   214s  |<p>37 + 183 = <br>220s </p>|  53 247  | 301 034  |   386 829  |<p> 1 713 594 => <br> 424 240 </p>|
| tInc_0_50k   |  76.25s   |  1.4s  |    78s  |<p>15 + 145 = <br>160s </p>|  48 605  | 284 732  |    46 766  |<p> 1 097 073 => <br> 269 043 </p>|
|-----------|-----------|-----------|-----------|--------------|-----------|-----------|-----------|--------------|
| tInc_100_25k |  194.21s  |  167s  |   361s  |<p>51 + 209 = <br> 260s</p>|  48 044  | 224 883  | 1 164 973  |<p> 2 558 474 => <br> 639 393 </p>|
| tInc_75_25k  |  170.42s  |  221s  |   391s  |<p>50 + 193 = <br> 243s</p>|  41 910  | 202 033  | 1 023 679  |<p> 2 351 558 => <br> 587 164 </p>|
| tInc_50_25k  |  143.63s  |  148s  |   292s  |<p>42.5 +173.5=<br>216s</p>|  35 824  | 179 640  |   858 650  |<p> 2 092 951 => <br> 521 571 </p>|
| tInc_25_25k  |  85.73s   |  107s  |   193s  |<p>25 + 112 = <br> 137s</p>|  29 892  | 159 294  |   434 191  |<p> 1 342 541 => <br> 333 560 </p>|
| tInc_10_25k  |  55.07s   |  105s  |   160s  |<p>22 + 100 = <br> 122s</p>|  26 218  | 147 199  |   199 703  |<p>   971 289 => <br> 240 399 </p>|
| tInc_0_25k   |  30.76s   |    1s  |    32s  |<p> 8 + 68 = <br>76s   </p>|  24 022  | 139 019  |    24 935  |<p>   613 779 => <br> 150 326 </p>|
|-----------|-----------|-----------|-----------|--------------|-----------|-----------|-----------|--------------|
| tInc_100_10k |  92.15s   |  168s  |   260s  |<p>27.5 +111.5=<br>139s</p>|  18 674  | 80 142   |   616 288  |<p> 1 420 777 => <br> 354 775 </p>|
| tInc_75_10k  |  74.3s    |  225s  |   299s  |<p>24 + 87 = <br> 111s </p>|  16 403  | 72 019   |   475 037  |<p> 1 148 339 => <br> 286 309 </p>|
| tInc_50_10k  |  114.83s  |  155s  |   270s  |<p> 19 + 73 = <br> 92s </p>|  13 979  | 63 916   |   356 239  |<p> 961 234 => <br> 239 086  </p> |
| tInc_25_10k  |  37.37s   |  98s   |   135s  |<p> 17 + 58 = <br> 75s </p>|  11 533  | 55 794   |   195 097  |<p> 702 223 => <br> 174 219  </p> |
| tInc_10_10k  |  31.35s   |  97s   |   128s  |<p> 8.6 + 46.4 =<br>55s</p>|  10 226  | 50 761   |    94 083  |<p> 503 374 => <br> 124 122  </p> |
| tInc_0_10k   |  13.67s   |  0.7s  |    14s  |<p> 3 + 39 = <br>42s   </p>|   9 337  | 47 614   |    13 278  |<p> 344 713 => <br> 84 249   </p> |
|-----------|-----------|-----------|-----------|--------------|-----------|-----------|-----------|--------------|
| tInc_100_5k  |   47.88s  |   110s |   158s  |<p> 17 + 61 = <br>78s  </p>|   9 284  |  40 339  |   348 999  | <p>816 094 => <br> 204 118  </p> |
| tInc_75_5k   |   37.87s  |  65.5s |   103s  |<p> 15 + 50 = <br>65s  </p>|   8 073  |  36 230  |   261 071  | <p>682 192 => <br> 170 525  </p> |
| tInc_50_5k   |   29.65s  |   112s |   142s  |<p> 15 + 42 = <br>57s  </p>|   6 838  |  32 217  |   185 222  | <p>557 083 => <br> 139 272  </p> |
| tInc_25_5k   |   18.33s  |    29s |    47s  |<p> 10.6 + 35.4=<br>46s</p>|   5 751  |  28 051  |   102 933  | <p>399 019 => <br> 99 546   </p> |
| tInc_10_5k   |   10.49s  |   2.2s |    13s  |<p> 2 + 27 = <br>29s   </p>|   5 073  |  25 680  |    23 081  | <p>227 496 => <br> 56 489   </p> |
| tInc_0_5k    |   12.68s  |   0.6s |    13s  |<p> 2 + 23 = <br>25s   </p>|   4 642  |  24 037  |     7 175  | <p>199 573 => <br> 49 380   </p> |

Where:
- n-Rockit = preSolve + Solve 
- n-RockIt constraints = constraints before preSolve => after preSolve  


 # Results in Time of the Process   

|    File                     | dicoToNdico.py | MaPy.py      | Total  |
| :------------------:        |    :----:      |   :----:     | :--:   |
| dicotIncConf_100_50k.json   |     7s         |    757s      |  764s  |
| dicotIncConf_75_50k.json    |     3.6s       |    325s      |  329s  |
| dicotIncConf_50_50k.json    |     3.1s       |    144s      |  148s  |
| dicotIncConf_25_50k.json    |     2.35s      |    224.5s    |  227s  |
| dicotIncConf_10_50k.json    |     1s         |    174s      |  175s  |
| dicotIncConf_0_50k.json     |     0.15s      |    1.2s      |  1.3s  |
|-----------------------------|----------------|--------------|--------|
| dicotIncConf_100_25k.json   |     3.15s      |    163.9s    |  167s  |
| dicotIncConf_75_25k.json    |     2.8s       |    217.8s    |  221s  |
| dicotIncConf_50_25k.json    |     2.45s      |    146s      |  148s  |
| dicotIncConf_25_25k.json    |     1.15s      |    105.9s    |  107s  |
| dicotIncConf_10_25k.json    |     0.6s       |    105s      |  105s  |
| dicotIncConf_0_25k.json     |     0.08s      |    0.95s     |   1s   |
|-----------------------------|----------------|--------------|--------|
| dicotIncConf_100_10k.json   |     1.6s       |    167.6s    |  168s  |
| dicotIncConf_75_10k.json    |     1.25s      |    224.4s    |  225s  |
| dicotIncConf_50_10k.json    |     1s         |    153.9s    |  155s  |
| dicotIncConf_25_10k.json    |     0.6s       |    97.4s     |  98s   |
| dicotIncConf_10_10k.json    |     0.24s      |    96.8s     |  97s   |
| dicotIncConf_0_10k.json     |     0.04s      |    0.69s     |  0.7s  |
|-----------------------------|----------------|--------------|--------|
| dicotIncConf_100_5k.json    |     1s         |    109s      |  110s  |
| dicotIncConf_75_5k.json     |     0.7s       |    64.8s     |  65.5s |
| dicotIncConf_50_5k.json     |     0.55s      |    111s      |  112s  |
| dicotIncConf_25_5k.json     |     0.25s      |    28.6s     |  29s   | 
| dicotIncConf_10_5k.json     |     0.05s      |    2.2s      |  2.2s  |
| dicotIncConf_0_5k.json      |     0.02s      |    0.56s     |  0.6s  |
|-----------------------------|----------------|--------------|--------|



---------------------------------------------------------------------------------

# NeoMaPy:
- 0_5k:
    - Time : 2.4 sec
    - Score conflicts = 317.80555020000025
    - Score no conflicts = 721.7768804300002
    - Score total = 1039.5824306300005
    - listOfDicotInc_0_5k contains 1700 nodes, 86 dico with max length = 115
    - DicotIncNoConf_0_5k contains 2942 nodes
    - Total nodes = 4642

- 10_5k:
    - Time : 6.8 sec
    - Score conflicts = 376.3193302000005
    - Score no conflicts = 677.5936404393991
    - Score total = 1053.912970639399
    - listOfDicotInc_10_5k contains 2259 nodes, 145 dico with max length = 143 
    - (indice, size, time) = [(0, 143, 6.06s), (1, 134, 0.19s), (2, 106, 0.07s)]
    - distrib = [133, 9, 3, 0, 0, 0, 0, 0, 0, 0]
    - DicotIncNoConf_10_5k contains 2814 nodes
    - Total nodes = 5073

- 25_5k:
    - Time : 28.67 sec
    - Score conflicts = 436.3197303009998
    - Score no conflicts = 636.5519902323013
    - Score total = 1072.871720533301

- 50_5k:
    - Time : 111.5 sec
    - Score conflicts = 563.2840405795994
    - Score no conflicts = 549.1886800916598
    - Score total = 1112.472720671259
    - listOfDicotInc_50_5k contains 4347 nodes, 355 dico with max length = 419
    - DicotIncNoConf_50_5k contains 2491 nodes
    - Total nodes = 6838 

- 75_5k:
    - Time : 64.8 sec
    - Score conflicts = 713.9635509578999
    - Score no conflicts = 431.0391695037002
    - Score total = 1145.0027204616001

- 100_5k:
    - Time : 384.4s
    - Score conflicts = 870.5461207135
    - Score no conflicts = 310.56638963602006
    - Score total = 1181.11251034952

-------------------------------------------------------------------------------------------    

- 0_10k:
    - Time : 3.8 sec
    - Score conflicts = 601.5846702499992
    - Score no conflicts = 1500.7107203200044
    - Score total = 2102.2953905700037
    - listOfDicotInc_0_10k contains 3263 nodes, 199 dico with max length = 117
    - DicotIncNoConf_0_10k contains 6074 nodes
    - Total nodes = 9337

- 10_10k:
    - Time : 96.86 sec
    - Score conflicts = 701.5942201999995
    - Score no conflicts = 1426.6205905400022
    - Score total = 2128.2148107400017

- 25_10k:
    - Time : 97.37 sec
    - Score conflicts = 821.7069606575997
    - Score no conflicts = 1353.9256999269187
    - Score total = 2175.6326605845184

- 50_10k:
    - Time : 153.89 sec
    - Score conflicts = 1144.9110609235995
    - Score no conflicts = 1097.8501295498572
    - Score total = 2242.7611904734567

- 75_10k:
    - Time : 224.38 sec
    - Score conflicts = 1451.6609510872001
    - Score no conflicts = 855.0486094027011
    - Score total = 2306.7095604899014

- 100_10k:
    - Time : 167.6 sec
    - Score conflicts = 1769.849120883162
    - Score no conflicts = 601.1349196811121
    - Score total = 2370.984040564274

------------------------------------------------------------------------------------------- 

- 0_25k:
    - Time : 5.3 sec
    - Score conflicts = 1124.3495005700006
    - Score no conflicts = 4454.232609100002
    - Score total = 5578.582109670003
    - listOfDicotInc_0_25k contains 6 124 nodes, 450 dico with max length = 133
    - DicotIncNoConf_0_25k contains 17 898 nodes
    - Total nodes = 24 022

- 10_25k:
    - Time : 105 sec
    - Score conflicts = 1337.8598712075996
    - Score no conflicts = 4319.886808383882
    - Score total = 5657.7466795914825

- 25_25k:
    - Time : 105.92 sec
    - Score conflicts = 1817.8718808460114
    - Score no conflicts = 3929.469598641273
    - Score total = 5747.341479487284

- 50_25k:
    - Time : 146 sec
    - Score conflicts = 2629.939361654275
    - Score no conflicts = 3276.668607919835
    - Score total = 5906.60796957411

- 75_25k:
    - Time : 217.8 sec
    - Score conflicts = 3435.15731096963
    - Score no conflicts = 2785.3418481313674
    - Score total = 6220.4991591009975

- 100_25k:
    - Time : 163.87 sec
    - Score conflicts = 4244.43639078329
    - Score no conflicts = 2312.7215278496797
    - Score total = 6557.15791863297

------------------------------------------------------------------------------------------- 

- 0_50k:
    - Time : 5.4 sec
    - Score conflicts = 1987.274360180002
    - Score no conflicts = 9428.338059280117
    - Score total = 11415.612419460118
    - listOfDicotInc_0_50k contains 10 767 nodes, 843 dico with max length = 348 
    - (indice, size, time) = [(0, 348, 0.64s), (1, 194, 0.21s), (2, 123, 0.08s), (3, 89, 0.02s), (4, 86, 0.69s), (5, 111, 1.90s)]
    - distribution with a gap of 50 = [809, 27, 5, 1, 0, 0, 1, 0, 0, 0]
    - DicotIncNoConf_0_50k contains 37 838 nodes
    - Total nodes = 48 605

- 10_50k:
    - Time : 86 sec
    - Score conflicts = 2559.32257055
    - Score no conflicts = 9010.019988558492
    - Score total = 11569.342559108089
    - listOfDicotInc_10_50k contains - nodes, - dico with max length = ? 
    - DicotIncNoConf_10_50k contains - nodes
    - Total nodes = 

- 25_50k:
    - Time : 224.5 sec
    - Score conflicts = 3519.56521100519
    - Score no conflicts = 8228.037928652875
    - Score total = 11747.603139658066

- 50_50k:
    - Time : 145 sec
    - Score conflicts = 5117.00397999309
    - Score no conflicts = 7288.239498509248
    - Score total = 12405.24347850234
    - listOfDicotInc_50_50k contains 39 909 nodes, 5393 dico with max length = 461 
    - DicotIncNoConf_50_50k contains 32 718 nodes
    - Total nodes = 72 627

- 75_50k:
    - Time : 325.16 sec
    - Score conflicts = 6869.803541977189
    - Score no conflicts = 6288.838057316909
    - Score total = 13158.641599294097

- 100_50k:
    - 756.9s
    - approx = 288.9s et score = 8215.354050270247 + 5046.633859383296  ==> 13261.987909653544
    - 8513.251010129014
    - 5046.633859383296
    - Score total = 13559.884869512309



----------------------------------------------------------------------------------------------------------------------------
    


# Algorithm :

<p align="center">
  <img src="https://github.com/cedric-cnam/Daphne-UTKG/blob/main/MAP_Inference/Img/compatible_merge.jpg"/>
</p>

<p align="center">
  <img src="https://github.com/cedric-cnam/Daphne-UTKG/blob/main/MAP_Inference/Img/build_solutions.jpg"/>
</p>
