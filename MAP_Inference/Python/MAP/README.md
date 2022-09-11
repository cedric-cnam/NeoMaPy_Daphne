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


 # Results in Time of the Process   

|    File                   | cleanData.py | divideDico.py | dicoToNdico.py | map_opti3.py | Total  |
| ------------------        | :----:       | :----:        | :----:         |   :----:     | :--:   |
| dicotIncConf_100_50k.json |  Not Used    |   Not Used    |     8.7s       |    ? s       |  ? s   |
| dicotIncConf_50_50k.json  |  Not Used    |   Not Used    |     3.6s       |    ? s       |  ? s   |
| dicotIncConf_0_50k.json   |  Not Used    |   Not Used    |     0.15s      |    5.4s      |  5.4s  |
| ------------------        | :----:       | :----:        | :----:         |   :----:     | :--:   |
| dicotIncConf_0_25k.json   |  Not Used    |   Not Used    |     0.08s      |    5.3s      |  5.3s  |
| dicotIncConf_0_10k.json   |  Not Used    |   Not Used    |     0.04s      |    3.8s      |  3.8s  |
| ------------------        | :----:       | :----:        | :----:         |   :----:     | :--:   |
| dicotIncConf_100_5k.json  |  Not Used    |   Not Used    |     1.1s       |    ? s       |  ? s   |
| dicotIncConf_50_5k.json   |  Not Used    |   Not Used    |     0.6s       |    ? s       |  ? s   |
| dicotIncConf_0_5k.json    |  Not Used    |   Not Used    |     0.02s      |    2.4s      |  2.4s  |
| dicoConfNodes.json        |    0.75s     |     0.01s     |     0.015s     |    1.1s      |  1.8s  |
| dicoConfNodes.json        |  Not Used    |   Not Used    |     0.015s     |    1.55s     |  1.6s  |


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

NeoMaPy:
- 0_5k:
    - Time without clear data and without parallelization : 2.4 sec
    - Score conflicts = 317.80555020000025
    - Score no conflicts = 721.7768804300002
    - Score total = 1039.5824306300005
    - listOfDicotInc_0_5k contains 1700 nodes, 86 dico with max length = 115
    - DicotIncNoConf_0_5k contains 2942 nodes
    - Total nodes = 4642

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
    - DicotIncNoConf_0_50k contains 37 838 nodes
    - Total nodes = 48 605

n-RockIt:
- 0_5k:
    - Time = 25 sec

- 0_50k:
    - Time = 2 min 40

---------------------------------------------------------------------------------

# Algorithm 3 - Optimisation 1:

<p align="center">
  <img src="https://github.com/cedric-cnam/Daphne-UTKG/blob/main/MAP_Inference/Img/compatible_merge.jpg"/>
</p>

<p align="center">
  <img src="https://github.com/cedric-cnam/Daphne-UTKG/blob/main/MAP_Inference/Img/build_solutions.jpg"/>
</p>
