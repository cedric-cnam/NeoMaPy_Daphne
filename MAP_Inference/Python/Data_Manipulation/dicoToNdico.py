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

start = time.time()
data_conf = '.\..\..\Data_Json\Dictionnary\dicotIncConf_0_5k.json'
#data_conf = '.\..\..\Data_Json\Dictionnary\ClearDico\dicotIncConfClear_0_50k.json'
with open(data_conf, 'r') as f:     
    dic = json.load(f)


def oneDico(key, dico, l_id, d_out):
    for n in dico[str(key)][1]:
        if n not in l_id:
            l_id += [int(n)]
            d_out[str(n)]= dico[str(n)]
            l_id,d_out = oneDico(str(n), dico, l_id, d_out)
    return l_id,d_out


def decrease(dico):
    l_deso = list(dico.items())
    l_croi = [l_deso[0]]
    for i in range(1,len(l_deso)):
        add = False
        for j in range (0,len(l_croi)):
            if len(l_deso[i][1][1]) >= len(l_croi[j][1][1]):
                l_croi.insert(j,l_deso[i])
                add = True
                break
        if add == False:
            l_croi.insert(j+1,l_deso[i])
    dico_output = {}
    for elem in l_croi:
        dico_output[elem[0]] = elem[1]
    return dico_output


def Ndico(dico):
    l_id_total = set()
    d_total = []    
    for k in dico:
        if int(k) not in l_id_total:
            d_out = {}
            d_out[str(k)] = dico[str(k)]
            l_id, d_out = oneDico(k, dico, [int(k)], d_out)
            #d_total.append(decrease(d_out))
            d_total.append(d_out)
            l_id_total.update(set(l_id))
    return d_total


##############################################################################################################
##############################################################################################################
############################################## Write the data ################################################

# Creation of the json file of this dictionnary    
fichier = open("listOfDicotInc_0_5k.json", "w")
fichier.write("{\n")
fichier.write("\t \"list\": [\n")
ListeOfDicos = Ndico(dic)
i = 1
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

end = time.time()
elapsed = end - start
print(f'Temps d\'exécution : {elapsed:.5}s')