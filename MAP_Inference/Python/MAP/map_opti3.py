# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 24/08/2022

@author: Victor
"""

from ast import Continue
import json
from re import S
import time
import copy
#from itertools import chain, combinations
import multiprocessing


##############################################################################################################
##############################################################################################################
###################################### LOAD the data  OPTI 1 #################################################

#with open('.\..\..\Data_Json\Dictionnary\ClearDico\dico-2.5kNoConf.json', 'r') as f:
with open('.\..\..\Data_Json\Dictionnary\dicotIncNoConf_100_50k.json', 'r') as f:
    dico = json.load(f)

with open('.\..\..\Data_Json\Dictionnary\ClearDico\dicotIncNoConfClear_50_5k.json', 'r') as f2:
    dico2 = json.load(f2)

##############################################################################################################
##############################################################################################################
######################################  OPTIMISATION 1 - Algorithme 3 ######################################## 

"""
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
"""

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
	return liste
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
    #return liste

"""
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
def build_sol(dico): #,index):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    threshold = int(nb_nodes*0.67)
    threshold2 = int(nb_nodes*0.35)
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
        if i%3  == 0:    
            deletInclude(liste_sol)    

        if i > threshold2 and i%3==0:
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

    return liste_sol


#print(build_sol(dico))


# Build the solutions
def build_sol_approx(dico):#,index):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    threshold = int(nb_nodes*0.67)
    step = int(nb_nodes*0.2)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]
    #max_len = 1.0
    #set_sol = set(frozenset([int(l_dico[0][0])]))
    
    tmp_comp = 0
    tmp_inc = 0
    taille_inc_a = 0
    taille_inc_b = 0
    i_taille = 0
    
    for i in range(1,len(l_dico)):
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste
        """
        if index == 8 :#and i == len(l_dico)-1:
            print(f'etape {i} / node = {int(l_dico[i][0])} {len(l_dico)} avec l_sol = ')
            printSol(liste_sol)
            print('\n')
        """
        while j < len(liste_sol)-h:
            """
            if len(liste_sol[j][0]) < float(max_len/10) :
                Stop = False
                for l in liste_sol:
                    if liste_sol[j][0] < l[0]:# or l2[0]>l[0]:
                        Stop = True
                        del liste_sol[j]
                        break
                if Stop:
                    continue
            """
            #if index < 1:
            #    start = time.time()
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)

            #if index < 1:
            #    end = time.time()
            #    elapsed = end - start
            #    tmp_comp += elapsed
            
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] += l_dico[i][1][0]
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]
                    """  
                if max_len < len(liste_sol[j][0]):
                    max_len = len(liste_sol[j][0])
                    """

                if i > threshold:
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        del liste_sol[j]
                        j -= 1    
                
            else:
                #include = False
                for l in liste_sol:
                    include = False
                    if l2[0] <= l[0]: #or l2[0]>l[0]:
                        include = True
                        break

                    #if l2[0]>l[0]:
                        #include = True
                        
                if not(include):
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
                        """
                    if max_len < len(l2[0]):
                        max_len = len(l2[0])
                        """
            j += 1
        """
        if index < 1:
                start = time.time()
                taille_inc_b += len(liste_sol)
                i_taille += 1  
        """       
        if i%2  == 0:    
            #liste_sol = 
            deletInclude(liste_sol)  
        """  
        if index < 1:
                end = time.time()
                elapsed = end - start
                taille_inc_a += len(liste_sol)
                tmp_inc += elapsed 

        l_test = [threshold, threshold + step, threshold + 2*step, threshold + 3*step]
        if i in l_test:
            for y in range(0,len(l_dico)):
                for l in liste_sol:
                    if int(l_dico[y][0]) not in l[1]:
                        l[0].add(int(l_dico[y][0]))
                        l[1] |= set(l_dico[y][1][1])
                        l[2] += l_dico[y][1][0]
                    if maxi < l[2]:
                        maxi = l[2]
        
        if index == 8 and i == len(l_dico)-1:
            print(f'Approx etape {i} / {len(l_dico)} avec l_sol = ')
            printSol(liste_sol)
            print('\n')
        
    
    if index == 0:
        print(f'temps de comp à indice {index} = {tmp_comp}')
        print(f'temps de inc à indice {index} = {tmp_inc}')
        print(f'taille moyenne de list_sol before dans inc à indice {index} = {taille_inc_b/i_taille}')
        print(f'taille moyenne de list_sol after dans inc à indice {index} = {taille_inc_a/i_taille}')
    
        if index == 84:
        for s in set_sol:
            print(s)
        print('\n')
        print(liste_sol)
    
        print(f'solution na index 8')
        printSol(liste_sol)
        val,liste = max_sum_list_int(dico,liste_sol)
        print(f'best score ={val} et sol')
        print(liste)
    """
    return liste_sol


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
#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5kClear.json', 'r') as f: 	
#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5k.json', 'r') as f: 	
with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_10_5k.json', 'r') as f: 	
    l_dico = json.load(f)


