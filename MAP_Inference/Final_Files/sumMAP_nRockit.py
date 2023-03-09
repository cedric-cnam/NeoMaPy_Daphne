import csv

#data = ".\..\..\..\Neo4J\wikidata\data\\rockit_wikidata_0_5k.csv"
data_csv = ".\..\..\..\\NeoMaPy_Daphne_Data\\wikidata-nrockit\\input_data\\rockit_wikidata_10_5k.csv"
file_csv = open(data_csv,"r")

# C:\Users\Victor\Documents\GitHub\NeoMaPy_Daphne\MAP_Inference\Data_Manipulation
# C:\Users\Victor\Documents\GitHub\NeoMaPy_Daphne_Data\wikidata-nrockit\input data

data_db = ".\..\..\..\\NeoMaPy_Daphne_Data\MAP_nRockit\output_10_5k.db"
file_db = open(data_db,'r')

sum = 0
sum_noInf = 0
i = 0
j = 0
dico_weight = {}
lines_csv = csv.reader(file_csv, delimiter=",")
for line_csv in lines_csv:
    if len(line_csv) > 3 :
        list_line_csv = str(line_csv).split("\"")
        id_a = list_line_csv[1]
        id_b = list_line_csv[3]
        id_c = list_line_csv[5]
        if id_c[0] != 'Q':
            id_c = int(id_c)

        id_d = list_line_csv[7]
        id_d = int(id_d)
        id_e = list_line_csv[9]
        id_e = int(id_e)

        str_weight = list_line_csv[12].split(" ")
        weight = float(str_weight[2][:-3])

        if str(id_a)+str(id_b)+str(id_c)+str(id_d)+str(id_e) not in dico_weight:
            dico_weight[str(id_a)+str(id_b)+str(id_c)+str(id_d)+str(id_e)] = [weight]
        else:
            dico_weight[str(id_a)+str(id_b)+str(id_c)+str(id_d)+str(id_e)].append(weight)


for line_db in file_db:
    
    list_line = line_db.split("\"")
    id_1 = list_line[1]
    id_2 = list_line[3]

    id_3 = list_line[5]
    if id_3[-2:] == 'E7':
        id_3 = int(id_3[:-2].replace(".",""))
        if id_3 > 0:
            while id_3 < 10000000:
                id_3 = id_3*10

    elif id_3[-2:] == '.0':
        id_3 = int(id_3[:-2])

    id_4 = list_line[7]
    id_4 = int(float(id_4))

    id_5 = list_line[9]
    id_5 = int(float(id_5))
    
    id = str(id_1)+str(id_2)+str(id_3)+str(id_4)+str(id_5)
    maxi = max(dico_weight[id])
    dico_weight[id].remove(maxi)
    #dico_weight[id].append(0)
    sum += maxi
    i+=1
    if maxi < 10000:
        sum_noInf += maxi
        j+=1

print(f'nb total node = {i}')
print(f'nb not infinite node = {j}')

print(f'sum = {sum}')
print(f'sum_noInf = {sum_noInf}')

file_db.close()
file_csv.close()


#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.23296)
#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.37535)

# [9.223372036854776e+18, ['Q5024', 'P54', 'Q2739', 200101, 200201]
# [9.223372036854776e+18, ['Q1939', 'P54', 'Q1344163', 200501, 200608]
# [9.223372036854776e+18, ['Q1925', 'P54', 'Q1450557', 201501, 201601]
# [9.223372036854776e+18, ['Q10869', 'P54', 'Q5794', 201201, 201301] => ligne output 915, 1233, 1421, 2119
# [9.223372036854776e+18, ['Q5117', 'P54', 'Q319699', 200201, 200201]