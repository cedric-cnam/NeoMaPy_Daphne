# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 07/10/2022

@author: Victor
"""

from ast import Continue
import json
from re import S, X
import time
import copy
import multiprocessing


##############################################################################################################
##############################################################################################################
###################################### LOAD the data  OPTI 1 #################################################
#with open('.\..\..\Data_Json\Dictionnary\dicoNoConf_0_5k.json', 'r') as f:
 #   dico = json.load(f)

with open('.\..\..\Data_Json\Dictionnary\dicoNoConf_0_5k_SansC0.json', 'r') as f:
    dico = json.load(f)

with open('.\..\..\Data_Json\Dictionnary\ClearDico\dicotIncNoConfClear_0_5k_nrockit.json', 'r') as f2:
    dico2 = json.load(f2)

##############################################################################################################
##############################################################################################################
##############################################  Algorithmes ################################################## 

def printSol(l_sol):
    for l in l_sol:
        print(f'{l[0]}, {l[2]}')


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
            if liste[i][0] < liste[j][0]:
                del liste[i]
                continue
            elif liste[j][0] < liste[i][0]:
                del liste[j]	
                continue
            j += 1
        i += 1


def deletIncludeHEAP(liste):
    i = 0
    while i < len(liste):
        j = len(liste) - 1 
        while j > i:
            if liste[i][0] > liste[j][0]:
                del liste[j]
            j -= 1
        i += 1


def compatible_merge(node,liste,dico):
    l_merge_comp = [{node}, set(dico[str(node)][1]), dico[str(node)][0]]
    if not(node in liste[1]):
        compatible = True
        l_merge_comp = []
    else:
        compatible = False
        for n in liste[0]:
            if not(node in dico[str(n)][1]):
                l_merge_comp[0].add(n)
                l_merge_comp[1] |= set(dico[str(n)][1])
                l_merge_comp[2] += dico[str(n)][0]
    return (l_merge_comp,compatible)
		
# To heapify subtree rooted at index i.
# n is size of heap
def heapify(arr, n, i):
    lowest = i  # Initialize lowest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2
 # See if left child of root exists and is
 # lower than root
    if l < n and arr[i][2] > arr[l][2]:
        lowest = l
 # See if right child of root exists and is
 # lower than root
    if r < n and arr[lowest][2] > arr[r][2]:
        lowest = r
 # Change root, if needed
    if lowest != i:
        (arr[i], arr[lowest]) = (arr[lowest], arr[i])  # swap
  # Heapify the root.
        heapify(arr, n, lowest)
 
 
# The main function to sort an array of given size
def heapSort(arr):
    n = len(arr)
 # Build a maxheap.
 # Since last parent will be at ((n//2)-1) we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
 # One by one extract elements
    for i in range(n - 1, 0, -1):
        (arr[i], arr[0]) = (arr[0], arr[i])  # swap
        heapify(arr, i, 0)

def accurate_MAP(dico):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    modulo = 4
    modulo2 = 2
    threshold = int(nb_nodes*0.67)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]
    max_sol = liste_sol[0]
    new_max = False
    try_winner = False
    winner = liste_sol[0]
    set_nodes = set()
    for l in l_dico:
        set_nodes.add(int(l[0]))

    for i in range(1,len(l_dico)):
        #print(f'accurate MAP: {i}/{len(l_dico)}')
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste
        if new_max == True and (len(max_sol[0]) + len(max_sol[1]) > threshold):
            potential_winner = copy.deepcopy(max_sol)
            new_max = False
            for k in range(i+1,len(l_dico)):
                if int(l_dico[k][0]) not in potential_winner[1]: 
                    potential_winner[0].add(int(l_dico[k][0]))
                    potential_winner[1] |= set(l_dico[k][1][1])
                    potential_winner[2] += l_dico[k][1][0]
            if potential_winner[2] > winner[2]:
                winner = copy.deepcopy(potential_winner)
                try_winner = True
        if try_winner:
            x = 0
            try_winner = False
            while x < len(liste_sol):                
                if len(liste_sol[x][0]) + len(liste_sol[x][1]) > threshold:
                    diff = set_nodes - liste_sol[x][1]
                    sum_max = 0
                    for n in diff:
                        sum_max += dico[str(n)][0]
                    if sum_max + liste_sol[x][2] < winner[2]:
                        set_id = set()
                        for l in liste_sol:
                            if l != liste_sol[x]:
                                set_id |= l[0]
                        set_diff = liste_sol[x][0] - set_id
                        if len(set_diff) == 0:
                            del liste_sol[x]
                            x -= 1
                        else: # solution ne pouvant gagner mais avec des nodes a garder => new sol contient uniquement new nodes
                            liste_sol[x][0] = set_diff
                            liste_sol[x][1] = set()
                            liste_sol[x][2] = 0
                            for n in liste_sol[x][0]:
                                liste_sol[x][1] |= set(dico[str(n)][1])
                                liste_sol[x][2] += dico[str(n)][0]
                x += 1 

        while j < len(liste_sol)-h:
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] += l_dico[i][1][0]
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]
                    max_sol = copy.deepcopy(liste_sol[j]) 
                    new_max = True
                if len(liste_sol[j][0]) + len(liste_sol[j][1]) > threshold:
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        del liste_sol[j]
                        j -= 1 
            else:
                include = False
                for l in liste_sol:
                    if l2[0] <= l[0]: #or l2[0]>l[0]:
                        include = True
                        break
                if not(include):
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
                        max_sol = copy.deepcopy(l2)
                        new_max = True
            j += 1
        if i%modulo  == 0:    
            deletInclude(liste_sol)    

        if i%modulo2 == 0:
            x = 0
            while x < len(liste_sol):                
                if len(liste_sol[x][0]) + len(liste_sol[x][1]) > threshold:
                    diff = (set_nodes - liste_sol[x][1]) - liste_sol[x][0]
                    sum_max = 0
                    for n in diff:
                        sum_max += dico[str(n)][0]
                    if sum_max + liste_sol[x][2] < maxi:
                        set_id = set()
                        for l in liste_sol:
                            if l != liste_sol[x]:
                                set_id |= l[0]
                        set_diff = liste_sol[x][0] - set_id
                        if len(set_diff) == 0:
                            del liste_sol[x]
                            x -= 1
                        else:
                            liste_sol[x][0] = set_diff
                            liste_sol[x][1] = set()
                            liste_sol[x][2] = 0
                            for n in liste_sol[x][0]:
                                liste_sol[x][1] |= set(dico[str(n)][1])
                                liste_sol[x][2] += dico[str(n)][0]
                x += 1 
    return liste_sol

#def fast_MAP(dico,liste_sol,i,set_nodes,new_max,maxi,max_sol,winner,try_winner):
def fast_MAP(dico):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    modulo = 3
    threshold = int(nb_nodes*0.67)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]
    max_sol = liste_sol[0]
    new_max = False
    winner = liste_sol[0]
    set_nodes = set()
    for l in l_dico:
        set_nodes.add(int(l[0]))

    for i in range(1,len(l_dico)):
        #print(f'fast MAP: {i}/{len(l_dico)} and nb sol = {len(liste_sol)}')
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste
        if new_max == True and (len(max_sol[0]) + len(max_sol[1]) > threshold):
            potential_winner = copy.deepcopy(max_sol)
            new_max = False
            for k in range(i+1,len(l_dico)):
                if int(l_dico[k][0]) not in potential_winner[1]:
                    potential_winner[0].add(int(l_dico[k][0]))
                    potential_winner[1] |= set(l_dico[k][1][1])
                    potential_winner[2] += l_dico[k][1][0]
            if potential_winner[2] > winner[2]:
                winner = copy.deepcopy(potential_winner)  

        while j < len(liste_sol)-h:
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] += l_dico[i][1][0]
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]
                    max_sol = copy.deepcopy(liste_sol[j])  
                    new_max = True
            else:
                include = False
                for l in liste_sol:
                    if l2[0] <= l[0]:# or l2[0]>l[0]:
                        include = True
                        break
                if not(include):
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
                        max_sol = copy.deepcopy(l2)
                        new_max = True
            j += 1

        #if len(liste_sol) > 500:
         #   heapSort(liste_sol)
          #  liste_sol = liste_sol[:500]

        if i%modulo  == 0 :    
            #print(f'first = {liste_sol[0][2]} last = {liste_sol[len(liste_sol)-1][2]}') 
            heapSort(liste_sol)
            #print(f'first = {liste_sol[0][2]} last = {liste_sol[len(liste_sol)-1][2]}')
            if len(liste_sol) < 100:
                deletIncludeHEAP(liste_sol) 
            else:
                liste_sol = liste_sol[:100]
                   
            x = 0
            while x < len(liste_sol):                
                if len(liste_sol[x][0]) + len(liste_sol[x][1]) > threshold:
                    diff = (set_nodes - liste_sol[x][1]) - liste_sol[x][0]
                    sum_max = 0
                    for n in diff:
                        sum_max += dico[str(n)][0]
                    if sum_max + liste_sol[x][2] < winner[2]:
                        set_id = set()
                        for l in liste_sol:
                            if l != liste_sol[x]:
                                set_id |= l[0]
                        set_diff = liste_sol[x][0] - set_id
                        if len(set_diff) == 0:
                                del liste_sol[x]
                                x -= 1
                        else: # solution ne pouvant gagner mais avec des nodes a garder => new sol contient uniquement new nodes                           
                                liste_sol[x][0] = set_diff
                                liste_sol[x][1] = set()
                                liste_sol[x][2] = 0
                                for n in liste_sol[x][0]:
                                    liste_sol[x][1] |= set(dico[str(n)][1])
                                    liste_sol[x][2] += dico[str(n)][0] 
                x += 1     
                
    return liste_sol

# Build the solutions
def build_sol(dico):
    l_dico = list(dico.items())
    if len(l_dico[0][1][1]) < 30:
        liste_sol = accurate_MAP(dico)
    else:  
        liste_sol = fast_MAP(dico)
    for sol in liste_sol:
        for i2 in range(0,len(l_dico)):
            if int(l_dico[i2][0]) not in sol[1] and int(l_dico[i2][0]) not in sol[0]:
                sol[0].add(int(l_dico[i2][0]))
                sol[1] |= set(l_dico[i2][1][1])
                sol[2] += l_dico[i2][1][0]
    return liste_sol


##############################################################################################################
##############################################################################################################
###################################  OPTIMISATION 2 - Algorithme 3+ ########################################## 


##################################### LOAD the data for OPTI 2 ###############################################

with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico_0_5k_SansC0.json', 'r') as f: 	
    l_dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k.json', 'r') as f: 	
#    l_dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k_nrockitClear.json', 'r') as f: 	
    #l_dico = json.load(f)

#################################### Apply Opti 1 on the list of dico ########################################
def solutionForList(l_dico):
    set_init = set()
    output = [0, set_init]
    i = 0
    for dico in l_dico["list"]:
        print(f'{i}/{len(l_dico["list"])} with {len(dico)}')
        val,liste = max_sum_list_int(dico,build_sol(dico))
        output[0] += val
        output[1] |= set(liste)
        i+=1
    return output


"""
start = time.time()
output1 = solutionForList(l_dico)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution conf : {elapsed:.5}s')
print(output1[0])
#output12 = sum_weight(dico2,dico2)
#print(output12)

