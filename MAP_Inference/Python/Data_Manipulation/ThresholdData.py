# -*- coding: utf-8 -*-
"""
Created on 07/09/2022
Last update 07/09/2022

@author: Victor
"""

import time
import json


# Give your initial json file containing the conflicting nodes
#data = 'dicoTest100.json'
#data = '.\..\..\Data_Json\Dictionnary\\1kDico.json'
data = '.\..\..\Data_Json\Dictionnary\dicoConfNodes.json'
with open(data, 'r') as f:
    dico = json.load(f)


##############################################################################################################



# Creation of the json file of this dictionnary    
fichier = open("dico-2.5kThreshold.json", "w")
fichier.write("{\n")

threshold = 0.2
size = len(dico)
i = 1

#for (k,v) in dico.items():
for k,v in dico:
    if v[0] > threshold:
        fichier.write("\t\"")
        fichier.write(str(k))
        fichier.write("\": [")
        fichier.write(str(dico[str(k)][0]))
        fichier.write(", ")
        fichier.write(str(v))
        if i != size:    
            fichier.write("],\n")
        else:
            fichier.write("]\n")
    i += 1

fichier.write("}")
fichier.close()
