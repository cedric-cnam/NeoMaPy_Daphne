import csv

#data = ".\..\..\..\Neo4J\wikidata\data\\rockit_wikidata_0_5k.csv"
data_input = "rockit_wikidata_0_5k.csv"
file_input = open(data_input,"r")

data_output = "rockit_wikidata_0_5k-10.csv"
file_output = open(data_output,'w')

lines = csv.reader(file_input, delimiter=",")

for line in lines:
    if len(line) > 3 :
        str_weight = line[6][:-1]
        float_weight = float(str_weight)%10.0
        weight = round(float_weight/10,5)

        str_line = str(line[:-1])
        str_line = str_line.replace("[","")
        str_line = str_line.replace("]","")
        str_line = str_line.replace("'","")
        file_output.write(str_line)
        file_output.write(", ")
        file_output.write(str(weight))
        file_output.write(')\n')

    else:
        str_line = str(line)
        str_line = str_line.replace("[","")
        str_line = str_line.replace("]","")
        str_line = str_line.replace("'","")
        file_output.write(str_line)
        file_output.write('\n')

file_input.close()
file_output.close()
