# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 24/08/2022

@author: Victor
"""

import json
from re import S
import time
import multiprocessing


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


#with open('.\..\..\Data_Json\Dictionnary\ClearDico\dico-1kNoConf.json', 'r') as f:
with open('.\..\..\Data_Json\Dictionnary\ClearDico\dico-2.5kNoConf.json', 'r') as f:
    dico = json.load(f)


##############################################################################################################
##############################################################################################################
######################################  OPTIMISATION 1 - Algorithme 3 ######################################## 

def printSol(l_sol):
	for l in l_sol:
		print(f'{l}\n')



###############################################################################################

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
	return liste


###############################################################################################

"""
def sum_weight(dico,solution):
    sum = 0
    for id in solution:
        sum += dico[str(id)][0]
    return sum
"""

def max_sum(l_sol):
    l_sum = []
    for sol in l_sol:
        #l_sum.append(sum_weight(dico,sol[0]))
        l_sum.append(sol[2])
    return (max(l_sum), l_sol[l_sum.index(max(l_sum))][0])


#liste = [[id_nodes],[conflicts]]
def compatible_merge(node,liste,dico):
    l_merge_comp = [{node}, set(dico[str(node)][1]), dico[str(node)][0]]
    compatible = True
    for n in liste[0]:
        if node in dico[str(n)][1]:
            compatible = False
        else:
            l_merge_comp[0].add(n)
            l_merge_comp[1] |= set(dico[str(n)][1])
            l_merge_comp[2] += dico[str(n)][0]
    return (l_merge_comp,compatible)

# Build the solutions
def build_sol_sum(dico):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    threshold = int(nb_nodes*0.6)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]

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
                elif i > threshold:
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        del liste_sol[j]
                        j -= 1    
            else:
                exist = False
                for l in liste_sol:
                    if l[0] == l2[0]:
                        exist = True
                        break 
                if not exist:
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
            j += 1
        liste_sol = deletInclude(liste_sol)
    return liste_sol



###############################################################################################

###############################################################################################

"""
def sum_weight_alpha(dico,solution,alpha):
    sum = 0
    for id in solution:
        sum += dico[str(id)][0]**alpha
    sum = sum**(1/alpha)
    return sum
"""

def max_sum_alpha(l_sol,alpha):
	l_sum = []
	for sol in l_sol:
		l_sum.append(sol[2])#**(1/alpha))
	return (max(l_sum), l_sol[l_sum.index(max(l_sum))][0])

#liste = [[id_nodes],[conflicts]]
def compatible_merge_alpha(node,liste,dico,alpha):
    l_merge_comp = [{node}, set(dico[str(node)][1]), dico[str(node)][0]**alpha]
    compatible = True
    for n in liste[0]:
        if node in dico[str(n)][1]:
            compatible = False
        else:
            l_merge_comp[0].add(n)
            l_merge_comp[1] |= set(dico[str(n)][1])
            l_merge_comp[2] += dico[str(n)][0]**alpha
    return (l_merge_comp,compatible)

# Build the solutions
def build_sol_sum_alpha(dico,alpha):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    threshold = int(nb_nodes*0.6)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]**alpha

    for i in range(1,len(l_dico)):
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste
        while j < len(liste_sol)-h:
            (l2,bool) = compatible_merge_alpha(int(l_dico[i][0]),liste_sol[j],dico,alpha)
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] += l_dico[i][1][0]**alpha
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]
                elif i > threshold:
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]**alpha  
                    if potential_max < maxi:
                        del liste_sol[j]
                        j -= 1    
            else:
                exist = False
                for l in liste_sol:
                    if l[0] == l2[0]:
                        exist = True
                        break 
                if not exist:
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
            j += 1
        liste_sol = deletInclude(liste_sol)
    return liste_sol



#############################################################################################

"""
def sum_weight_pond(dico,solution):
    i = 1
    sum = dico[str(solution[0])][0]
    while i < len(solution):
        sum = (sum + dico[str(solution[i])][0]) - (sum*dico[str(solution[i])][0])
        i += 1
    return sum
