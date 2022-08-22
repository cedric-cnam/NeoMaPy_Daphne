---------------------------------------------------------------------------------
 Results of Algo 1 vs Algo 2 vs Algo 3 vs Algo 3+ : Temps || Score       
---------------------------------------------------------------------------------

|    File            | Time Aglo 1 | Time Algo 2 | Time Algo 3 | Time Algo 3+ | Score Aglo 1 | Score Algo 2 | Score Algo 3 | Score Algo 3+  |
| ------------------ | :----: | :----:      | :----:        | :-----:   | :----:   | :----: | :----:   | :------: |
| dicoConfNodes.json | 0.4s   | ?           | ?             | 11.8s     | 406.1858 | ------ | ------   | 603.8150 |
| 1kDico.json        | 0.05s  | ?           | ?             | 0.3s      | 158.421  | ------ | ------   | 175.1238 |
| 100Dico.json       | 0s     | ?           | ?             | 0s        | 18.077   | ------ | ------   | 20.0265  |
| 80Dico.json        | 0s     | ?           | ?             | 0s        | 14.814   | ------ | ------   | 15.6493  |
| 60Dico.json        | 0s     | ?           | 1093s (18min) | 0s        | 10.3632  | ------ | 10.9541  | 10.9541  |
| 55Dico.json        | 0s     | ?           | 41s           | 0s        | 9.79568  | ------ | 10.2861  | 10.2861  |
| 50Dico.json        | 0s     | ?           | 3.8s          | 0s        | 9.08248  | ------ | 9.43362  | 9.43362  |
| 12Dico.json        | 0s     | 466s (8min) | 0s            | 0s        | 2.31822  | 2.34025 | 2.34025 | 2.34025  |
| 11Dico.json        | 0s     | 36s         | 0s            | 0s        | 2.08734  | 2.10937 | 2.10937 | 2.10937  |
| 10Dico.json        | 0s     | 13s         | 0s            | 0s        | 0.86158  | 1.31749 | 1.31749 | 1.31749  |


- with dicoConfNodes.json:    0.4s    vs ?   ?    vs 11.8s	    || 406.1858 vs    ?     vs 603.8150
- with 1kDico.json:           0.05s   vs ?   ?    vs 0.3s       || 158.421 	vs    ?     vs 175.1238
- with 100Dico.json:          0s      vs ?   ?    vs 0s			|| 18.077 	vs    ?     vs 20.0265
- with 80Dico.json:           0s      vs ?   ?	vs 0s	        || 14.814 	vs    ?     vs 15.6493
- with 60Dico.json:           0s      vs ? vs 1093s(18m) vs 0s	|| 10.36327 vs    ?     vs 10.9541
- with 55Dico.json:           0s      vs ? 		vs 41.2s	    || 9.79568  vs    ?     vs 10.2861
- with 50Dico.json:           0s      vs ? 		vs 3.8s	        || 9.08248  vs    ?     vs 9.43362
- with 12Dico.json:           0s      vs 466s(8m)	vs 0s       || 2.31822  vs 2.34025  vs 2.34025
- with 11Dico.json:           0s      vs 36s		vs 0s       || 2.08734  vs 2.10937  vs 2.10937 
- with 10Dico.json:           0s      vs 13s 		vs 0s       || 0.86158  vs 1.31749  vs 1.31748
