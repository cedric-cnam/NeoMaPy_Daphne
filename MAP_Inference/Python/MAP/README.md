---------------------------------------------------------------------------------
 Results in Time and Score of the different Algorithms      
---------------------------------------------------------------------------------

|    File            | Time Algo 1 | Time Algo 2 | Time Algo 3 | Time Algo 3+ | Score Algo 1 | Score Algo 2 | Score Algo 3 | Score Algo 3+  |
| ------------------ | :----: | :----:      | :----:        | :-----:   | :----:   | :----:  | :----:   | :------: |
| dicoConfNodes.json | 0.4s   | ?           | ?             | 11.8s     | 406.1858 |  ?      | ?        | 603.8150 |
| 1kDico.json        | 0.05s  | ?           | ?             | 0.3s      | 158.421  |  ?      | ?        | 175.1238 |
| 100Dico.json       | 0s     | ?           | ?             | 0s        | 18.077   |  ?      | ?        | 20.0265  |
| 80Dico.json        | 0s     | ?           | ?             | 0s        | 14.814   |  ?      | ?        | 15.6493  |
| 60Dico.json        | 0s     | ?           | 1093s (18min) | 0s        | 10.3632  |  ?      | 10.9541  | 10.9541  |
| 55Dico.json        | 0s     | ?           | 41s           | 0s        | 9.79568  |  ?      | 10.2861  | 10.2861  |
| 50Dico.json        | 0s     | ?           | 3.8s          | 0s        | 9.08248  |  ?      | 9.43362  | 9.43362  |
| 12Dico.json        | 0s     | 466s (8min) | 0s            | 0s        | 2.31822  | 2.34025 | 2.34025  | 2.34025  |
| 11Dico.json        | 0s     | 36s         | 0s            | 0s        | 2.08734  | 2.10937 | 2.10937  | 2.10937  |
| 10Dico.json        | 0s     | 13s         | 0s            | 0s        | 0.86158  | 1.31749 | 1.31749  | 1.31749  |

Where: 
- Algo 1 is First Solution,
- Algo 2 is Brute Force,
- Algo 3 is Opti 1,
- Algo 3+ is Opti 1 + 2,
- dicoConfNodes.json contains 2500 nodes.


---
header-includes:
  - \usepackage[ruled,vlined,linesnumbered]{algorithm2e}
---
# Algorithm 3 - Optimisation 1:

\begin{algorithm}[H]
\DontPrintSemicolon
\SetAlgoLined
\KwResult{Node merged with the maximum of nodes of a list}
\SetKwInOut{Input}{Input}\SetKwInOut{Output}{Output}
\Input{Node = int(key), List = [[set of nodes], [set of conflict nodes]], Dico = {id_node: [weight, [set of conflict nodes]]}}
\Output{Node+maxList_compatible, bool_compatible}
\BlankLine
new = list(dico[str(node)][1])
l_merge_comp = [[node],new]
compatible = True
\For{n in List[0]}{
    instructions\;
    \eIf{node in dico[str(n)][1] }{
        compatible = False
    }{
        new2 = list(dico[str(n)][1])\;
		l_merge_comp[0].append(n)\;
		l_merge_comp[1] += new2\;
		l_merge_comp[1] = list(set(l_merge_comp[1]));
    }
}
return (l_merge_comp,compatible)
\caption{Merge a node with a list}
\end{algorithm}


		

def build_sol(dico):
	liste_sol = []
	i = 0 
	for k, v in dico.items():
		if i == 0:
			new = list(dico[k][1])
			liste_sol.append([[int(k)],new])
			i = 1
		else:
			for j in range(0,len(liste_sol)):
				(l2,bool) = compatible_merge(int(k),liste_sol[j],dico)
				if bool:
					liste_sol[j][0].append(int(k))
					liste_sol[j][1] += new
					liste_sol[j][1] = list(set(liste_sol[j][1]))
				else:
					liste_sol += [[l2[0],l2[1]]]
			liste_sol = deletInclude(liste_sol)
		
	return liste_sol
