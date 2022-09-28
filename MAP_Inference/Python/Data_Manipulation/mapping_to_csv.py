import json

file_json = "mapping_Neo4j_wikidata_0_5k_true.json"
#file_json = open(data_json,"r")
#file_solution = open("n-rockit_solution_0_4642_tinc.json","w")

with open(file_json, 'r') as f:
    l_dico = json.load(f)

new_file = open("wikidata_0_5k_true2.csv","w")

set_so = set()
set_s = set()
set_o = set()

for dico in l_dico:
    id = dico["wikiID"]
    l_id = id.split("-")
    s = l_id[0]
    p = l_id[2]
    o = l_id[1]
    d_s = l_id[3]+l_id[4]
    d_e = l_id[6]+l_id[7]
    w = l_id[9]
    #print(w)
    #print(w[-3:])
    #print("\n")
    if w[-3:] == "E18":
        w = "9223372"
    string = "pinstConf(\"" + s + "\",\"" + p + "\",\"" + o + "\",\"" + d_s + "\",\"" + d_e + "\",\"true\"," + w + ")\n" 
    new_file.write(string)
    
    
    set_o.add(o)
    set_s.add(s)

#print(len(set_o))
#print(len(set_s))

set_so = set_s.union(set_o)
#print(len(set_so))

for so in set_so:
    new_file.write("sameAs(\"")
    new_file.write(so)
    new_file.write("\",\"")
    new_file.write(so)
    new_file.write("\")\n")

new_file.close()

#i = 2519
#sum = 660.5564099999989


#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.23296)
#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.37535)