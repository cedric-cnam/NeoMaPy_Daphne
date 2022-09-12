# -*- coding: utf-8 -*-
"""
Created on 17/08/2022
Last update 18/08/2022

@author: Victor
"""

import time
import json


# Give your initial json file containing the conflicting nodes
#data = 'dicoTest100.json'
#data = '.\..\..\Data_Json\Dictionnary\\1kDico.json'
data = '.\..\..\Data_Json\Dictionnary\dicotIncConf_50_50k.json'
with open(data, 'r') as f:
    dico = json.load(f)


##############################################################################################################


def group(dico):
    list_ban = set()
    list_dico = list(dico.items())
    i = 0
    while i < len(list_dico):
        j = i+1
        set_i = set(list_dico[i][1][1])
        while j < len(list_dico): 
            if int(list_dico[i][0]) in list_dico[j][1][1]:
                set1 = set_i - {int(list_dico[j][0])}
                set2 = set(list_dico[j][1][1]) - {int(list_dico[i][0])} 
                if set1 >= set2 and list_dico[i][1][0] < list_dico[j][1][0]:
                    list_ban |= {int(list_dico[i][0])}
                    del list_dico[i]
                    i -= 1
                    break 
                elif set1 <= set2 and list_dico[i][1][0] > list_dico[j][1][0]:
                    list_ban |= {int(list_dico[j][0])}
                    del list_dico[j]
                    j -= 1                
            j += 1
        i += 1   
    return list_ban   

# selectione chaque nodes qui n'est pas banni
def select(dico):
    list_ban = group(dico)
    output = []
    i = 0
    for k,v in dico.items():
        if int(k) not in list_ban:
            output.append([int(k),[]])
            for n in v[1]:
                if n not in list_ban:
                    output[i][1].append(n)
            i +=1
    return output        



##############################################################################################################


start = time.time()
# Creation of the clean dictionnary 
output = select(dico)


# Creation of the json file of this dictionnary    
fichier = open("dicotIncInitClear_50_50k.json", "w")
fichier.write("{\n")
size = len(output)
i = 1
for k,v in output:
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

end = time.time()
elapsed = end - start
print(f'Temps d\'exécution: {elapsed:.5}s')