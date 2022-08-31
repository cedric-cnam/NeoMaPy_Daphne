# -*- coding: utf-8 -*-
"""
Created on 20/08/2022
Last update 28/08/2022

@author: Victor
"""

import json
import time


##############################################################################################################
##############################################################################################################
############################################## LOAD the data #################################################


with open('.\..\..\Data_Json\Dictionnary\\1kDico.json', 'r') as f: 
    dico = json.load(f)


# Creation of the json file of this dictionnary  
fichier = open("dico-1kClean.json", "w")
fichier.write("{\n")

size = len(dico)
i = 1

#for (k,v) in dico.items():
for k,v in dico.items():
    fichier.write("\t\"")
    fichier.write(str(k))
    fichier.write("\": [")
    fichier.write(str(dico[str(k)][0]))
    fichier.write(", [")
    #fichier.write(str(v))
    j = 0
    #print(f'v= {v}')
    for elem in v[1]:
        #print(f' elem = {elem}')
        if str(elem) in dico:
            if j == 0:
                fichier.write(str(elem))
                j += 1
            else:
                fichier.write(", ")
                fichier.write(str(elem))
                j += 1
    fichier.write("]")
    
    if i != size:    
        fichier.write("],\n")
    else:
        fichier.write("]\n")
    i += 1

fichier.write("}")
fichier.close()