### json to dico
# -*- coding: utf-8 -*-
"""
Created on 17/08/2022
Last update 10/09/2022

@author: Victor
"""

import json
import sys

from ast import Continue
import json
from re import S, X
import time
import copy
import multiprocessing


if len( sys.argv ) != 5:
    print( "Please give the 4 following parameters:" )
    print( "1. your initial json file containing the conflicting nodes," )
    print( "2. your initial json file containing the non conflicting nodes," )
    print( "3. the integer k = top element to keep during the algo of MaPy." )
    print( "4. the float of the threshold or use 0 for no threshold." )
    exit()

# Give your initial json file containing the conflicting nodes
#data_conf = '.\..\..\Data_Json\Initial_Data\conflicts_75_200k.json'
data_conf = sys.argv[1]
with open(data_conf, 'r') as f:
    liste_conf = json.load(f)


# Give your initial json file containing the non conflicting nodes
#data_noconf = '.\..\..\Data_Json\Initial_Data\\noConflicts_75_200k.json'
data_noconf = sys.argv[2]
with open(data_noconf, 'r') as f2:
    liste_noconf = json.load(f2)

global topk
topk = int(sys.argv[3])
seuil = float(sys.argv[4])


##############################################################################################################
##############################################################################################################


# Creation of the dictionnary of conflincting nodes where (key,value) is ('id' : [weight, listOfConflicts])
if seuil > 0:
    set_del_node = set()

dico_conf = {}
for i in liste_conf:
    id = i["Node_id"]
    w = i["weight"]
    conf = i["Conflicts_node_ids"]
    if seuil > 0:
        if w > seuil:
            dico_conf[id] = (w,conf)
        else:
            set_del_node.add(id)
    else:
        dico_conf[id] = (w,conf)

if seuil > 0:
    for id in dico_conf:
        set_conf = set(dico_conf[id][1])
        new_conf = list(set_conf - set_del_node)
        w = dico_conf[id][0]
        dico_conf[id] = (w,new_conf)


# Creation of the dictionnary of non conflincting nodes where (key,value) is ('id' : [weight, []])
dico_noconf = {}
for i in liste_noconf:
    id = i["Node_id"]
    w = i["weight"]
    conf = []
    if seuil > 0:
        if w > seuil:
            dico_noconf[id] = (w,conf)
    else:
        dico_noconf[id] = (w,conf)


##############################################################################################################
##############################################################################################################


# Creation of the json file of this dictionnary of conflicting nodes 
fichier_conf = open("dicoConf.json", "w")
fichier_conf.write("{\n")
size = len(dico_conf)
i = 1
for (k,v) in dico_conf.items():
    fichier_conf.write("\t\"")
    fichier_conf.write(str(k))
    fichier_conf.write("\": [")
    fichier_conf.write(str(v[0]))
    fichier_conf.write(", ")
    fichier_conf.write(str(v[1]))
    if i != size:    
        fichier_conf.write("],\n")
    else:
        fichier_conf.write("]\n")
    i += 1
fichier_conf.write("}")
fichier_conf.close()


# Creation of the json file of this dictionnary of non conflicting nodes 
fichier_noconf = open("dicoNoConf.json", "w")
fichier_noconf.write("{\n")
size = len(dico_noconf)
i = 1
for (k,v) in dico_noconf.items():
    fichier_noconf.write("\t\"")
    fichier_noconf.write(str(k))
    fichier_noconf.write("\": [")
    fichier_noconf.write(str(v[0]))
    fichier_noconf.write(", ")
    fichier_noconf.write(str(v[1]))
    if i != size:    
        fichier_noconf.write("],\n")
    else:
        fichier_noconf.write("]\n")
    i += 1
fichier_noconf.write("}")
fichier_noconf.close()


##############################################################################################################
##############################################################################################################



##############################################################################################################
##############################################################################################################
############################################## LOAD the data #################################################

#start = time.time()
data_conf = '.\dicoConf.json'
#data_conf = '.\..\..\Data_Json\Dictionnary\ClearDico\dicotIncConfClear_75_200k_nrockit.json'
with open(data_conf, 'r') as f:     
    dic = json.load(f)


def oneDico(key, dico, l_id, d_out):
    for n in dico[str(key)][1]:
        if n not in l_id:
            l_id += [int(n)]
            d_out[str(n)]= dico[str(n)]
            l_id,d_out = oneDico(str(n), dico, l_id, d_out)
    return l_id,d_out


def decrease(dico):
    l_deso = list(dico.items())
    l_croi = [l_deso[0]]
    for i in range(1,len(l_deso)):
        add = False
        for j in range (0,len(l_croi)):
            if len(l_deso[i][1][1]) >= len(l_croi[j][1][1]):
                l_croi.insert(j,l_deso[i])
                add = True
                break
        if add == False:
            l_croi.insert(j+1,l_deso[i])
    dico_output = {}
    for elem in l_croi:
        dico_output[elem[0]] = elem[1]
    return dico_output


