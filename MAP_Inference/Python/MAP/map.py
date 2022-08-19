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
####################################### LOAD the data and RESULTS ############################################

# ----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------#      ###   Algo 1 vs Algo 2 vs Algo 3: Temps || Score   ###   -
# ----------------------------------------------------------------------------------------------------------------------------------

#with open('.\..\..\Data_Json\Dictionnary\dicoConfNodes.json', 'r') as f:  # 0.234 s vs ?					|| 406.1858 vs ?
#with open('.\..\..\Data_Json\Dictionnary\\1kDico.json', 'r') as f:	  # 0.05 s vs ? 						|| 158.421 	vs ?
#with open('.\..\..\Data_Json\Dictionnary\\100Dico.json', 'r') as f:  # 0.0 s vs ?							|| 18.077 	vs ?
#with open('.\..\..\Data_Json\Dictionnary\\80Dico.json', 'r') as f:   # 0.0 s vs ? 							|| 14.814 	vs ?
#with open('.\..\..\Data_Json\Dictionnary\\60Dico.json', 'r') as f:   # 0.0 s vs ? vs 1093.7 s env. 18min   || 10.36327 vs    ?    vs 10.95413
#with open('.\..\..\Data_Json\Dictionnary\\55Dico.json', 'r') as f:   # 0.0 s vs ? 				vs 41.2 s   || 9.79568  vs    ?    vs 10.2861
with open('.\..\..\Data_Json\Dictionnary\\50Dico.json', 'r') as f: 	  # 0.0 s vs ? 				vs 3.8 s    || 9.08248  vs    ?    vs 9.43362
#with open('.\..\..\Data_Json\Dictionnary\\12Dico.json', 'r') as f:   # 0.0 s vs 466.17s (8min) vs 0.0 s	|| 2.31822  vs 2.34025 vs 2.34025
#with open('.\..\..\Data_Json\Dictionnary\\11Dico.json', 'r') as f:   # 0.0 s vs 21.169s    	vs 0.0 s	|| 2.08734  vs 2.10937 vs 2.10937 
#with open('.\..\..\Data_Json\Dictionnary\\10Dico.json', 'r') as f:   # 0.0 s vs 5.195s  		vs 0.0 s    || 0.86158  vs 1.31749 vs 1.317489
    dico = json.load(f)



##############################################################################################################
##############################################################################################################
###################################### First Solution - Algorithme 1 #########################################

# Algo naive : first solution
# output = (sum, list_of_nodes, list_of_conflicts)

start = time.time()

output = [0,[],[]]
for elem in dico.items():
    (k,v) = elem
    if (int(k) not in output[2]) and (not((set(output[1]) & set(v[1])))): 
        output[0] += v[0]
        output[1].append(int(k))
        output[2] += v[1]
        output[2] = list(set(output[2]))

print((output[0],output[1]))


end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.5}s')

print('\n\n')



##############################################################################################################
##############################################################################################################
########################################  Calcule TOUT - Algorithme 2 ########################################

# Algo force brut : test any solution 
output = [0,[]]

# solution is a list of id_nodes
def test_solution(dico,solution):
    for i in range(0,len(solution)):
        for j in range(i+1,len(solution)):
            if (int(solution[i]) in dico[solution[j]][1]) or (int(solution[j]) in dico[solution[i]][1]):
                return False
    return True

# solution with all id_nodes
def max_solution(dico):
    solution = []
    for id in dico:
        solution.append(id)
    return solution

#sol = max_solution(dico)
#print(test_solution(dico,sol))

# from a solution give the list of all solutions minus one id_node
def list_of_subsolutions(solution):
    l = []
    for i in range(0,len(solution)):
        l.append([])
        for j in range(0,len(solution)):
            if j != i:
                l[i].append(solution[j])
    return l

#s = ['1','2','3','4']
#print(list_of_subsolutions(s))
# => [['2', '3', '4'], ['1', '3', '4'], ['1', '2', '4'], ['1', '2', '3']]

def best_solution(dico,solution,current):
    if test_solution(dico,solution):
        return solution
    else:
        l = list_of_subsolutions(solution)
        for sol in l:
            s = best_solution(dico,sol,current)
            if s not in current and s != current:
                current.append(s)
        return current
        
#print(best_solution(dico,max_solution(dico),[]))

#Return True if L1 is strictly include in L2, otherwhise False
def isInclude(L1, L2):
    return set(L1) < set(L2)

def clear_solution(solution):
    i = 0
    while i < len(solution):
        j = 0
        while j < len(solution):
            if isInclude(solution[i], solution[j]) and solution[i] in solution:
                del solution[solution.index(solution[i])]
                i-=1
                break
            j+=1
        i+=1
    return solution

#print(clear_solution(best_solution(dico,max_solution(dico),[])))


def list_max_sol(dico):
    return clear_solution(best_solution(dico,max_solution(dico),[]))


def sum_weight_list(dico,solution):
    sum = 0
    for id in solution:
        sum += dico[id][0]
    return sum

def max_sum_list(dico,l_sol):
    l_sum = []
    for sol in l_sol:
        l_sum.append(sum_weight_list(dico,sol))
    return (max(l_sum), l_sol[l_sum.index(max(l_sum))])


start = time.time()

print(max_sum_list(dico,list_max_sol(dico)))

end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.5}s')


##############################################################################################################
##############################################################################################################
########################################  OPTIMISATION - Algorithme 3 ######################################## 

def sum_weight(dico,solution):
    sum = 0
    for id in solution:
        sum += dico[str(id)][0]
    return sum

def max_sum_list_int(dico,l_sol):
    l_sum = []
    for sol in l_sol:
        l_sum.append(sum_weight(dico,sol[0]))
    return (max(l_sum), l_sol[l_sum.index(max(l_sum))])



def deletInclude(liste):
	i = 0
	while i < len(liste):
		j = i + 1 
		while j < len(liste):
			if set(liste[i][0]) < set(liste[j][0]):
				del liste[i]
			if set(liste[j][0]) < set(liste[i][0]):
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

start = time.time()

print(max_sum_list_int(dico,build_sol(dico)))

end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.5}s')

##############################################################################################################
##############################################################################################################