# -*- coding: utf-8 -*-
"""
Created on 17/08/2022
Last update 18/08/2022

@author: Victor
"""

import json


# Give your initial json file containing the conflicting nodes
data = 'conflictNodes.json'
with open(data, 'r') as f:
    liste = json.load(f)

##############################################################################################################
##############################################################################################################

# Creation of the dictionnary of conflincting nodes where (key,value) is ('id' : [weight, listOfConflicts])
dico={}
for i in liste:
    id = i["Node_id"]
    w = i["weight"]
    conf = i["Conflicts_node_ids"]
    dico[id] = (w,conf)


##############################################################################################################
##############################################################################################################

# Creation of the json file of this dictionnary    
fichier = open("dicoConfNodes.json", "w")
fichier.write("{\n")

size = len(dico)
i = 1

for (k,v) in dico.items():
    fichier.write("\t\"")
    fichier.write(str(k))
    fichier.write("\": [")
    fichier.write(str(v[0]))
    fichier.write(", ")
    fichier.write(str(v[1]))
    if i != size:    
        fichier.write("],\n")
    else:
        fichier.write("]\n")
    i += 1

fichier.write("}")
fichier.close()