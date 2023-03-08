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
k = 0
end = False

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
                #print(id_3)

    elif id_3[-2:] == '.0':
        id_3 = int(id_3[:-2])

    id_4 = list_line[7]
    id_4 = int(float(id_4))

    id_5 = list_line[9]
    id_5 = int(float(id_5))
    find = False
    
    if end:
        break

    #if j ==0:
    #    print(f"{id_1} {id_2} {id_3} {id_4} {id_5}")
    

    file_csv.seek(0)
    lines_csv = csv.reader(file_csv, delimiter=",")

    #k = 0
    list_possibilities = []
    #list_test = []
    ban_list = []

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

            if id_1 == id_a and id_2 == id_b and id_3 == id_c and id_4 == id_d and id_5 == id_e:
                str_weight = list_line_csv[12].split(" ")
                weight = float(str_weight[2][:-3])
                list_possibilities.append(weight)
                #list_test.append([weight,[id_1,id_2,id_3,id_4,id_5]])
                #sum += weight
                i += 1
                find = True     

                #k += 1
                    
    #if k > 1:
    #    print(f"{id_1} {id_2} {id_3} {id_4} {id_5}")

    if find:
        sum += min(list_possibilities)
        if str(id_1)+str(id_2)+str(id_3)+str(id_4)+str(id_5) not in ban_list:
            for w in list_possibilities:
                sum += w

        if min(list_possibilities) < 10000:
            sum_noInf += min(list_possibilities)
            j+=1
        


        #if max(list_possibilities) > 10000:
            #print(list_test)
            #print(f'{id_1} and {id_2} and {id_3} and {id_4} and {id_5}')
        k +=1

    else:
        print(f'{id_1} and {id_2} and {id_3} and {id_4} and {id_5}')
        end = True

    #j+=1

print(f'i = {i}')
print(f'j = {j}')
print(f'j = {k}')
print(f'sum = {sum}')
print(f'sum = {sum_noInf}')

file_db.close()
file_csv.close()

#i = 2519
#sum = 660.5564099999989


#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.23296)
#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.37535)

# [9.223372036854776e+18, ['Q5024', 'P54', 'Q2739', 200101, 200201]
# [9.223372036854776e+18, ['Q1939', 'P54', 'Q1344163', 200501, 200608]
# [9.223372036854776e+18, ['Q1925', 'P54', 'Q1450557', 201501, 201601]
# [9.223372036854776e+18, ['Q10869', 'P54', 'Q5794', 201201, 201301] => ligne output 915, 1233, 1421, 2119
# [9.223372036854776e+18, ['Q5117', 'P54', 'Q319699', 200201, 200201]