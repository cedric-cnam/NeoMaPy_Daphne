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
with open('.\..\..\Data_Json\Dictionnary\dicoConfNodes.json', 'r') as f: 	
#with open('.\..\..\Data_Json\Dictionnary\ClearDico\dico-1kClean.json', 'r') as f: 
#with open('.\..\..\Data_Json\Dictionnary\ClearDico\dico-1kConf.json', 'r') as f: 
#with open('.\..\..\Data_Json\Dictionnary\ClearDico\dico-2.5kConf.json', 'r') as f: 
#with open('.\dico-2.5kConf.json', 'r') as f:     
    dic = json.load(f)

def oneDico(key, dico, l_id, d_out):
    for n in dico[str(key)][1]:
        if n not in l_id:
            l_id += [int(n)]
            d_out[str(n)]= dico[str(n)]
            l_id,d_out = oneDico(str(n), dico, l_id, d_out)
    return l_id,d_out

"""
test_d = {
    "1": [0.17849, [2,3]],
    "2": [0.19241, [1,3]],
    "3": [0.25549, [1,2,6]],
    "4": [0.19522999, [5]],
    "5": [0.19223, [4]],
    "6": [0.14644, [3]]
    }
"""
"""
def increase(dico):
    l_deso = list(dico.items())
    l_croi = [l_deso[0]]
    for i in range(1,len(l_deso)):
        add = False
        for j in range (0,len(l_croi)):
            if len(l_deso[i][1][1]) <= len(l_croi[j][1][1]):
                l_croi.insert(j,l_deso[i])
                add = True
                break
        if add == False:
            l_croi.insert(j+1,l_deso[i])
    dico_output = {}
    for elem in l_croi:
        dico_output[elem[0]] = elem[1]
    return dico_output
"""

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

#l_id,d_out = oneDico(1, test_d, [1], {"1":[0.17849, [2,3]]})
#print(f'l_id = {l_id}\n')
#print(f'd_out = {d_out}\n')

def Ndico(dico):
    l_id_total = set()
    d_total = []    
    for k in dico:
        if int(k) not in l_id_total:
            d_out = {}
            d_out[str(k)] = dico[str(k)]
            l_id, d_out = oneDico(k, dico, [int(k)], d_out)
            d_total.append(decrease(d_out))
            l_id_total.update(set(l_id))

    return d_total

#print(Ndico(test_d))




"""
for k,v in dico.items():
    buildNewDico = True
    for dico in ListeOfDicos:
        for key,value in dico.items():
            if int(k) in value[1] or (set(v[1]) & set(value[1])):
            #set(v[1]).intersection(set(value[1])) != set():
                dico[k] = v 
                buildNewDico = False
                break
        if buildNewDico == False:
            break
    if buildNewDico:
        ListeOfDicos.append({k:v})         


list_size = []
for dico in ListeOfDicos:
    list_size.append(len(dico))
print(f'list = {list_size}')

"""

##############################################################################################################
##############################################################################################################


# Creation of the json file of this dictionnary    
fichier = open("listOfDico2.5k.json", "w")

ListeOfDicos = Ndico(dic)

i = 1

fichier.write("{\n")
fichier.write("\t \"list\": [\n")
for dico in ListeOfDicos:
    fichier.write("\t\t")
    #print(dico)
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