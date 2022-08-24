# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 22/08/2022

@author: Victor
"""

import json
import time

import map_firstSolution as mf
import map_brutForce as mb
import map_opti2 as mo

if __name__ == '__main__':

##############################################################################################################
##############################################################################################################
####################################### LOAD the data and RESULTS ############################################

# --------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------      ###   Algo 1 vs Algo 2 vs Algo 3 vs Algo 3+ : Temps || Score   ###      ----------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------


    with open('.\..\..\Data_Json\Dictionnary\dicoConfNodes.json', 'r') as f:    # 0.4s  vs ?   ?    vs 11.8s	    || 406.1858 vs    ?     vs 603.8150
    #with open('.\..\..\Data_Json\Dictionnary\\1kDico.json', 'r') as f:		    # 0.05s vs ?   ?    vs 0.3s	        || 158.421 	vs    ?     vs 175.1238
    #with open('.\..\..\Data_Json\Dictionnary\\100Dico.json', 'r') as f:        # 0.0s  vs ?   ?    vs 0s			|| 18.077 	vs    ?     vs 20.0265
    #with open('.\..\..\Data_Json\Dictionnary\\80Dico.json', 'r') as f:		    # 0s    vs ?   ?	vs 0s	        || 14.814 	vs    ?     vs 15.6493
    #with open('.\..\..\Data_Json\Dictionnary\\60Dico.json', 'r') as f:		    # 0s    vs ? vs 1093s(18m) vs 0s	|| 10.36327 vs    ?     vs 10.9541
    #with open('.\..\..\Data_Json\Dictionnary\\55Dico.json', 'r') as f:		    # 0s    vs ? 		vs 41.2s	    || 9.79568  vs    ?     vs 10.2861
    #with open('.\..\..\Data_Json\Dictionnary\\50Dico.json', 'r') as f:		    # 0s    vs ? 		vs 3.8s	        || 9.08248  vs    ?     vs 9.43362
    #with open('.\..\..\Data_Json\Dictionnary\\12Dico.json', 'r') as f:		    # 0s    vs 466s(8m)	vs 0s	        || 2.31822  vs 2.34025  vs 2.34025
    #with open('.\..\..\Data_Json\Dictionnary\\11Dico.json', 'r') as f:		    # 0s    vs 36s		vs 0s   	    || 2.08734  vs 2.10937  vs 2.10937 
    #with open('.\..\..\Data_Json\Dictionnary\\10Dico.json', 'r') as f:		    # 0s    vs 13s 		vs 0s   	    || 0.86158  vs 1.31749  vs 1.31748
        dico = json.load(f)



##############################################################################################################
##############################################################################################################
###################################### First Solution - Algorithme 1 #########################################

# Algo naive : first solution
# output = (sum, list_of_nodes, list_of_conflicts)
    start = time.time()
    output = mf.solution(dico)
    print("Algo 1 - First solution:")
    print(output[0])
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution : {elapsed:.5}s\n')



##############################################################################################################
##############################################################################################################
#########################################  Brut Force - Algorithme 2 #########################################

    #start = time.time()
    #print("Algo 2 - Brut Force:")
    #print(mb.max_sum_list(dico,mb.list_max_sol(dico)))
    #end = time.time()
    #elapsed = end - start
    #print(f'Temps d\'exécution : {elapsed:.5}s\n')



##############################################################################################################
##############################################################################################################
########################################  OPTIMISATION - Algorithme 3 ######################################## 


############################################### OPTI 1 #######################################################

    #print("Algo 3 - Opti 1:")
    #start = time.time()
    #print(mo.max_sum_list_int(dico,mo.build_sol(dico)))
    #end = time.time()
    #elapsed = end - start
    #print(f'Temps d\'exécution : {elapsed:.5}s')    

############################################## OPTI 1 + 2 ####################################################

########################################## LOAD the data for OPTI 2 ##########################################

    with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico.json', 'r') as f: 	
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico1k.json', 'r') as f: 	
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico100.json', 'r') as f:
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico80.json', 'r') as f:
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico60.json', 'r') as f: 
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico55.json', 'r') as f: 
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico50.json', 'r') as f: 
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico12.json', 'r') as f: 
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico11.json', 'r') as f: 	
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico10.json', 'r') as f: 					 	
        l_dico = json.load(f)


    print("Algo 3 - Opti 1+2:")
    start = time.time()
    output = mo.solutionForList(l_dico)
    end = time.time()
    elapsed = end - start
    print(output[0])
    print(f'Temps d\'exécution : {elapsed:.5}s\n')

############################################ OPTI 1 + 2 + 3 ###################################################

    print("Algo 3 - Opti 1+2+3:")
    #start = time.time()
    output,elapsed = mo.parallelization(l_dico)
    #end = time.time()
    #elapsed = end - start
    print(output[0])
    print(f'Temps d\'exécution : {elapsed:.5}s')
