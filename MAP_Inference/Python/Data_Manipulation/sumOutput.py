import csv

#data = ".\..\..\..\Neo4J\wikidata\data\\rockit_wikidata_0_5k.csv"
data_csv = "rockit_wikidata_0_5k-10.csv"
file_csv = open(data_csv,"r")

data_db = "output_0_5k-10.db"
file_db = open(data_db,'r')

sum = 0
i = 0

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
                print(id_3)

    elif id_3[-2:] == '.0':
        id_3 = int(id_3[:-2])

    id_4 = list_line[7]
    id_4 = int(float(id_4))

    id_5 = list_line[9]
    id_5 = int(float(id_5))
    find = False
    
    if end:
        break

    file_csv.seek(0)
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

            if id_1 == id_a and id_2 == id_b and id_3 == id_c and id_4 == id_d and id_5 == id_e:
                str_weight = list_line_csv[12].split(" ")
                weight = float(str_weight[2][:-3])
                sum += weight
                i += 1
                find = True     

    if not find:
        print(f'{id_1} and {id_2} and {id_3} and {id_4} and {id_5}')
        end = True

print(f'i = {i}')
print(f'sum = {sum}')

file_db.close()
file_csv.close()

#i = 2519
#sum = 660.5564099999989