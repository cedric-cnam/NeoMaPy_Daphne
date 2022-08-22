# -*- coding: utf-8 -*-
"""
Created on 20/08/2022
Last update 20/08/2022

@author: Victor
"""

import json
import time


##############################################################################################################
##############################################################################################################
############################################## LOAD the data #################################################

#with open('.\..\..\Data_Json\Dictionnary\dicoConfNodes.json', 'r') as f: 	
with open('.\..\..\Data_Json\Dictionnary\\1kDico.json', 'r') as f: 
    dico = json.load(f)

ListeOfDicos = []

for k,v in dico.items():
    buildNewDico = True
    for dico in ListeOfDicos:
        for key,value in dico.items():
            if int(k) in value[1] or (set(v[1]) & set(value[1])):
                dico[k] = v 
                buildNewDico = False
                break
    if buildNewDico:
        ListeOfDicos.append({k:v})         
        
"""
list_size = []
for dico in ListeOfDicos:
    list_size.append(len(dico))
print(f'list = {list_size}')
"""

##############################################################################################################
##############################################################################################################

# Creation of the json file of this dictionnary    
fichier = open("listOfDico1k.json", "w")

i = 1

fichier.write("{\n")
fichier.write("\t \"list\": [\n")
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