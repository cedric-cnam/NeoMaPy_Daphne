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

with open('.\..\..\Data_Json\Dictionnary\dicotIncNoConf_0_5k.json', 'r') as f:
    dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\ClearDico\dicotIncNoConfClear_0_5k_nrockit.json', 'r') as f2:
#    dico2 = json.load(f2)

##############################################################################################################
##############################################################################################################
##############################################  Algorithmes ################################################## 

def printSol2(l_sol):
    for l in l_sol:
        if 89 in l[0]:
            print(f'{l[0]}, {l[2]}')

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
    #print(f'len-sol = {len(l_sol)}')
    for sol in l_sol:
        l_sum.append(sum_weight(dico,sol[0]))
    return (max(l_sum), l_sol[l_sum.index(max(l_sum))][0])


def deletInclude(liste):
    i = 0
    while i < len(liste):
        j = i + 1 
        while j < len(liste):
            if (liste[i][0] < liste[j][0]):
                del liste[i]
                continue
            elif (liste[j][0] < liste[i][0]):
                del liste[j]	
                continue
            """
            if (liste[i][1] >= liste[j][1] and liste[i][2] < liste[j][2]):
                print("here i")
                del liste[i]
                continue
            elif (liste[j][1] >= liste[i][1] and liste[j][2] < liste[i][2]):
                print("here j")
                del liste[j]	
                continue
            """ 
            j += 1
        i += 1

