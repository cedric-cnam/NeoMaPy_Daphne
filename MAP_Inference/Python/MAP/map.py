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
with open('smallDico.json', 'r') as f:
    dico = json.load(f)

##############################################################################################################
##############################################################################################################


# Algo naive : first solution
# output = (sum, list_of_nodes, list_of_conflicts)

start = time.time()

output = [0,[],[]]
for elem in dico.items():
    (k,v) = elem
    #print(f'k: {k}, output[1]: {output[1]}, output[2]: {output[2]}, v[1]: {v[1]}')
    if (int(k) not in output[2]) and (int(k) not in v[1]) and (not((set(output[1]) & set(v[1])))):
        output[0] += v[0]
        output[1].append(int(k))
        output[2] += v[1]
        list(set(output[2]))

print((output[0],output[1]))


end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.9}ms')

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

##############################################################################################################
##############################################################################################################

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

##############################################################################################################
##############################################################################################################
##  OPTI A FAIRE ##

# from a solution give the list of all solutions minus one id_node
def opti_list_of_subsolutions(solution,dico):
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

def opti_best_solution(dico,solution,current):
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

##############################################################################################################
##############################################################################################################

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

"""
    ,
	"67": [0.17252001, [83]],
	"73": [0.20397, [83]],
	"100": [0.18592, [108]],
	"107": [0.24195, [105]],
	"113": [0.46576, [166]],
	"138": [0.22402, [166]],
	"145": [0.20755, [166]],
	"153": [0.2441, [166]],
	"162": [0.33468002, [166]],
	"165": [0.14474, [166]],
	"167": [0.17898001, [168]],
	"168": [0.17043, [167]],
    "175": [0.24155, [176]],
	"176": [0.32017, [175]],
	"177": [0.24866, [178]],
	"178": [0.29939002, [177]],
	"181": [0.18523, [182]],
	"182": [0.20038, [181]],
	"188": [0.17377, [189]],
	"189": [0.23321, [188]],
	"194": [0.17857, [195]],
	"195": [0.23271, [194]],
	"198": [0.18506, [199]],
	"199": [0.25609, [198]],
	"205": [0.40396, [206]],
	"206": [0.21610999, [205]],
	"215": [0.17807999, [217]],
	"216": [0.21503, [217]],
	"218": [0.19359, [219]],
	"219": [0.33287, [218]],
	"220": [0.30458, [221]],
	"221": [0.21164998, [220]],
	"222": [0.15022, [223]],
	"223": [0.25066, [222]],
	"224": [0.2214, [225]],
	"225": [0.21632, [224]],
	"230": [0.19597, [231]],
	"231": [0.29549998, [230]],
	"234": [0.29113, [278]],
	"235": [0.24142, [278]],
	"236": [0.27098, [278]],
	"237": [0.17906, [278]],
	"238": [0.20515001, [278]],
	"241": [0.14552, [278]],
	"244": [0.54685, [278]],
	"245": [0.39282, [278]],
	"249": [0.32452, [278]],
	"255": [0.34094998, [278]],
	"256": [0.1752, [278]],
	"261": [0.16288, [278]],
	"262": [0.18153, [278]],
	"263": [0.22276, [278]],
	"291": [0.19404, [296]],
	"294": [0.24356, [301]],
	"296": [0.33871, [291]],
	"299": [0.14242001, [301]],
	"306": [0.19018, [307]],
	"307": [0.15582, [306]],
	"308": [0.19477001, [309]],
	"309": [0.34094998, [308]],
	"310": [0.1798, [311]],
	"311": [0.38132, [310]],
	"312": [0.51794, [313]],
	"313": [0.81113994, [312]],
	"314": [0.35732, [315]],
	"315": [0.65699, [314]],
	"319": [0.16056, [318]],
	"320": [0.45653, [318]],
	"322": [0.31099, [323]],
	"323": [0.22907, [322]],
	"324": [0.52734, [325]],
	"325": [0.38371998, [324]],
	"326": [0.16648999, [327]],
	"327": [0.25775, [326]],
	"329": [0.17036, [330]],
	"330": [0.25297, [329]],
	"335": [0.22072999, [336]],
	"336": [0.17345999, [335]],
	"339": [0.2375, [340]],
	"340": [0.19487, [339]],
	"341": [0.25684, [342]],
	"342": [0.24221, [341]],
	"344": [0.21031001, [345]],
	"345": [0.17607, [344]],
	"346": [0.14045, [347]],
	"347": [0.23321, [346]],
	"357": [0.20416, [358]],
	"358": [0.37579, [357]]
"""