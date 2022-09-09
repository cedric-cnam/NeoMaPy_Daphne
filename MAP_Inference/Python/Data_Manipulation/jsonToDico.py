# -*- coding: utf-8 -*-
"""
Created on 17/08/2022
Last update 18/08/2022

@author: Victor
"""

import json


# Give your initial json file containing the conflicting nodes
#data = 'conflictNodes.json'
#data = '.\..\..\Data_Json\Initial_Data\\tInc_conflicts.json'
data = '.\..\..\Data_Json\Initial_Data\\tInc_noconflicts.json'
#data = 'withoutconflicts.json'
with open(data, 'r') as f:
    liste = json.load(f)

##############################################################################################################
##############################################################################################################

# Creation of the dictionnary of conflincting nodes where (key,value) is ('id' : [weight, listOfConflicts])
dico={}

for i in liste:
    id = i["Node_id"]
    w = i["weight"]
    #conf = i["Conflicts_node_ids"]
    conf = []
    dico[id] = (w,conf)

"""
for i in liste:
    id = i["Node_id"]
    w = i["weight"]
    if type(w) == list:
        sum = 0
        for w_i in w:
            sum += w_i
        w = sum
    if w == None :
        w = 0
    conf = []
    dico[id] = (w,conf)
"""

##############################################################################################################
##############################################################################################################

# Creation of the json file of this dictionnary    
fichier = open("dicotIncNoConf.json", "w")
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