"""
i = 43 + len(l_dico) = 107 et len_sol = 6392 
i = 44 + len(l_dico) = 107 et len_sol = 8394 
i = 45 + len(l_dico) = 107 et len_sol = 7068 
i = 46 + len(l_dico) = 107 et len_sol = 7635 
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


def end_sol(sol_init,index,dico):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    modulo = 4
    modulo2 = 2
    threshold = int(nb_nodes*0.67)
    #threshold = int(nb_nodes*0.33)
    liste_sol.append(sol_init)
    maxi = sol_init[2]
    max_sol = liste_sol[0]
    new_max = False
    winner = sol_init
    try_winner = False

    conf = sol_init[1]
    change = False

    set_nodes = set()
    for l in l_dico:
        set_nodes.add(int(l[0]))

    for i in range(index,len(l_dico)):
        
        if len(liste_sol) > 100:
            liste_sol2 = []
            for sol in liste_sol:
                s = end_sol(sol,i,dico)
                liste_sol2.append(s)
            change = True
            break



        if i not in conf:
            #print(f'end_sol : i = {i} + len(l_dico) = {len(l_dico)} et len_sol = {len(liste_sol)} ')
            j = 0
            h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste

        if new_max == True and (len(max_sol[0]) + len(max_sol[1]) > threshold):
            #print("la ?")
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
        #if index == 39:
            #print(f'i = {i}')

        while j < len(liste_sol)-h:
            #if index == 39:
                #print(f'j = {j}')
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
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
                    #best_sol = end_sol(liste_sol[j],i+1,dico)
                    #if index == 39:
                        #print(f'l_sol2 = {len(best_sol)}')
                    #end_sols.append(best_sol)
                    #del liste_sol[j]
                    #j -= 1 
                    
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        del liste_sol[j]
                        j -= 1 
                     
                    
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

        if i%modulo  == 0:    
            deletInclude(liste_sol)    

        #if i > threshold2 and i%modulo2==0:
        
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

    if change == False:
        best_score = 0
        for sol in liste_sol:
            for i2 in range(0,len(l_dico) ):
                if int(l_dico[i2][0]) not in sol[1] and int(l_dico[i2][0]) not in sol[0]:
                    sol[0].add(int(l_dico[i2][0]))
                    sol[1] |= set(l_dico[i2][1][1])
                    sol[2] += l_dico[i2][1][0]
            if sol[2] > best_score:
                best_score = sol[2]
                best_sol = sol
    else:
        best_score = 0
        for sol in liste_sol2:
            for i2 in range(0,len(l_dico)):
                if int(l_dico[i2][0]) not in sol[1] and int(l_dico[i2][0]) not in sol[0]:
                    sol[0].add(int(l_dico[i2][0]))
                    sol[1] |= set(l_dico[i2][1][1])
                    sol[2] += l_dico[i2][1][0]
            if sol[2] > best_score:
                best_score = sol[2]
                best_sol = sol      

    #if best_sol == []:
        #print("problem !!")
    return best_sol


# Build the solutions
def build_sol(dico,index):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    modulo = 4
    modulo2 = 2
    threshold = int(nb_nodes*0.67)
    #threshold = int(nb_nodes*0.95)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]
    max_sol = liste_sol[0]
    new_max = False
    winner = liste_sol[0]
    try_winner = False

    end = False
    end_sols = []

    #print(f'index = {index}')

    set_nodes = set()
    for l in l_dico:
        set_nodes.add(int(l[0]))
    
    #if index == 39:
        #print(f'l_dico = {len(l_dico)}')

    for i in range(0,len(l_dico)):
        #if index == 39:
            #print(f'i = {i} et l_sol = {len(liste_sol)}')
        if len(liste_sol)> 100:
            print(f'build sol : i = {i} + len(l_dico) = {len(l_dico)} et len_sol = {len(liste_sol)} ')
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste

        
        if len(liste_sol) > 100 :  
            for sol in liste_sol:
                best_sol = end_sol(sol,i,dico)
                end_sols.append(best_sol)
            end = True
            break
        

        #if i == 42:
            #printSol(liste_sol)
            #print(f'0 : {len(liste_sol[0][0]) + len(liste_sol[0][1])} / {len(l_dico)}')
            #print(f'1 : {len(liste_sol[1][0]) + len(liste_sol[1][1])} / {len(l_dico)}')
            #print(f'2 : {len(liste_sol[2][0]) + len(liste_sol[2][1])} / {len(l_dico)}')
            #print(f'3 : {len(liste_sol[3][0]) + len(liste_sol[3][1])} / {len(l_dico)}')
            #print(f'4 : {len(liste_sol[4][0]) + len(liste_sol[4][1])} / {len(l_dico)}')

        if new_max == True and (len(max_sol[0]) + len(max_sol[1]) > threshold):
            #print("la ?")
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
        #if index == 39:
            #print(f'i = {i}')

        while j < len(liste_sol)-h:
            #if index == 39:
                #print(f'j = {j}')
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
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
                    #best_sol = end_sol(liste_sol[j],i+1,dico)
                    #if index == 39:
                        #print(f'l_sol2 = {len(best_sol)}')
                    #end_sols.append(best_sol)
                    #del liste_sol[j]
                    #j -= 1 
                    
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        del liste_sol[j]
                        j -= 1 
                     
                    
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

        if i%modulo  == 0:    
            deletInclude(liste_sol)    

        #if i > threshold2 and i%modulo2==0:
        
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
            
    if end==False:
        end_sols = copy.deepcopy(liste_sol)
    
    for sol in end_sols:
        for i2 in range(0,i):
            if int(l_dico[i2][0]) not in sol[1] and int(l_dico[i2][0]) not in sol[0]:
                sol[0].add(int(l_dico[i2][0]))
                sol[1] |= set(l_dico[i2][1][1])
                sol[2] += l_dico[i2][1][0]
    

    #if index == 38:
    #print(f'end_sol = {end_sols}')
    #print(f'list_sol = {liste_sol}')
    
    return end_sols


##############################################################################################################
##############################################################################################################
###################################  OPTIMISATION 2 - Algorithme 3+ ########################################## 


##################################### LOAD the data for OPTI 2 ###############################################

with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k.json', 'r') as f: 	
    l_dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k_nrockit.json', 'r') as f: 	
    #l_dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k_nrockitClear.json', 'r') as f: 	
#    l_dico = json.load(f)

#################################### Apply Opti 1 on the list of dico ########################################
def solutionForList(l_dico):
    set_init = set()
    output = [0, set_init]
    i = 0
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
with open('n-rockit_solution_0_5k_avecC0.json', 'r') as f:
    l_rockit = json.load(f)

set_k = set()
for k,v in dico.items():
    set_k.add(int(k))

set_mapy = set(output1[1]).union(set_k)
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

"""
if __name__ == '__main__':
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_50_50kClear.json', 'r') as f: 
    with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_5k.json', 'r') as f: 	
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
"""