"""

def max_sum_pond(l_sol):
    l_sum = []
    for sol in l_sol:
        l_sum.append(sol[2])
    return (max(l_sum), l_sol[l_sum.index(max(l_sum))][0])


#liste = [[id_nodes],[conflicts]]
def compatible_merge_pond(node,liste,dico):
    l_merge_comp = [{node}, set(dico[str(node)][1]), dico[str(node)][0]]
    compatible = True
    for n in liste[0]:
        if node in dico[str(n)][1]:
            compatible = False
        else:
            l_merge_comp[0].add(n)
            l_merge_comp[1] |= set(dico[str(n)][1])
            l_merge_comp[2] = (l_merge_comp[2] + dico[str(n)][0]) - (l_merge_comp[2] * dico[str(n)][0])
    return (l_merge_comp,compatible)

# Build the solutions
def build_sol_sum_pond(dico):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    threshold = int(nb_nodes*0.6)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]

    for i in range(1,len(l_dico)):
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste
        while j < len(liste_sol)-h:
            (l2,bool) = compatible_merge_pond(int(l_dico[i][0]),liste_sol[j],dico)
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] = (liste_sol[j][2] + l_dico[i][1][0]) - (liste_sol[j][2] * l_dico[i][1][0])
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]
                elif i > threshold:
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max = (potential_max + l_dico[k][1][0]) - (potential_max * l_dico[k][1][0])
                    if potential_max < maxi:
                        del liste_sol[j]
                        j -= 1    
            else:
                exist = False
                for l in liste_sol:
                    if l[0] == l2[0]:
                        exist = True
                        break 
                if not exist:
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
            j += 1
        liste_sol = deletInclude(liste_sol)
    return liste_sol








#print(build_sol(dico))


"""
start = time.time()
res = build_sol(d_1)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution inc : {elapsed:.5}s')
print("\n")
printSol(res)
print(len(res))
h = []
for elem in res:
    h.append(elem[2])
print(max(h))

print(max_sum_list_int(d_1,res))
"""



##############################################################################################################
##############################################################################################################
###################################  OPTIMISATION 2 - Algorithme 3+ ########################################## 


##################################### LOAD the data for OPTI 2 ###############################################
#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico1kClear.json', 'r') as f: 	
#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5kClear.json', 'r') as f: 	
with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5k.json', 'r') as f: 	
    l_dico = json.load(f)


#################################### Apply Opti 1 on the list of dico ########################################
def solution_sum(l_dico):
	output = [0,[]]
	#i = 0
	#size = len(l_dico["list"])
	for dico in l_dico["list"]:
		#print(f'{i} / {size} with length = {len(dico)}')
		val,liste = max_sum(build_sol_sum(dico))
		output[0] += val
		output[1] += liste
		#i+=1
	return output



def solution_sum_alpha(l_dico,alpha):
    output = [0,[]]
    #i = 0
    #size = len(l_dico["list"])
    for dico in l_dico["list"]:
    #print(f'{i} / {size} with length = {len(dico)}')
        val,liste = max_sum_alpha(build_sol_sum(dico),alpha)
        output[0] += val
        output[1] += liste
    #i+=1
    output[0] = output[0]**(1/alpha)
    return output



def solution_sum_pond(l_dico):
	output = [0,[]]
	#i = 0
	#size = len(l_dico["list"])
	for dico in l_dico["list"]:
		#print(f'{i} / {size} with length = {len(dico)}')
		val,liste = max_sum_pond(build_sol_sum_pond(dico))
		output[0] += val
		output[1] += liste
		#i+=1
	return output

"""   
avg_time_1 = 0 
for i in range(0,10):
    start = time.time()
    output1 = solutionForList(l_dico)
    end = time.time()
    elapsed1 = end - start
    avg_time_1 += elapsed1
    #print(output1[0])
    #print(output1[1])
    print(f'Temps d\'exécution conf : {elapsed1:.5}s')
 
    start = time.time()
    output2 = sum_weight(dico,dico)
    #print(output2)
    end = time.time()
    elapsed2 = end - start
    print(f'Temps d\'exécution no conf : {elapsed2:.5}s')
    #print(output1[0]+output2)
    #print(output1[1])
    print(f'Temps d\'exécution total : {elapsed1 + elapsed2:.5}s\n')
    avg_time_1 += elapsed1 + elapsed2

