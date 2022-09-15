# -*- coding: utf-8 -*-
"""
Created on 17/08/2022
Last update 10/09/2022

@author: Victor
"""

import json


# Give your initial json file containing the conflicting nodes
data_conf = '.\..\..\Data_Json\Initial_Data\\tInc_conflicts_100_50k.json'
with open(data_conf, 'r') as f:
    liste_conf = json.load(f)


# Give your initial json file containing the non conflicting nodes
data_noconf = '.\..\..\Data_Json\Initial_Data\\tInc_noConflicts_0_10k.json'
with open(data_noconf, 'r') as f2:
    liste_noconf = json.load(f2)


##############################################################################################################
##############################################################################################################


# Creation of the dictionnary of conflincting nodes where (key,value) is ('id' : [weight, listOfConflicts])
dico_conf = {}
for i in liste_conf:
    id = i["Node_id"]
    w = i["weight"]
    conf = i["Conflicts_node_ids"]
    dico_conf[id] = (w,conf)


# Creation of the dictionnary of non conflincting nodes where (key,value) is ('id' : [weight, []])
dico_noconf = {}
for i in liste_noconf:
    id = i["Node_id"]
    w = i["weight"]
    conf = []
    dico_noconf[id] = (w,conf)


##############################################################################################################
##############################################################################################################


# Creation of the json file of this dictionnary of conflicting nodes 
fichier_conf = open("dicotIncConf_100_50k.json", "w")
fichier_conf.write("{\n")
size = len(dico_conf)
i = 1
for (k,v) in dico_conf.items():
    fichier_conf.write("\t\"")
    fichier_conf.write(str(k))
    fichier_conf.write("\": [")
    fichier_conf.write(str(v[0]))
    fichier_conf.write(", ")
    fichier_conf.write(str(v[1]))
    if i != size:    
        fichier_conf.write("],\n")
    else:
        fichier_conf.write("]\n")
    i += 1
fichier_conf.write("}")
fichier_conf.close()


# Creation of the json file of this dictionnary of non conflicting nodes 
fichier_noconf = open("dicotIncNoConf_0_10k.json", "w")
fichier_noconf.write("{\n")
size = len(dico_noconf)
i = 1
for (k,v) in dico_noconf.items():
    fichier_noconf.write("\t\"")
    fichier_noconf.write(str(k))
    fichier_noconf.write("\": [")
    fichier_noconf.write(str(v[0]))
    fichier_noconf.write(", ")
    fichier_noconf.write(str(v[1]))
    if i != size:    
        fichier_noconf.write("],\n")
    else:
        fichier_noconf.write("]\n")
    i += 1
fichier_noconf.write("}")
fichier_noconf.close()