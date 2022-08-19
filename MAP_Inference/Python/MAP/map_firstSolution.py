# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 18/08/2022

@author: Victor
"""

import json
import time

# Load the data

#with open('dicoConfNodes.json', 'r') as f:
with open('.\..\..\Data_Json\Dictionnary\smallDico.json', 'r') as f:
    dico = json.load(f)

##############################################################################################################
##############################################################################################################


# Algo naive : first solution
# output = (sum, list_of_nodes, list_of_conflicts)

start = time.time()

output = [0,[],[]]
for elem in dico.items():
    (k,v) = elem
    if (int(k) not in output[2]) and (int(k) not in v[1]) and (not((set(output[1]) & set(v[1])))):
        output[0] += v[0]
        output[1].append(int(k))
        output[2] += v[1]
        list(set(output[2]))

print((output[0],output[1]))


end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.9}ms')