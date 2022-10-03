import json

#data = ".\..\..\..\Neo4J\wikidata\data\\rockit_wikidata_0_5k.csv"
data_db = "output_0_5k_avecC0.db"
#".\..\..\Data_Json\\nRocKit\\rockit_wikidata_0_5k-10.csv"

file_db = open(data_db,"r")

i = 0

list_sol = []

for line_db in file_db:
    list_line = line_db.split("\"")
    s = str(list_line[1])
    o = str(list_line[5])
    p = str(list_line[3])
    date_start = list_line[7]
    date_start = int(float(date_start))
    date_start = str(date_start)
    ds = date_start[0:4]+ "-" +date_start[4:6]+ "-01"
    ds = str(ds)
    date_end = list_line[9]
    date_start = int(float(date_end))
    date_start = str(date_end)
    de = date_end[0:4]+ "-"+date_end[4:6]+ "-01"
    de = str(de)
    #weight = str(list_line[13])
    #weight = str(weight[:-1])

    #id_3 = list_line[5]
    if o[-2:] == 'E7':
        o = int(o[:-2].replace(".",""))
        if o > 0:
            while o < 10000000:
                o = o*10
                #print(id_3)

    elif o[-2:] == '.0':
        o = int(o[:-2])

    o = str(o)

    id = s + "-" + o + "-" + p + "-" + ds + "-" + de 
    list_sol.append(id)
    
    #file_solution.write(id)
    #file_solution.write("\n")


file_json = "mapping_Neo4j_wikidata_0_5k_nrockit.json"
#file_json = open(data_json,"r")
file_solution = open("n-rockit_solution_0_5k_avecC0.json","w")

with open(file_json, 'r') as f:
    l_dico = json.load(f)

set_sol = set()

for sol in list_sol:
    for dico in l_dico:
        if sol in dico["wikiID"]:
            set_sol.add(dico["Node_id"])

sum = 0
file_solution.write("[")
i = 1
for sol in set_sol:
    file_solution.write(str(sol))
    if i < len(set_sol):
        file_solution.write(",\n")
    else:
        file_solution.write("\n")
    for dico in l_dico:
        if sol == dico["Node_id"]:
            sum += dico["weight"]
    i += 1

file_solution.write("]")           

print(f'sum = {sum}')

file_db.close()
#file_json.close()
file_solution.close()


#i = 2519
#sum = 660.5564099999989


#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.23296)
#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.37535)