output2 = sum_weight(dico,dico)
#output22 = sum_weight(dico2,dico2)
print(output2)
#print(output22)
print(f'Score total MaPy = {output1[0] + output2}')# + output22}')
#print(f'Score Rockit = 1097.7027803900003')
#print(f'Score Rockit sameAS = 505.30539979')
#print(f'Score Rockit sameAS tinc = 505.26962978')

#print(f'Score total = {output1[0] + output12 + output2}')
print(len(output1[1])+len(dico))#+len(dico2))
#print(output1[1])

"""

"""
file_solution = open("solution_0_5k.json","w")
sum = 0
file_solution.write("[")
i = 1
for sol in output1[1]:
    file_solution.write(str(sol))
    if i < len(output1[1]):
        file_solution.write(",\n")
    else:
        file_solution.write("\n")
    for dico in l_dico:
        if sol == dico["Node_id"]:
            #if dico["weight"] < 100:
            sum += dico["weight"]
    i += 1

file_solution.write("]")           
print(f'sum = {sum}')
"""

"""
3000-1500serie
Temps d'exécution conf : 501.73s
4.611686e+19
3159.402000000004
Score total MaPy = 4.611686e+19
1951

2000-1000//
Temps d'exécution conf : 111.36s
46118877.99620002
len sol conf = 716
Temps d'exécution no conf : 0.0s
3159.402000000004
nb nodes no conf = 1286
nb nodes total = 2002
Score total = 46122037.39820002
"""



#with open('n-rockit_solution_0_5k_avecC0.json', 'r') as f:
    #l_rockit = json.load(f)

"""
set_k = set()
for k,v in dico.items():
    set_k.add(int(k))

