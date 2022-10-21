# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 16/09/2022

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
with open('.\..\..\Data_Json\Dictionnary\dicotIncNoConf_100_50k.json', 'r') as f:
    dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\dicotIncNoConf_0_5k.json', 'r') as f:
    #dico = json.load(f)

with open('.\..\..\Data_Json\Dictionnary\ClearDico\dicotIncNoConfClear_0_5k_nrockit.json', 'r') as f2:
    dico2 = json.load(f2)

##############################################################################################################
##############################################################################################################
##############################################  Algorithmes ################################################## 

def printSol2(l_sol):
    for l in l_sol:
        if 89 in l[0]:
            print(f'{l[0]}, {l[2]}')

def printSol(l_sol):
    for l in l_sol:
        print(f'{l[0]}, {l[1]}, {l[2]}')


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

"""
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
"""

def dec(l_sol):
    l_croi = [l_sol[0]]
    for i in range(1,len(l_sol)):
        add = False
        for j in range (0,len(l_croi)):
            if len(l_sol[i]) >= len(l_croi[j]):
                l_croi.insert(j,l_sol[i])
                add = True
                break
        if add == False:
            l_croi.insert(j+1,l_sol[i])
    return l_croi


def deletInclude(liste):
    i = 0
    #if len(liste) > 10000:
    if len(liste) > 4000:
        l_dec = dec(liste)
        while i < len(l_dec):
            j = len(l_dec) - 1 
            while j > i:
                if l_dec[i][0] > l_dec[j][0]:
                    del l_dec[j]
                j -= 1
            i += 1
        return l_dec
    else:
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
        return liste


"""
def deletInclude(liste,index,dico):
    i = 0
    if len(liste) > 5000:
        l_dico = list(dico.items())
        for sol in liste:
            for ind in range(0,index+1):
                if int(l_dico[ind][0]) not in sol[1]:
                    sol[0].add(int(l_dico[ind][0]))
                        
        l_dec = dec(liste)
        while i < len(l_dec)-1:
        #i = len(liste)
        #while i > 0:    
            j = i + 1
            #j = len(l_dec) - 1
            while j<len(l_dec) and len(l_dec[i][0]) == len(l_dec[j][0]):
            #while j > i:
                if l_dec[i][0] == l_dec[j][0]:
                    if l_dec[i][2] >= l_dec[j][2]:
                        del l_dec[j]
                        #j += 1
                        continue
                    else:
                        del l_dec[i]
                        #j += 1
                        break
                #j += 1
                j += 1
            i += 1
        return l_dec
    else:
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
        return liste        
"""

#liste = [[id_nodes],[conflicts]]
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
		