print(f'temps moyen = {avg_time_1/10}\n')
"""

start = time.time()
output_sum = solution_sum(l_dico)
end = time.time()
elapsed = end - start

print(f'Score sum = {output_sum[0]}')
#print(output1[1])
print(f'Temps d\'exécution sum : {elapsed:.5}s')


alpha = 3
start = time.time()
output_sum_alpha = solution_sum_alpha(l_dico,alpha)
end = time.time()
elapsed = end - start

print(f'Score sum alpha = {output_sum_alpha[0]}')
#print(output1[1])
print(f'Temps d\'exécution sum alpha: {elapsed:.5}s')



start = time.time()
output_sum_pond = solution_sum_pond(l_dico)
end = time.time()
elapsed = end - start

print(f'Score sum pond = {output_sum_pond[0]}')
#print(output1[1])
print(f'Temps d\'exécution sum pond: {elapsed:.5}s')

#output2 = sum_weight(dico,dico)
#print(output2)

#print(f'Score total = {output1[0]}')
#print(f'Score total = {output1[0]+output2}')
#print(output1[1])

set_10 = set(output_sum[1]) - set(output_sum_alpha[1])
set_11 = set(output_sum[1]) - set(output_sum_pond[1])

set_20 = set(output_sum_alpha[1]) - set(output_sum[1])
set_21 = set(output_sum_alpha[1]) - set(output_sum_pond[1])

set_30 = set(output_sum_pond[1]) - set(output_sum[1])
set_31 = set(output_sum_pond[1]) - set(output_sum_alpha[1])

print(f'Set sum - sum_alpha = {set_10}')
print(f'Set sum - sum_pond = {set_11}')

print(f'Set sum_alpha - sum = {set_20}')
print(f'Set sum_alpha - sum_pond = {set_21}')

print(f'Set sum_pond - sum = {set_30}')
print(f'Set sum_pond - sum_alpha = {set_31}')

"""
set_noConf = set()
for id in dico:
    set_noConf.update({int(id)})
print(len(set_noConf))
#611

set_conf = set(output1[1])
print(len(set_conf))
#996

set_total = set_conf.union(set_noConf)
print(len(set_total))
#1607
"""

############################################ Parallelization #################################################


def task(dico):
	val,liste = max_sum(build_sol_sum(dico))
	return val,liste


def parallelization(l_dico):
	output = [0,[]]
	#start = time.time()
	pool = multiprocessing.Pool(2)
	result = pool.imap(task, l_dico["list"])
	for val,liste in result:
		output[0] += val
		output[1] += liste
	#end = time.time()
	#elapsed = end - start
	#print(f'Temps d\'exécution : {elapsed:.5}s')
	return output#,elapsed

"""
if __name__ == '__main__':
    with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5kClear.json', 'r') as f: 	
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5k.json', 'r') as f: 
        l_dico = json.load(f)

    start = time.time()
    output1 = parallelization(l_dico)
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution conf : {elapsed:.5}s\n')
    #print(output[0])

    #start = time.time()
    #output2 = sum_weight(dico,dico)
    #print(output2)
    #end = time.time()
    #elapsed2 = end - start
    #print(f'Temps d\'exécution no conf : {elapsed2:.5}s')

    #print(f'Temps d\'exécution total : {elapsed1+elapsed2:.5}s')
    #print(f'Score total = {output1[0]+output2}')
    print(f'Score total = {output1[0]}')
"""
