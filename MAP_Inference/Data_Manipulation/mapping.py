import json

#data = ".\..\..\..\Neo4J\wikidata\data\\rockit_wikidata_0_5k.csv"
data_db = ".\..\..\..\\NeoMaPy_Daphne_Data\MAP_nRockit\output_10_5k.db"

#C:\Users\Victor\Documents\GitHub\NeoMaPy_Daphne_Data\MAP_nRockit

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
    #print(f'start {date_start}')
    #date_start = date_start[:-2]
    #todo = 6 - len(date_start)
    #i = 0
    #print(f'avant {date_start}')
    while len(date_start)<6:
        date_start = "0" + date_start
        #i += 1
    
    #print(f'après {date_start}\n')
    ds = date_start[0:4]+ "-" +date_start[4:6]+ "-01"
    ds = str(ds)

    
    date_end = list_line[9]
    date_end = int(float(date_end))
    date_end = str(date_end)
    #date_end = date_end[:-2]
    #todo = 6 - len(date_end)
    #i = 0
    while len(date_end)<6:
        date_end = "0" + date_end
        #i += 1
    
    de = date_end[0:4]+ "-"+date_end[4:6]+ "-01"
    de = str(de)
    #weight = str(list_line[13])
    #weight = str(weight[:-1])
    
    #id_3 = list_line[5]

    minus = False
    if "-" in o:
        o = o.replace("-", "")
        minus = True

    if o[-2:] == 'E7':
        o = int(o[:-2].replace(".",""))
        if o > 0:
            while o < 10000000:
                o = o*10
                #print(id_3)
        o = str(o)

    elif o[-2:] == '.0':
        o = "0"+ o[:-2]

    if o[0] != "Q":
        while len(o) < 8:
            o = "0"+o

    if minus:
        o = "-" + o

    #print(ds)   
    #2010-01-01
    if ds[5:7] == "00":
        ds = ds[0:5] + "01" + ds[7:]

    if de[5:7] == "00":
        de = de[0:5] + "01" + de[7:]  

    """
    if "Q1528" in s and "11540101" in o and  "P570" in p:
        print("")
        print(ds)
        t1 = ds[:4]
        t2 = ds[5]
        t3 = ds[7:]
        t =t1 + t2 + "-01" + t3
        print(t1,t2,t3)
        print(de)
        print("")
    """
    
    
    if ds[2] == "-" and ds[4] == "-":
        t1 = ds[:2] + ds[3]
        t2 = ds[5]
        t3 = ds[7:]
        ds = t1 + t2 + "-01" + t3

    if de[2] == "-" and de[4] == "-":
        t1 = de[:2] + de[3]
        t2 = de[5]
        t3 = de[7:]
        de = t1 + t2 + "-01" + t3




    if ds[1] == "-" and ds[4] == "-":
        t1 = ds[0] + ds[2:4]
        t2 = ds[5]
        t3 = ds[7:]
        ds = t1 + t2 + "-01" + t3

    if de[1] == "-" and de[4] == "-":
        t1 = de[0] + de[2:4]
        t2 = de[5]
        t3 = de[7:]
        de = t1 + t2 + "-01" + t3    
    
    #115-40-01
    #1154-01-01

    if ds[0] == "-" and ds[4] == "-" and ds[7] == "-":
        t1 = ds[1:4] + ds[5]
        t2 = "-01"
        t3 = ds[7:]
        ds = t1 + t2 + t3

    if de[0] == "-" and de[4] == "-" and de[7] == "-":
        t1 = de[1:4] + de[5]
        t2 = "-01"
        t3 = de[7:]
        de = t1 + t2  + t3


    # 000--10-01
    if ds[3] == "-" and ds[4] == "-":
        ds = "0001-01-01"

    if de[3] == "-" and de[4] == "-":
        de = "0001-01-01"


    #if de[4] == "-":
    #    de = de[0:4] + de[5] + "01" + de[7:]

    id = s + "-" + o + "-" + p + "-" + ds + "-" + de 
    list_sol.append(id)
    
    #file_solution.write(id)
    #file_solution.write("\n")


