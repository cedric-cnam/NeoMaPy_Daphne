# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 18/08/2022

@author: Victor
"""

import json
import time

# Load the data

#with open('dicoConfNodes.json', 'r') as f:
with open('.\..\..\Data_Json\Dictionnary\smallDico.json', 'r') as f:
    dico = json.load(f)

##############################################################################################################
##############################################################################################################

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
        #print(f'subliste: {l}')
        for sol in l:
            s = best_solution(dico,sol,current)
            #print(f'courrante: {current}')
            #print(f'{s}\n')
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
    #print(l_sum)
    return (max(l_sum), l_sol[l_sum.index(max(l_sum))])


start = time.time()

print(max_sum_list(dico,list_max_sol(dico)))

end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.9}ms')