# Build the solutions
def build_sol(dico):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    modulo = 4
    modulo2 = 2
    threshold = int(nb_nodes*0.67)
    #threshold = int(nb_nodes*0.33)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]
    max_sol = liste_sol[0]
    new_max = False
    winner = liste_sol[0]
    try_winner = False

    set_nodes = set()
    for l in l_dico:
        set_nodes.add(int(l[0]))

    for i in range(0,len(l_dico)):
        #print(f'i = {i} + len(l_dico) = {len(l_dico)} et len_sol = {len(liste_sol)} ')
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste

        """
        if i == 48:
            maxim = 0
            for solu in liste_sol:
                if len(solu[0])+len(solu[1]) > maxim:
                    maxim = len(solu[0])+len(solu[1])
            print(maxim)
            #printSol(liste_sol)
        """

        if new_max == True and (len(max_sol[0]) + len(max_sol[1]) > threshold):
            #print("la ?")
            #start = time.time()
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
            #end = time.time()
            #elapsed = end - start
            #if elapsed > 0.5:
            #    print(f'Temps d\'exécution new max : {elapsed:.5}s')

        if try_winner:
            x = 0
            try_winner = False
            #start = time.time()
            while x < len(liste_sol):                
                if len(liste_sol[x][0]) + len(liste_sol[x][1]) > threshold:
                    #print("ici ?")
                    """
                    potential_max = liste_sol[x][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0] 
                    if potential_max < winner[2]:
                        del liste_sol[x]
                        x -= 1
                    """

                    diff = (set_nodes - liste_sol[x][1]) #- liste_sol[x][0]
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
                            #potential_max = liste_sol[x][2]
                            #for k in range(i+1,len(l_dico)):
                            #    potential_max += l_dico[k][1][0] 
                            #if potential_max < winner[2]:
                                liste_sol[x][0] = set_diff
                                liste_sol[x][1] = set()
                                liste_sol[x][2] = 0
                                for n in liste_sol[x][0]:
                                    liste_sol[x][1] |= set(dico[str(n)][1])
                                    liste_sol[x][2] += dico[str(n)][0] 
                x += 1 
            #end = time.time()
            #elapsed = end - start
            #if elapsed > 0.5:
            #    print(f'Temps d\'exécution try winner : {elapsed:.5}s')
        
        while j < len(liste_sol)-h:
            #start = time.time()
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
            #end = time.time()
            #elapsed = end - start
            #if elapsed > 0.5:
             #   print(f'Temps d\'exécution compatible : {elapsed:.5}s')
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] += l_dico[i][1][0]
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]
                    max_sol = copy.deepcopy(liste_sol[j])  
                    new_max = True
                
                #if i > threshold2:
                if len(liste_sol[j][0]) + len(liste_sol[j][1]) > threshold:
                    #start = time.time()
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        """
                        set_id = set()
                        for l in liste_sol:
                            if l != liste_sol[j]:
                                set_id |= l[0]
                        set_diff = liste_sol[j][0] - set_id
                        if len(set_diff) == 0:
                            """
                        del liste_sol[j]
                        j -= 1 
                        """
                        else:
                            liste_sol[j][0] = set_diff
                            liste_sol[j][1] = set()
                            liste_sol[j][2] = 0
                            for n in liste_sol[j][0]:
                                liste_sol[j][1] |= set(dico[str(n)][1])
                                liste_sol[j][2] += dico[str(n)][0]      
                            """
                    #end = time.time()
                    #elapsed = end - start
                    #if elapsed > 0.5:
                    #    print(f'Temps d\'exécution if bool : {elapsed:.5}s')
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
        
        if i%modulo  == 0 :#or (len(liste_sol)>10000 and i%2== 0 ):    
            #start = time.time()
            liste_sol = deletInclude(liste_sol)   
            #end = time.time()
            #elapsed = end - start
            #if elapsed > 0.5:
              #  print(f'Temps d\'exécution deletInclude : {elapsed:.5}s') 
        
        #if i > threshold2 and i%modulo2==0:
        
        if i%modulo2 == 0:
            #start = time.time()
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
            #end = time.time()
            #elapsed = end - start
            #if elapsed > 0.5:
             #   print(f'Temps d\'exécution last opti : {elapsed:.5}s')

    for sol in liste_sol:
        for i2 in range(0,i):
            if int(l_dico[i2][0]) not in sol[1] and int(l_dico[i2][0]) not in sol[0]:
                sol[0].add(int(l_dico[i2][0]))
                sol[1] |= set(l_dico[i2][1][1])
                sol[2] += l_dico[i2][1][0]
    
    return liste_sol


##############################################################################################################
##############################################################################################################
###################################  OPTIMISATION 2 - Algorithme 3+ ########################################## 


##################################### LOAD the data for OPTI 2 ###############################################

with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k_nrockit.json', 'r') as f: 	
    l_dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k.json', 'r') as f: 	
#    l_dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k_nrockitClear.json', 'r') as f: 	
    #l_dico = json.load(f)

#################################### Apply Opti 1 on the list of dico ########################################
def solutionForList(l_dico):
    set_init = set()
    output = [0, set_init]
    i = 1
    size = len(l_dico["list"])
    for dico in l_dico["list"]:
        #start = time.time()
        print(f"{i}/ {size} : {len(dico)}")
        val,liste = max_sum_list_int(dico,build_sol(dico,i))
        output[0] += val
        output[1] |= set(liste)
        #if len(dico) > 50:
        #    end = time.time()
        #elapsed = end - start
        #if elapsed > 1:
        #    print(f'Temps d\'exécution {i} / {size} avec len = {len(dico)} et time: {elapsed:.5}s')
        i += 1
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



#with open('n-rockit_solution_0_5k_avecC0.json', 'r') as f:
    #l_rockit = json.load(f)

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
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_50_50kClear.json', 'r') as f: 
    with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_100_50k.json', 'r') as f: 	
        l_dico = json.load(f)

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
