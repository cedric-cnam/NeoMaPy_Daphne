# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 22/08/2022

@author: Victor
"""

import json
import time


##############################################################################################################
##############################################################################################################
############################################# LOAD the data  #################################################

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



##############################################################################################################
##############################################################################################################
###################################### First Solution - Algorithme 1 #########################################

# Algo naive : first solution
# output = (sum, list_of_nodes, list_of_conflicts)

def solution(dico):
    output = [0,[],[]]
    for elem in dico.items():
        (k,v) = elem
        # set & set : check the intersection
        if (int(k) not in output[2]) and (not((set(output[1]) & set(v[1])))): 
            output[0] += v[0]
            output[1].append(int(k))
            output[2] += v[1]
            output[2] = list(set(output[2]))
    return output

#start = time.time()
#output = solution(dico)    
#print((output[0],output[1]))
#end = time.time()
#elapsed = end - start
#print(f'Temps d\'exécution : {elapsed:.5}s')