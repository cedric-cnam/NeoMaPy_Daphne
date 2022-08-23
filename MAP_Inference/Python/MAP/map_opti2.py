# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 19/08/2022

@author: Victor
"""

import json
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
with open('.\..\..\Data_Json\Dictionnary\\55Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\50Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\12Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\11Dico.json', 'r') as f:		
#with open('.\..\..\Data_Json\Dictionnary\\10Dico.json', 'r') as f:		
    dico = json.load(f)


##############################################################################################################
##############################################################################################################
######################################  OPTIMISATION 1 - Algorithme 3 ######################################## 

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
			if set(liste[i][0]) < set(liste[j][0]):
				del liste[i]
				continue
			elif set(liste[j][0]) < set(liste[i][0]):
				del liste[j]	
				continue
			j += 1
		i += 1
	return liste

#liste = [[id_nodes],[conflicts]]
def compatible_merge(node,liste,dico):
	l_merge_comp = [[node],set(dico[str(node)][1])]
	compatible = True
	for n in liste[0]:
		if node in dico[str(n)][1]:
			compatible = False
		else:
			l_merge_comp[0].append(n)
			l_merge_comp[1] |= set(dico[str(n)][1])
	return (l_merge_comp,compatible)
		
# Build the solutions
def build_sol(dico):
	liste_sol = []
	l_dico = list(dico.items())
	liste_sol.append([[int(l_dico[0][0])],set(l_dico[0][1][1])])
	for i in range(1,len(l_dico)):
			for j in range(0,len(liste_sol)):
				(l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
				if bool:
					liste_sol[j][0].append(int(l_dico[i][0]))
					liste_sol[j][1] |= set(l_dico[0][1][1])
				else:
					liste_sol += [[l2[0],l2[1]]]
			liste_sol = deletInclude(liste_sol)
	return liste_sol


    #new = list(l_dico[0][1][1])
	#new = list(dico[k1][1])
	#for k, v in dico.items():
		#if i == 0: 
		#	new = list(v[1])
        #   #new = list(dico[k][1])
		#	liste_sol.append([[int(k)],new])
		#	i = 1
		#else:

#print(build_sol(dico))

#start = time.time()
#print(max_sum_list_int(dico,build_sol(dico)))
#end = time.time()
#elapsed = end - start
#print(f'Temps d\'exécution : {elapsed:.5}s')


##############################################################################################################
##############################################################################################################
###################################  OPTIMISATION 2 - Algorithme 3+ ########################################## 


##################################### LOAD the data for OPTI 2 ###############################################
#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico.json', 'r') as f: 	
    #l_dico = json.load(f)


#################################### Apply Opti 1 on the list of dico ########################################
def solutionForList(l_dico):
    output = [0,[]]
    for dico in l_dico["list"]:
        val,liste = max_sum_list_int(dico,build_sol(dico))
        output[0] += val
        output[1] += liste
    return output

"""
start = time.time()
output = solutionForList(l_dico)
end = time.time()
elapsed = end - start
print(output[0])
print(f'Temps d\'exécution : {elapsed:.5}s')
"""

############################################ Parallelization #################################################


def task(dico):
	val,liste = max_sum_list_int(dico,build_sol(dico))
	return val,liste


def parallelization(l_dico):
	output = [0,[]]
	start = time.time()
	pool = multiprocessing.Pool(2)
	result = pool.imap(task, l_dico["list"])
	for val,liste in result:
		output[0] += val
		output[1] += liste
	end = time.time()
	elapsed = end - start
	print(f'Temps d\'exécution : {elapsed:.5}s')
	return output,elapsed


#if __name__ == '__main__':
	#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico.json', 'r') as f: 	
		#l_dico = json.load(f)

	#start = time.time()
	#output,elaspe = parallelization(l_dico)
	#end = time.time()
	#elapsed = end - start
	#print(f'Temps d\'exécution : {elapsed:.5}s\n')
	#print(output[0])