file_json = "mapping_Neo4j_wikidata.json"
#file_json = open(data_json,"r")
file_solution = open("MAP_nRockit_10_5k.json","w")

with open(file_json, 'r') as f:
    l_dico = json.load(f)

set_sol = set()
for sol in list_sol:
    find = False
    for dico in l_dico:
        if sol in dico["wikiID"]:
            set_sol.add(dico["Node_id"])
            find = True
    if find == False:
        print(sol)

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

#print(set_sol)

set_MAPY = {'3700', '3009', '2474', '2481', '2701', '2502', '14574', '3023', '2858', '2766', '2819', '4086', '3701', '784', '2578', '913', '355', '727', '279', '959', '2784', '3285', '2300', 79, '384', '14619', 83, 85, 86, 87, '1088', 89, 90, 91, '876', 97, '900', '390', '2807', '281', 128, 134, 136, 137, 138, 140, 141, 142, '2450', '14501', 148, 151, '2318', '219', '2773', '14500', 169, 171, 188, 189, 190, 191, 192, 193, '887', '3587', '919', '2735', '342', '3961', '1066', '235', 213, '334', '2828', '366', 227, '1401', '1384', '863', 258, '2939', '4085', '1136', '2478', 274, '2316', '14662', 286, '2857', '14565', '736', '3028', '4143', 319, 320, 321, 322, 323, 324, 325, '3044', '3946', 336, '914', 340, '888', '4144', '796', '14581', '904', '201', '715', '4137', 365, '2747', '14653', 376, 377, 378, 379, 391, 392, '2859', '811', '3909', 401, 402, '649', '1259', '782', '886', 414, '2226', '3634', '2741', '1241', '2442', '230', '723', '263', '387', '1366', '1230', '4029', '3030', '14620', '1245', '280', '2297', '1105', 501, '1402', '4106', '2428', '3984', '815', '2782', '335', '3966', '14577', 531, 532, 533, 539, '856', 545, '989', '2881', 589, 591, '2563', '283', '3045', '885', '2479', '2813', '2473', '1243', '2840', '218', '14531', '2743', 642, '3300', '4089', '359', '4169', '2433', 667, '4159', 670, '3973', '413', 681, '778', 684, '2335', '14638', 691, '2485', 707, 708, '855', 716, '940', '2350', 734, 738, 744, '1381', 746, '206', '3965', '14641', '14632', '253', '3720', '266', '1049', 776, '2249', 786, '1084', '766', 793, 794, 800, '204', '244', '4136', '14650', '14541', '14595', '2501', '3633', '388', '1057', '2742', '2838', '3005', '1543', 847, 848, 849, 850, 851, 852, 853, '1112', '2475', 866, '2495', 869, '2684', 873, 874, '928', '4091', '1090', 891, '2847', 897, '946', '4146', '2829', '2330', 922, '2454', '932', '2323', '1460', '350', '3958', '925', '1129', '3680', '1100', '883', '2342', 977, 979, 980, 982, 985, 993, 996, 999, 1005, 1008, '879', 1018, '2293', '808', '288', 1027, 1028, 1029, 1030, '1120', '711', '3976', '3967', '1079', 1077, 1086, '14569', '2449', '2727', '1372', '1383', '2776', 1098, '2846', '14566', 1101, '4152', '3734', '14582', '327', 1116, '1002', 1123, 1124, '4002', 1134, '2832', '4079', '394', '930', '2729', '951', '3826', '14634', '3691', '4160', 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, '358', '931', '2887', 1233, 1234, '3962', '4013', '4047', 1252, 1253, 1254, '3518', '1080', '3298', '4174', '207', '225', '2810', '2602', '2443', '2338', '269', 1326, 1327, 1328, 1329, 1330, 1331, '936', 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, '2324', '2714', '1042', '3650', '819', '3585', '1854', '1396', '3662', 1414, '3696', '210', '3685', '2295', '3464', 1437, 1439, 1440, 1441, 1442, '246', 1458, 1459, 1462, 1463, '2294', '2744', '3679', '1065', '2817', '1092', '759', '3450', '3726', '361', 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1515, '1110', '4175', '338', '820', 1534, 1535, 1536, 1537, '918', 1549, '882', '3048', 1556, 1560, 1561, '3465', '3839', '385', 1570, 1571, '354', '1051', '799', 1574, 1575, '2934', '3672', '14594', '264', '3821', 1590, '3037', '14492', 1601, 1602, 1604, 1606, 1607, 1608, '1545', 1611, '1364', '2462', '810', 1665, '2405', '732', '2341', '3473', '2831', '3660', 1692, '2894', 1697, '2811', 1699, 1700, '4028', '2745', 1715, 1716, 1717, '2314', 1719, '14664', 1721, 1722, 1725, 1726, '1055', '2862', '2332', '941', '955', '251', '4042', '3011', '2852', '2438', 1794, '1368', 1796, '2451', 1799, 1800, 1801, 1802, 1804, 1806, '2488', '2489', 1814, 1817, '14564', '2437', '233', '197', '14484', 1845, 1846, 1848, 1849, 1850, 1852, 1855, 1860, '903', 1890, 1891, '2599', '3689', 1896, 1897, '289', 1906, '2818', '3698', '410', '2303', '3666', '2503', '14508', '4162', '823', 1939, 1940, 1941, 1942, 1945, 1946, 1947, 1948, '2036', '2812', '2885', 1970, '2498', 1973, 1974, '2444', 1976, 1977, 1981, 1983, '1370', '881', '2685', 1991, '2336', '252', '1108', 1999, 2000, 2001, 2002, '964', 2011, 2012, 2013, 2015, '915', 2019, '1119', 2034, '1389', '2830', '1398', '3823', '14515', '783', '3952', '2504', '3034', '771', '3688', 2080, '2753', 2082, 2083, 2084, 2085, 2086, 2087, 2088, 2089, 2090, '255', '346', 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2135, 2136, '14580', '1379', '3016', '2358', '239', 2181, '406', '795', '4165', 2196, 2205, 2206, '4090', '3018', '2732', '1391', 2217, 2218, 2219, 2220, '785', 2224, 2225, '2359', '2480', '14631', 2235, 2237, 2238, 2242, 2256, 2257, 2258, 2259, '1103', '14579', '2601', '1046', '15305', '4131', 2281, 2282, 2283, 2284, 2285, 2286, 2287, '3684', '3538', '2694', '349', '878', 2340, '3669', '1104', '1060', 2348, 2356, '748', '2808', 2363, 2364, 2365, '2861', '14537', '3675', '3730', 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, '1054', '2471', '3816', '14648', 2420, 2421, 2422, 2423, 2424, 2425, 2426, 2427, '2334', '2783', '3673', '386', '893', 2448, '2604', '854', '2823', '2875', '2755', '3648', '14642', '894', '2461', '1371', '2825', 2508, 2509, 2510, '647', '4096', '2756', 2520, 2521, 2522, 2523, 2524, 2531, '407', '248', '1089', 2558, 2559, 2560, 2561, 2562, 2565, 2566, '3943', '910', 2574, 2575, 2576, 2577, '14639', '14510', '1106', '2353', '3290', 2587, 2588, 2589, 2590, '2525', '2839', '2459', '2815', '2008', '4014', '2890', '2464', '962', '270', '226', '268', '4009', 2622, 2623, 2624, 2625, 2626, 2627, '14497', '2707', '751', '824', '4011', '3676', '4093', '3682', 2670, 2671, 2672, 2673, 2674, 2675, 2676, 2677, 2678, 2679, 2680, '4075', '1400', '2760', '929', '2820', '362', '14586', '1403', 2710, '967', '249', '405', '2469', '745', '196', '4111', '4010', '3294', '404', '2867', '862', '2845', 2788, '2844', '3638', 2801, 2802, 2803, 2804, 2805, '908', '14491', '14540', '1132', '265', '353', '2296', '4153', '14562', '937', 2884, '2719', 2895, 2912, '195', '3020', '3694', '3956', '3649', 2926, 2927, 2928, 2929, '2305', 2931, 2932, 2933, '3659', '3526', 2941, 2942, '3908', '237', '4000', '14507', '4080', '860', '902', '2453', 2978, 2979, 2980, 2981, 2982, 2983, 2984, 2985, '1138', '276', '1238', '3963', 3004, 3014, '14490', '2740', '2841', '3637', '260', '3957', 3041, 3042, '4001', '750', '2737', '3029', '4300', '960', 3087, 3088, 3089, '4074', 3092, 3093, '2455', '3025', '2936', 3113, '3653', 3118, '3667', 3121, 3122, 3123, '4081', '2754', '2877', '953', 3137, '764', '262', '2292', 3144, 3146, '2848', '2872', '3643', '2313', '14616', '3955', 3207, 3208, 3209, 3210, '2328', '3681', '3842', '650', '990', '1111', '3586', 3251, 3253, '198', 3261, 3262, 3263, 3264, 3265, 3267, '2873', 3270, '2326', '966', '284', '3723', 3280, '4076', '2716', 3287, '2153', '1062', '926', '2457', '409', '4164', 3312, 3313, 3314, 3315, '383', '1063', '1376', '14538', '4145', '1039', '14663', '14567', '3832', '14657', '3724', '858', '245', '332', '273', '4142', '14499', '818', 3420, '278', '1242', '14596', '2759', 3435, 3436, 3437, 3438, 3439, 3440, 3441, 3442, 3443, 3444, 3445, 3446, '3470', 3448, '4022', '4078', '14593', 3454, '948', 3456, '14652', '958', 3462, 3463, '998', 3466, 3475, 3476, '370', '3714', '921', '2748', 3484, 3485, '1388', 3487, 3488, '395', '2497', '2775', '3979', 3508, 3509, 3517, '3819', '4103', '14563', '14519', 3533, 3534, 3535, '3520', '242', '3733', '721', '2835', 3562, 3566, 3568, '3284', 3570, 3571, 3572, 3574, 3575, '3736', '1125', 3590, '3695', 3602, 3603, 3604, 3605, '3033', 3618, 3620, 3621, 3622, 3623, 3624, '223', 3626, 3627, '3644', '216', '329', '3844', '3647', '1378', '14601', '3824', '14656', '3719', '2595', '2579', '14588', '343', 3704, 3710, 3711, 3712, '825', 3727, '1045', '14504', '2600', '3661', '3959', 3758, '229', 3759, 3760, 3761, 3762, 3763, 3764, '209', '2317', '2152', '924', '4017', '14584', '2691', '947', '3006', '14518', 3803, 3804, 3805, 3806, 3807, 3808, 3809, 3810, 3811, 3812, 3813, 3814, '1382', '2346', '3024', 3818, '14590', '2470', '2826', '2833', 3836, '356', '2696', '3670', '3948', 3860, 3861, 3862, 3863, 3864, 3865, '261', '2886', '2291', '821', '807', '2430', '2441', 3894, 3895, '2699', '1043', 3912, 3913, '2298', '2693', '2734', 3926, 3927, 3928, 3929, 3930, 3931, '3725', '3999', '2868', 3950, '952', '822', '3291', '1067', '968', '14575', '2500', '2686', '1047', 3985, 3986, 3988, '2779', 3991, 3998, '1107', '2876', '934', 4005, 4006, '14599', '769', '3699', 4024, 4027, '282', 4032, 4033, 4036, 4037, 4038, 4045, 4046, '3471', 4048, '2248', 4052, 4053, '2290', '2683', '1404', '3663', '14512', '1240', '2781', 4066, 4067, 4068, '240', '243', '2329', 4072, 4084, '905', 4087, '3015', 4095, '772', 4099, '1390', 4102, '2468', 4112, '1126', 4124, 4125, 4126, '236', 4129, '813', '1056', 4132, 4134, '1131', '714', '2496', '1118', '3702', 4148, '2467', 4156, '774', 4158, '2596', '992', '389', '15307', '1113', 4177, '2938', '939', '3721', 4216, 4217, 4218, 4219, 4220, 4221, 4222, 4223, 4224, '2310', '3722', '3452', '4168', '1115', '3983', '411', '14587', '14600', '1853', 4289, 4290, 4291, 4292, 4293, 4294, 4295, 4296, 4297, 4298, '2711', '14570', 4303, '2758', '1082', '1059', 4318, 4319, 4320, 4321, 4322, 4323, '770', '949', '1387', '3522', 4328, 4329, 4330, '3524', 4353, 4354, 4355, 4356, 4357, 4358, 4359, 4360, '901', '814', '737', '14791', '14649', 4383, 4384, 4385, 4386, 4387, 4388, 4389, '4109', '779', '1099', '3652', '1399', '3019', '806', '330', '944', '2746', '2682', '742', '3527', '277', '781', '382', '3654', '1237', '2882', '3630', '3646', '1058', '2778', '205', '2343', '749', '1727', '1407', '988', '3472', '3525', '1247', '399', '1073', '4161', '4154', '2721', '1244', '2767', '14511', '3668', '920', '4149', '2854', '935',
             '3010', '403', '2325', '3732', '3838', '3677', '14571', '2816', '2351', '3449', '1068', '2769', '1135', '3295', '2345', '1609', '14630', '2891', '2764', '1114', '3843', '877', '3945', '965', '1081', '2834', '735', '1395', '950', '4050', '899', '241', '2436', '3283', '2580', '2768', '221', '797', '1258', '1365', '2606', '1038', '1374', '3021', '2889', '867', '1096', '2849', '1394', '4302', '762', '1069', '722', '3829', '726', '729', '14503', '200', '2824', '2689', '1053', '763', '3451', '648', '3971', '4023', '2307', '4008', '1121', '14532', '3012', '4141', '2301', '3970', '773', '2730', '2893', '859', '2354', '4097', '357', '4021', '4049', '4015', '199', '4012', '4108', '2456', '710', '3686', '809', '1248', '3645', '757', '3664', '367', '1075', '3674', '3687', '4107', '2715', '3735', '14493', '3046', '765', '755', '798', '3822', '328', '290', '3827', '956', '287', '326', '352', '4105', '1386', '3960', '3716', '3815', '2739', '4178', '363', '15115', '4043', '2863', '3940', '1061', '3296', '1074', '2720', '14502', '2751', '14498', '1239', '14517', '2736', '3528', '194', '2477', '3840', '2304', '397', '14516', '724', '2712', '3038', '2690', '333', '2772', '232', '2763', '3301', '3837', '4016', '254', '3942', '3299', '892', '14640', '2487', '2697', '2761', '725', '3951', '3022', '14668', '991', '4151', '1130', '2809', '247', '775', '2460', '3655', '217', '4088', '14659', '3975', '768', '651', '2888', '2837', '3713', '2289', '208', '812', '14536', '4110', '906', '14667', '3032', '1572', '2723', '895', '1246', '961', '2306', '14658', '2605', '2866', '351', '2007', '3974', '2836', '969', '3636', '3039', '909', '1527', '4163', '1231', '720', '2465', '2880', '3036', '2486', '14568', '3043', '3007', '2702', '215', '2434', '2337', '3297', '4077', '3293', '2774', '2771', '14660', '2445', '2681', '3692', '889', '2315', '2937', '728', '3718', '222', '1367', '945', '4030', '4170', '927', '1363', '2770', '14643', '1373', '211', '2822', '713', '756', '3641', 14486, '2492', '4019', '14654', '14629', 14494, 14495, '14625', '2728', 14513, '4104', '938', '2842', 14521, 14522, '2814', '942', 14525, '817', 14527, 14529, 14530, 14534, 14542, '14665', 14556, 14557, 14558, '718', '2864', '3665', 14572, 14573, '3656', '767', '802', '3008', '344', 14592, '1128', 14602, '408', 14613, 14614, 14615, '2757', 14618, '396', 14621, 14623, '3303', '2431', 14627, 14628, '3292', '3968', 14637, '2321', 14645, '2302', 14647, '758', '398', '3969', 14666, '780', '2717', '3453', '3954', '957', '752', '1050', '2598', '2892', 14706, 14707, 14708, 14709, 14710, 14711, 14712, 14713, 14714, '995', '14792', '2435', '3629', '14589', '3282', '2484', '954', '2333', '2870', 14779, 14780, 14781, 14782, 14783, 14784, 14785, 14786, 14787, 14788, '2713', 14793, '1083', 14808, 14809, 14810, 14811, 14812, 14813, '911', '2878', '3288', 14817, 14818, '3944', '2752', '1094', '272', '2698', '2860', 14837, 14838, 14839, 14840, 14841, 14842, 14843, '238', '3031', '3671', '2452', 14866, 14867, 14868, 14869, 14870, 14871, 14872, '2499', '3693', '4150', '250', '1385', '14505', 14898, '14635', '2750', 14914, 14915, 14916, 14917, '754', '1109', '3683', 14934, '3026', '3731', '2482', '2869', '1393', 14967, '2726', 14969, 14970, 14971, '2319', 14977, '2725', '202', '4092', '2308', '2850', '2476', 14996, 14997, 14998, '3049', '3941', '4171', '2547', '2688', 15028, 15029, '1064', 15031, 15032, 15033, 15040, 15046, 15047, 15048, '3027', 15052, '1949', '2344', '857', '2762', '2777', 15107, 15108, 15109, 15110, 15111, 15112, 15113, 15114, '896', '864', '987', '14636', '3651', '816', 15127, 15130, '3834', '14489', '2352', '3947', '4020', '884', '345', '3469', 15153, 15156, '2299', '1236', '341', '2806', '3833', '1071', '2856', '803', 15238, 15239, '1397', 15241, 15242, 15243, '14526', 15245, 15250, 15251, '2718', '741', '2738', '1087', '1070', '3640', '15306', '4073', '3047', 15279, 15280, 15281, 15282, 15288, '212', 15301, 15302, 15303, 15304, 15313, '2724', '2463', '2780', '14633', '730', '1127', '3678', '2722', '14576', '1405', '2320', '3977', '1091', '3820', '1095', '2765', '1137', '2949', '3635', '4179', '1375', '14583', '2843', '1052', '3964', '861', '1040', '2440', '267', '805', '4140', '761', '360', '2855', '220', '2703', '916', '2853', '1377', '753', '2731', '3939', '2749', '2827', '2493', '4167', '917', '3972', '1048', '3289', '2446', '2355', '3717', '2733', '14488', '14598', '963', '760', '1093', '4173', '14790', '3831', '2458', '3980', '14585', '14655', '3828', '1392', '943', '3529', '3910', '1369', '2879', '381', '3035', '14661', '880', '4130', '2687', '3468', '2490', '2706', '2331', '2439', '1044', '2322', '3697', '2692', '4018', '2700', '2494', '2695', '224', '234', '1380', '2705', '970', '3978', '2483', '1992', '3631', '1235', '3825', '4003', '2704', '412', '646', '3521', '231', '3304', '2935', '3658', '14509', '1078', '14597', '2472', '3302', '203', '2432', '14651', '271', '986', '2311', '1406', '2871', '3632', '3715', '3519', '4172', '3305', '331', '14506', '2874', '2821', '719', '712', '380', '3539', '4166', '3642', '3523', '3982', '804', '731', '2035', '2603', '3017', '2309', '4301', '3841', '1546', '2466', '3690', '14539', '3639', '1001', '933', '2865', '740', '3830', '4100', '912', '2347', '2491', '2851', '2327', '3953', '1544', '347', '3657', '3628', '348', '2597', '14626', '907', '2312', '1041', '2897', '3588', '3981'}



print(len(set_MAPY))
diff1 = set_sol - set_MAPY
diff2 = set_MAPY - set_sol 

print(diff1)
print(len(diff1))

#print(diff2)