def Ndico(dico):
    l_id_total = set()
    d_total = []    
    for k in dico:
        if int(k) not in l_id_total:
            d_out = {}
            d_out[str(k)] = dico[str(k)]
            l_id, d_out = oneDico(k, dico, [int(k)], d_out)
            #d_total.append(decrease(d_out))
            d_total.append(d_out)
            l_id_total.update(set(l_id))
    return d_total


##############################################################################################################
##############################################################################################################
############################################## Write the data ################################################

# Creation of the json file of this dictionnary    
fichier = open("listOfDico.json", "w")
#fichier = open("listOfDicotInc_75_200k_nrockitClear.json", "w")
fichier.write("{\n")
fichier.write("\t \"list\": [\n")
ListeOfDicos = Ndico(dic)
i = 1
for dico in ListeOfDicos:
    fichier.write("\t\t")
    fichier.write("{")
    size = len(dico)
    j = 1
    for (k,v) in dico.items():
        fichier.write("\"")
        fichier.write(str(k))
        fichier.write("\": [")
        fichier.write(str(v[0]))
        fichier.write(", ")
        fichier.write(str(v[1]))
        if j != size:    
            fichier.write("],")
        else:
            fichier.write("]")
        j += 1
    fichier.write("}")
    if i < len(ListeOfDicos):
        fichier.write(", \n")
        i += 1
    else:
        fichier.write("\n")
fichier.write("\t ]\n")
fichier.write("}")
fichier.close() 

#end = time.time()
#elapsed = end - start
#print(f'Temps d\'exécution : {elapsed:.5}s')


##############################################################################################################
##############################################################################################################
###################################### LOAD the data  OPTI 1 #################################################

def sum(numbers):
    sum = 0
    for x in numbers:
        sum += x
    return sum

def psum(numbers,alpha):
    sum = 0
    for x in numbers:
        sum += x**alpha
    return sum**(1/alpha)



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
            #topk = 100
            if len(liste_sol) < topk:
                deletIncludeHEAP(liste_sol) 
            else:
                liste_sol = liste_sol[:topk]
                   
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

"""
with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico_25_200k.json', 'r') as f: 	
    l_dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_25_200k.json', 'r') as f: 	
#    l_dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_25_200k_nrockitClear.json', 'r') as f: 	
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
    with open('.\dicoNoConf.json', 'r') as f:
        dico = json.load(f)

    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_25_200k.json', 'r') as f: 
    with open('.\listOfDico.json', 'r') as f: 	
        l_dico = json.load(f)

    
    #print(f'number of sub dico = {len(l_dico["list"])}\n')
    start = time.time()
    output1 = parallelization(l_dico)
    end = time.time()
    elapsed = end - start
    #print(f'Execution time conflict : {elapsed:.5}s')
    time_conf = elapsed
    #print(f'Solution weight in conflict file : {output1[0]}\n')

    start = time.time()
    output2 = sum_weight(dico,dico)
    end = time.time()
    elapsed = end - start
    #print(f'Execution time no conflict : {elapsed:.5}s')
    time_noconf = elapsed
    #print(f'Solution weight in NO conflict file : {output2}\n')

    #print(f'nb nodes conf = {len(output1[1])}')
    #print(f'nb nodes no conf = {len(dico)}')
    #print(f'nb nodes total = {len(output1[1]) + len(dico)}')
    #print(f'Score total = {output1[0] + output12 + output2}')
    #print(f'Score total = {output1[0] + output2}')
    
    ############################################## Write the data ################################################

    # Creation of the output solutions   
    fichier = open("solutions_MaPy.txt", "w")
    for id in dico:
        fichier.write(str(id))
        fichier.write("\n")
        
    for sol in output1[1]:
        fichier.write(str(sol))
        fichier.write("\n")

    fichier.close()     



    # Creation of the output statistic 
    fichier = open("statistics_MaPy.txt", "w")
    
    fichier.write("Number of sub dictionary: ")
    fichier.write(str(len(l_dico["list"])))
    fichier.write("\n\n")

    fichier.write("Time execution for conflicts: ")
    fichier.write(str(time_conf))
    fichier.write(" secondes \n")
     
    fichier.write("Time execution for no conflicts: ")
    fichier.write(str(time_noconf))
    fichier.write(" secondes \n") 

    fichier.write("Time execution total: ")
    time_total = time_conf + time_noconf
    fichier.write(str(time_total))
    fichier.write(" secondes \n\n") 

    fichier.write("Weight of solutions in conflicts: ")
    fichier.write(str(output1[0]))
    fichier.write("\n") 

    fichier.write("Weight of solutions in no conflicts: ")
    fichier.write(str(output2))
    fichier.write("\n") 

    fichier.write("Weight of solutions in total: ")
    total = output1[0] + output2
    fichier.write(str(total))
    fichier.write("\n\n") 

    fichier.write("Number of solutions in conflicts: ")
    fichier.write(str(len(output1[1])))
    fichier.write("\n") 

    fichier.write("Number of solutions in no conflicts: ")
    fichier.write(str(len(dico)))
    fichier.write("\n") 

    fichier.write("Number of solutions in total: ")
    totalnode = len(output1[1]) + len(dico)
    fichier.write(str(totalnode))
    fichier.write("\n") 

    fichier.close()     