#################################### Apply Opti 1 on the list of dico ########################################
def solutionForList(l_dico):
    set_init = set()
    output = [0, set_init]
    i = 0
    #distrib = [0,0,0,0,0,0,0,0,0,0]
    #sum = 0
    #size = len(l_dico["list"])
    #print(size)
    #record = []
    for dico in l_dico["list"]:
        #if i == 0:
        #index = int(len(dico)/50)
        #distrib[index] += 1
            #print(f'{i} / {size} with length = {len(dico)}')# et distrib = {distrib} ')
            #max = 0
            #avg = 0
            #for k,v in dico.items():
                #avg += len(v[1])
                #if  len(v[1]) > max:
                    #max = len(v[1])
            #record.append((max,avg/len(dico)))
        #sum += len(dico)
        #if i == 0:
        #    start = time.time()
        val,liste = max_sum_list_int(dico,build_sol(dico,i))
        #if i == 0:
        #    end = time.time()
        #    elapsed = end - start
        #    print(f'Temps d\'exécution {i} : {elapsed:.5}s')

        output[0] += val
        output[1] |= set(liste)
        #output[1] += liste
        i+=1
    #print(f'nb total nodes conf = {sum}')
    #print(f'record = {record}')
    return output


def solutionForListapprox(l_dico):
    set_init = set()
    output = [0, set_init]
    i = 0
    #size = len(l_dico["list"])
    for dico in l_dico["list"]:
        #if i == 0:
        #    print(f'{i} / {size} with length = {len(dico)}')
        #if i == 0:
        #    start = time.time()
        val,liste = max_sum_list_int(dico,build_sol_approx(dico))#,i))
        #if i == 0:
        #    end = time.time()
        #    elapsed = end - start
        #    print(f'Temps d\'exécution {i} : {elapsed:.5}s')
        output[0] += val
        output[1] |= set(liste)
        #i+=1
    return output

"""
start = time.time()
output1 = solutionForList(l_dico)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution conf : {elapsed:.5}s')

print(output1[0])
"""

#print(output1[1])

"""
start = time.time()
output1a = solutionForListapprox(l_dico)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution conf approx : {elapsed:.5}s')

print(output1a[0])
"""

#print(f'nb nodes clear conf : {len(dico2)}')
#output12 = sum_weight(dico2,dico2)
#print(output12)

#print(f'nb nodes no conf : {len(dico)}')

#output2 = sum_weight(dico,dico)
#print(output2)

#print(f'Score total na = {output1[0] + output2}')
#print(f'Score total a = {output1a[0] + output2}')
#print(f'Score total = {output1[0] + output12 + output2}')


"""
set_na = set(output1[1])

set_a = set(output1a[1])

print(f'long a = {len(set_na)}')
print(f'long na = {len(set_a)}')


print(set_a - set_na) 
# = {2785, 2765, 2767, 2770, 2738, 2779}
print('\n')
print(set_na - set_a)
"""

# = {2786, 7363, 7309, 2766, 5136, 2768, 5139, 2771, 2775, 4664, 2780}
""" 
{6085, 6086, 6088, 6090, 6091, 6094, 6095, 6097, 6098, 6100, 6102, 6103, 6106, 6108, 6109, 6113, 6115, 6116, 6121, 6123, 6124, 6130, 6132}

    {2784, 2786, 7363, 2788, 2789, 2790, 2791, 2764, 2766, 2768, 2769, 2771, 2773, 2775, 2778, 2780, 2782, 2783}
      ok    ok    ok    ok    ok    ok    ok    no    ok    no    ok    no    no    no     ok    ok   ok    ok
      ok    no    ok    ok    ok    ok    ok    ok    ok    no    ok    no    ok    no     ok    ok   ok    ok
                  ok                            ok          ok          ok                       ok   
#long na = 1452
#long approx = 1447

"""

############################################ Parallelization #################################################


def task(dico):
	val,liste = max_sum_list_int(dico,build_sol(dico))
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


if __name__ == '__main__':
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_50_50kClear.json', 'r') as f: 
    with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_100_50k.json', 'r') as f: 		
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5k.json', 'r') as f: 
        l_dico = json.load(f)

    start = time.time()
    output1 = parallelization(l_dico)
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution conf : {elapsed:.5}s\n')
    print(output1[0])

    #start = time.time()
    #output2 = sum_weight(dico,dico)
    #print(output2)
    #end = time.time()
    #elapsed2 = end - start
    #print(f'Temps d\'exécution no conf : {elapsed2:.5}s')

    #print(f'Temps d\'exécution total : {elapsed1+elapsed2:.5}s')
    #print(f'Score total = {output1[0]+output2}')
    #print(f'Score total = {output1[0]}')

    #output12 = sum_weight(dico2,dico2)
    #print(output12)

    output2 = sum_weight(dico,dico)
    print(output2)

    #print(f'Score total = {output1[0] + output12 + output2}')
    print(f'Score total = {output1[0] + output2}')