set_mapy = set(output1[1]).union(set_k)
"""

"""
set_rockit = set(l_rockit)

diff1 = set_mapy.difference(set_rockit)
print(f'diff mapy - rockit = {diff1}\n')
print(len(diff1))

diff2 = set_rockit.difference(set_mapy)
print(f'diff rockit - mapy = {diff2}')
print(len(diff2))


set_conf = set()
sum = 0
q = 0
for id in set_rockit:
    #if q == 0:
        #print(f'type id = {type(id)}')
        #q += 1
    for dico in l_dico["list"]:
        #"if q == 1:
            #print(dico)
            #q += 1
        if str(id) in dico:
            #if q == 1 or q == 2:
                #print(f'ici')
                #q += 1
            for conf in dico[str(id)][1]:
                if int(conf) in set_rockit:
                    set_conf.add(int(conf))
                    set_conf.add(int(id))
                    sum += 1

#print(f'nb conflit rockit = {sum}')

print(f'nb nodes conflit rockit = {len(set_conf)}')
print(set_conf)
#without sA = 1566
#sameAS = 21
"""

"""
sum = 0
q = 0
for id in set_mapy:
    if q == 0:
        #print(f'type id = {type(id)}')
        q += 1
    for dico in l_dico["list"]:
        if q == 1:
            #print(dico)
            q += 1
        if str(id) in dico:
            if q == 1 or q == 2:
                #print(f'ici')
                q +=1
            for conf in dico[str(id)][1]:
                if int(conf) in set_mapy:
                    sum += 1

