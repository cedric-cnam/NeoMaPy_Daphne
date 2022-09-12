# -*- coding: utf-8 -*-
"""
Created on 17/08/2022
Last update 18/08/2022

@author: Victor
"""

import time
import json

start = time.time()
# Give your initial json file containing the conflicting nodes
data = 'dicotIncInitClear_0_50k.json'
with open(data, 'r') as f:
    dico = json.load(f)


##############################################################################################################

# Creation of the json file of this dictionnary    
file1 = open("dicotIncNoConfClear_0_50k.json", "w")
file1.write("{\n")

file2 = open("dicotIncConfClear_0_50k.json", "w")
file2.write("{\n")

i = 0
j = 0

for (k,v) in dico.items():
    if v[1] == []:
        if i != 0:    
            file1.write("],\n ")
        file1.write("\t\"")
        file1.write(str(k))
        file1.write("\": [")
        file1.write(str(dico[str(k)][0]))
        file1.write(", ")
        file1.write(str(v[1]))
        i += 1
    else:
        if j != 0:    
            file2.write("],\n ")
        file2.write("\t\"")
        file2.write(str(k))
        file2.write("\": [")
        file2.write(str(dico[str(k)][0]))
        file2.write(", ")
        file2.write(str(v[1]))
        j += 1

file1.write("]\n")
file1.write("}")
file1.close()

file2.write("]\n")
file2.write("}")
file2.close()

end = time.time()
elapsed = end - start
print(f'Temps d\'exécution : {elapsed:.5}s')