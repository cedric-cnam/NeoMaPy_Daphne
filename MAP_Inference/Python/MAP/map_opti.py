# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 19/08/2022

@author: Victor
"""

import json
import time


##############################################################################################################
##############################################################################################################
###################################### LOAD the data  OPTI 1 #################################################

#with open('.\..\..\Data_Json\Dictionnary\\testDico.json', 'r') as f: 	
#with open('.\..\..\Data_Json\Dictionnary\dicoConfNodes.json', 'r') as f: 	
#with open('.\..\..\Data_Json\Dictionnary\\1kDico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\100Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\80Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\60Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\55Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\50Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\12Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\11Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\10Dico.json', 'r') as f:		
    #dico = json.load(f)


##############################################################################################################
##############################################################################################################
######################################  OPTIMISATION 1 - Algorithme 3 ######################################## 

def sum_weight(dico,solution):
    sum = 0
    for id in solution:
        sum += dico[str(id)][0]
    return sum

def max_sum_list_int(dico,l_sol):
    l_sum = []
    for sol in l_sol:
        l_sum.append(sum_weight(dico,sol[0]))
    return (max(l_sum), l_sol[l_sum.index(max(l_sum))][0])

def deletInclude(liste):
	i = 0
	while i < len(liste):
		j = i + 1 
		while j < len(liste):
			if set(liste[i][0]) < set(liste[j][0]):
				del liste[i]
			elif set(liste[j][0]) < set(liste[i][0]):
				del liste[j]	
			j += 1
		i += 1
	return liste

#liste = [[id_nodes],[conflicts]]
def compatible_merge(node,liste,dico):
	new = list(dico[str(node)][1])
	l_merge_comp = [[node],new]
	compatible = True
	for n in liste[0]:
		if node in dico[str(n)][1] :
			compatible = False
		else:
			new2 = list(dico[str(n)][1])
			l_merge_comp[0].append(n)
			l_merge_comp[1] += new2
			l_merge_comp[1] = list(set(l_merge_comp[1]))
	
	return (l_merge_comp,compatible)
		
# Build the solutions
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

#print(build_sol(dico))

#start = time.time()
#print(max_sum_list_int(dico,build_sol(dico)))
#end = time.time()
#elapsed = end - start
#print(f'Temps d\'exécution : {elapsed:.5}s')


##############################################################################################################
##############################################################################################################
###################################  OPTIMISATION 2 - Algorithme 3+ ########################################## 


##################################### LOAD the data for OPTI 2 ###############################################
#with open('.\..\..\Data_Json\Dictionnary\listOfDico.json', 'r') as f: 	
    #l_dico = json.load(f)


#################################### Apply Opti 1 on the list of dico ########################################
def solutionForList(l_dico):
    output = [0,[]]
    for dico in l_dico["list"]:
        val,liste = max_sum_list_int(dico,build_sol(dico))
        output[0] += val
        output[1] += liste
    return output

#start = time.time()
#print(solutionForList(l_dico))
#end = time.time()
#elapsed = end - start
#print(f'Temps d\'exécution : {elapsed:.5}s')