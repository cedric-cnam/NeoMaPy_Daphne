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
data = '.\..\..\Data_Json\Dictionnary\\1kDico.json'
#data = '.\..\..\Data_Json\Dictionnary\dicoConfNodes.json'
with open(data, 'r') as f:
    dico = json.load(f)


##############################################################################################################

    # k = list_dico[i][0]
    # v = list_dico[i][1]
    # weight = list_dico[i][1][0]
    # conflicts = list_dico[i][1][1]

# grouper l'ensemble des noeuds qui sont en conflit et tel qu'ils possèdent exactement les mêmes autres conflits
def group(dico):
    list_dico = list(dico.items())
    list_choice = [[int(list_dico[0][0])]]
    for i in range(1,len(list_dico)):
        new = True
        for j in range(0,len(list_choice)):  
            set1 = set(dico[str(list_choice[j][0])][1]) - set(dico[str(list_dico[i][0])][1])
            set2 = set(dico[str(list_dico[i][0])][1]) - set(dico[str(list_choice[j][0])][1])
            if  {int(list_dico[i][0])}.union({int(list_choice[j][0])}) == set1.union(set2):
                list_choice[j].append(int(list_dico[i][0]))
                new = False    
            #if set(dico[str(list_choice[j][0])][1]) - set(dico[str(list_dico[i][0])][1]) == {int(list_dico[i][0])} and \
             #   set(dico[str(list_dico[i][0])][1]) - set(dico[str(list_choice[j][0])][1]) == {int(list_choice[j][0])}:
              #  list_choice[j].append(int(list_dico[i][0]))
               # new = False
        if new:
            list_choice.append([int(list_dico[i][0])])
    return list_choice

#print(group(dico))

# selectionne pour chaque group conflictuelle le meilleur score
def select(list_group,dico):
    output = []
    for liste in list_group:
        maxi_w = 0
        maxi_id = -1
        for id in liste:
            if dico[str(id)][0] >= maxi_w:
                maxi_w = dico[str(id)][0]
                maxi_id = id
        output.append(maxi_id)
    return output


#start = time.time()
#output = select(group(dico),dico)
#print(output)
#end = time.time()
#elapsed = end - start
#print(f'Temps d\'exécution : {elapsed:.5}s')

# version 1 est 2fois plus rapide environ


##############################################################################################################

# si un noeud a ses conflits inclu dans un autre noeud et que ce noeud inclue a un score superieure  
# alors inscrire le "gros" noeud avec un plus petit score dans une liste des noeuds à supprimer

def group2(dico):
    list_ban = set()
    list_dico = list(dico.items())
    for i in range(0,len(list_dico)):
        for j in range(0,len(list_dico)): 
            if int(list_dico[i][0]) in list_ban:
                break
            else:
                if int(list_dico[i][0]) in list_dico[j][1][1]:
                    set1 = set(list_dico[i][1][1]) - {int(list_dico[j][0])}
                    set2 = set(list_dico[j][1][1]) - {int(list_dico[i][0])} 
                    #if(set1 == set2 and list_dico[i][1][0] < list_dico[j][1][0]) or \
                    #    (set1 > set2 and list_dico[i][1][0] < list_dico[j][1][0]):
                    if set1 >= set2 and list_dico[i][1][0] < list_dico[j][1][0]:
                        list_ban.update({int(list_dico[i][0])})
            """
            if int(list_dico[j][0]) not in list_ban:
                if int(list_dico[j][0]) in list_dico[i][1][1]:
                    set1 = set(list_dico[i][1][1]) - {int(list_dico[j][0])}
                    set2 = set(list_dico[j][1][1]) - {int(list_dico[i][0])} 
                    if(set1 == set2 and list_dico[i][1][0] < list_dico[j][1][0]):# or \
                        #(set1 > set2 and list_dico[i][1][0] < list_dico[j][1][0]):
                        list_ban.update({int(list_dico[i][0])})
            """        
    return list_ban



# selectione chaque nodes qui n'est pas banni
def select2(dico):
    list_ban = group2(dico)
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


#start = time.time()
output = select2(dico)
#print(output)
#end = time.time()
#elapsed = end - start
#print(f'Temps d\'exécution : {elapsed:.5}s')




##############################################################################################################

# Creation of the json file of this dictionnary    
fichier = open("dico-1kinit.json", "w")
fichier.write("{\n")

size = len(output)
i = 1

#for (k,v) in dico.items():
for k,v in output:
    #if int(k) in output:
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
