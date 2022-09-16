# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 16/09/2022

@author: Victor
"""

from ast import Continue
import json
from re import S
import time
import multiprocessing


##############################################################################################################
##############################################################################################################
###################################### LOAD the data  OPTI 1 #################################################

with open('.\..\..\Data_Json\Dictionnary\dicotIncNoConf_100_50k.json', 'r') as f:
    dico = json.load(f)

#with open('.\..\..\Data_Json\Dictionnary\ClearDico\dicotIncNoConfClear_50_5k.json', 'r') as f2:
#    dico2 = json.load(f2)

##############################################################################################################
##############################################################################################################
##############################################  Algorithmes ################################################## 

def printSol(l_sol):
	for l in l_sol:
		print(f'{l[0]}')


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
def build_sol(dico): #,index):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    #nb_conf_max = len(l_dico[0][1][1])
    #if nb_conf_max > 200:
    #    modulo = 2
    #else:
    #    modulo = 3
    modulo = 3
    #modulo2 = 3
    threshold = int(nb_nodes*0.67)
    #threshold = int(nb_nodes*0.7)
    #threshold2 = int(nb_nodes*0.35)
    #threshold2 = int(nb_nodes*0.45)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]

    set_nodes = set()
    for l in l_dico:
        set_nodes.add(int(l[0]))

    for i in range(1,len(l_dico)):
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste
        while j < len(liste_sol)-h:
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] += l_dico[i][1][0]
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]   
                if i > threshold:
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        set_id = set()
                        for l in liste_sol:
                            if l != liste_sol[j]:
                                set_id |= l[0]
                        set_diff = liste_sol[j][0] - set_id
                        if len(set_diff) == 0:
                            del liste_sol[j]
                            j -= 1 
                        else:
                            liste_sol[j][0] = set_diff
                            liste_sol[j][1] = set()
                            liste_sol[j][2] = 0
                            for n in liste_sol[j][0]:
                                liste_sol[j][1] |= set(dico[str(n)][1])
                                liste_sol[j][2] += dico[str(n)][0]        
            else:
                include = False
                for l in liste_sol:
                    #include = False
                    if l2[0] <= l[0]: #or l2[0]>l[0]:
                        include = True
                        break
                if not(include):
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
            j += 1
        if i%modulo  == 0:    
            deletInclude(liste_sol)    
        """
        if i > threshold2 and i%modulo2==0:
            x = 0
            while x < len(liste_sol):
                diff = set_nodes - liste_sol[x][1]
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
        """
    return liste_sol


##############################################################################################################
##############################################################################################################
###################################  OPTIMISATION 2 - Algorithme 3+ ########################################## 


##################################### LOAD the data for OPTI 2 ###############################################

#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_0_50k.json', 'r') as f: 	
#    l_dico = json.load(f)


#################################### Apply Opti 1 on the list of dico ########################################
def solutionForList(l_dico):
    set_init = set()
    output = [0, set_init]
    for dico in l_dico["list"]:
        val,liste = max_sum_list_int(dico,build_sol(dico))
        output[0] += val
        output[1] |= set(liste)
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
print(output2)
print(f'Score total = {output1[0] + output2}')
#print(f'Score total = {output1[0] + output12 + output2}')
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

    start = time.time()
    output2 = sum_weight(dico,dico)
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution no conf : {elapsed:.5}s\n')
    print(output2)

    #print(f'Score total = {output1[0] + output12 + output2}')
    print(f'Score total = {output1[0] + output2}')
