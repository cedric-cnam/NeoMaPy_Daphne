import csv

#data = ".\..\..\..\Neo4J\wikidata\data\\rockit_wikidata_0_5k.csv"
data_csv = "pinstConf_rockit_wikidata_0_5k.csv"
#".\..\..\Data_Json\\nRocKit\\rockit_wikidata_0_5k-10.csv"
file_csv = open(data_csv,"r")

new_file = open("wikidata_0_5k.csv","w")

i = 0
set_o = set()

lines_csv = csv.reader(file_csv, delimiter=";")

for list_line in lines_csv:
    if i > 0:
        pinst = list_line[0]
        s = list_line[2]
        p = list_line[4]
        o = list_line[3]
        date_start = list_line[5]
        ds_liste = str(date_start).split("-")
        ds = ds_liste[0]+ds_liste[1]
        date_end = list_line[6]
        de_liste = str(date_end).split("-")
        de = de_liste[0]+de_liste[1]
        valid = list_line[9] # or 7
        weight = str(list_line[8])

        set_o.add(str(o))
        """
        weight = round(float(list_line[8])*10,4)
        if weight == 8.0:
            weight = 9223372036854776000.0000
        weight = str(weight)
        """

        #if pinst == "pinstConf":
        new_file.write("pinstConf(\"")
        new_file.write(s)
        new_file.write("\",\"")
        new_file.write(p)
        new_file.write("\",\"")
        new_file.write(o)
        new_file.write("\",\"")
        new_file.write(str(ds))
        new_file.write("\",\"")
        new_file.write(str(de))
        new_file.write("\",\"")
        new_file.write(valid)
        new_file.write("\",")
        new_file.write(weight)
        new_file.write(")\n")
    

    #file_csv.seek(0)
    #lines_csv = csv.reader(file_csv, delimiter=",")

    #for line_csv in lines_csv:
    i += 1

for o in set_o:
    new_file.write("sameAs(\"")
    new_file.write(o)
    new_file.write("\",\"")
    new_file.write(o)
    new_file.write("\")\n")

new_file.close()
file_csv.close()

#i = 2519
#sum = 660.5564099999989


#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.23296)
#pinstConf("Q24012",  "P54",  "Q1886",  "201301",  "201301",  "true", 0.37535)