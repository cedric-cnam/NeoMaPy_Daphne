# -*- coding: utf-8 -*-
"""
Created on 24/08/2022
Last update 24/08/2022

@author: Victor
"""

import random

# Creation of the json file of this dictionnary    
fichier = open("dicoTest100.json", "w")
fichier.write("{\n")

size = 100

j = 0

for i in range(0,size+1):
    fichier.write("\t\"")
    fichier.write(str(i))
    fichier.write("\": [")
    fichier.write(str(round(random.random(),5)))
    fichier.write(", [")
    for k in range((j*10),(j+1)*10):
        if j == 0 :
            if k != i:
                fichier.write(str(k))
                fichier.write(", ")
        else:            
            if k == j*10 and i == (j*10)+1:
                fichier.write(str(k))
                if i != size or k+1 != size-1: 
                    fichier.write(", ")

            if k != i:
                if k == (j*10)+1:
                    fichier.write(str(k))
                    if i != size or k+1 != size: 
                        fichier.write(", ")
                elif k != (j*10) :
                    fichier.write(str(k))
                    if i != size or k+1 != size: 
                        fichier.write(", ")
            
    if (j+1)*10 != i:
        fichier.write(str((j+1)*10))
    elif i != size:
        fichier.write(str(((j+1)*10)+1))

    j = int(i/10) 
    fichier.write("]")
    if i != size:    
        fichier.write("],\n")
    else:
        fichier.write("]\n")
    i += 1

fichier.write("}")
fichier.close()