print(f'nb conflit mapy = {sum}')
"""


############################################ Parallelization #################################################


def task(dico):
	val,liste = max_sum_list_int(dico,build_sol(dico))
	return val,liste


def parallelization(l_dico):
	output = [0,[]]
	pool = multiprocessing.Pool(2)
	result = pool.imap(task, l_dico["list"])
	for val,liste in result:
		output[0] += val
		output[1] += liste
	return output


if __name__ == '__main__':
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_50_50k.json', 'r') as f: 
    with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico_0_5k_SansC0.json', 'r') as f: 	
        l_dico = json.load(f)

    
    print(f'{len(l_dico["list"])}')
    start = time.time()
    output1 = parallelization(l_dico)
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution conf : {elapsed:.5}s\n')
    print(output1[0])
    print(f'len sol conf = {len(output1[1])}')

    start = time.time()
    output2 = sum_weight(dico,dico)
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution no conf : {elapsed:.5}s\n')
    print(output2)

    
    print(f'nb nodes no conf = {len(dico)}')
    print(f'nb nodes total = {len(output1[1]) + len(dico)}')
    #print(f'Score total = {output1[0] + output12 + output2}')
    print(f'Score total = {output1[0] + output2}')
    
    
    """
    with open('solution_0_5k.json', 'r') as f:
        l_rockit = json.load(f)

    #set_k = set()
    #for k,v in dico.items():
        #set_k.add(int(k))
    #set_mapy = set(output1[1]).union(set_k)

    set_rockit = set(l_rockit)
    """
    
    """
    diff1 = set_mapy.difference(set_rockit)
    print(f'diff mapy - rockit = {diff1}\n')
    print(len(diff1))

    diff2 = set_rockit.difference(set_mapy)
    print(f'diff rockit - mapy = {diff2}')
    print(len(diff2))
    """
    
    """
    set_conf = set()
    for id in set_rockit:
        for dico in l_dico["list"]:
            if str(id) in dico:
                for conf in dico[str(id)][1]:
                    if int(conf) in set_rockit:
                        set_conf.add(int(id))
                        break

    print(f'nb conflicts rockit = {len(set_conf)}')
    print(set_conf)
    """

    """
    70:
    {5765, 5766, 2698, 2699, 2576, 2577, 2594, 2595, 6309, 6310, 2603, 4523, 2605, 4142, 4143, 4524, 
    4527, 3762, 3763, 4528, 6321, 6322, 6712, 6713, 4542, 4159, 2624, 2623, 4160, 4419, 4420, 4543, 4422,
    4423, 4548, 4169, 4170, 4298, 4172, 4173, 3790, 3791, 4299, 4425, 4426, 4434, 7375, 7376, 7261, 7262, 3682, 3683, 4453, 4455,
    4456, 4549, 4202, 4203, 6892, 6893, 7015, 7016, 4464, 5873, 5874, 6134, 6135, 6136, 5243, 5244}
    """


    """
    set_conf = set()
    for id in set_mapy:
        for dico in l_dico["list"]:
            if str(id) in dico:
                for conf in dico[str(id)][1]:
                    if int(conf) in set_mapy:
                        set_conf.add(int(id))
                        break

    print(f'nb conflicts mapy = {len(set_conf)}')
    
    """