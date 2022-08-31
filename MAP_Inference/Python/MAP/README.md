---------------------------------------------------------------------------------
 Results in Time and Score of the different Algorithms      
---------------------------------------------------------------------------------

|    File            | Time Algo 1 | Time Algo 2 | Time Algo 3 | Time Algo 3+ | Time Algo 3* |  Score Algo 1 | Score Algo 2 | Score Algo 3 | Score Algo 3+ and 3* |
| ------------------ | :----: | :----:      | :----:        | :-----:    | :-----:   | :----:   | :----:  | :----:   | :------: | 
| dicoConfNodes.json |0.1-0.4s| ?           | ?             | 1.1s       | 1.2s      | 406.1858 |  ?      | ?        | 433.02028 |
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
- Algo 3* is Opti 1 + 2 + 3 (Parallelization),
- dicoConfNodes.json contains 2500 nodes.

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
4.a) Apply map_opti3.py to use the buildSol algorithm which has 2 optimizations:
    - deletInclude eliminates from the current list of solutions those that are included,
    - use a threshold (experimental optimization of the calculation around 0.6, i.e. after 60% of the dictionary nodes) to start searching and removing bad solutions which, even adding the (sum of the) last nodes, cannot have a better score than the current best solution.
4.b) For big data set, use the function parallelization to parallelize buildSol on the different dico.
  


# Algorithm 3 - Optimisation 1:

<p align="center">
  <img src="https://github.com/cedric-cnam/Daphne-UTKG/blob/main/MAP_Inference/Img/compatible_merge.jpg"/>
</p>

<p align="center">
  <img src="https://github.com/cedric-cnam/Daphne-UTKG/blob/main/MAP_Inference/Img/build_solutions.jpg"/>
</p>
