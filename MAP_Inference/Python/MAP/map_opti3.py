# -*- coding: utf-8 -*-
"""
Created on 18/08/2022
Last update 24/08/2022

@author: Victor
"""

import json
from re import S
import time
import multiprocessing


##############################################################################################################
##############################################################################################################
###################################### LOAD the data  OPTI 1 #################################################

#with open('.\..\..\Data_Json\Dictionnary\ClearDico\dico-2.5kNoConf.json', 'r') as f:
with open('.\..\..\Data_Json\Dictionnary\dicotIncNoConf_10_5k.json', 'r') as f:
    dico = json.load(f)

with open('.\..\..\Data_Json\Dictionnary\ClearDico\dicotIncNoConfClear_50_5k.json', 'r') as f2:
    dico2 = json.load(f2)

##############################################################################################################
##############################################################################################################
######################################  OPTIMISATION 1 - Algorithme 3 ######################################## 

def printSol(l_sol):
	for l in l_sol:
		print(f'{l[0]}')


def sum_weight(dico,solution):
    sum = 0
    for id in solution:
        sum += dico[str(id)][0]
    return sum


def max_sum_list_int(dico,l_sol):
    l_sum = []
    for sol in l_sol:
        l_sum.append(sum_weight(dico,sol[0]))
    return (max(l_sum), l_sol[l_sum.index(max(l_sum))][0])

"""
def deletInclude(liste):
	i = 0
	while i < len(liste):
		j = i + 1 
		while j < len(liste):
			if liste[i][0] < liste[j][0]:
				del liste[i]
				continue
			elif liste[j][0] < liste[i][0]:
				del liste[j]	
				continue
			j += 1
		i += 1
	return liste
"""

def deletInclude(liste,index):
    i = 0
    
    while i < len(liste):
        j = i + 1 
        while j < len(liste):
            #if index == 82:   
                #print(f'avant {len(liste[0])}')
                #if 3842 in liste[i][0] :
                #    print(f'i = {i}')
                #if 3842 in liste[j][0]:
                #    print(f'j = {j}')
            if liste[i][0] < liste[j][0]:
                del liste[i]
                continue
            elif liste[j][0] < liste[i][0]:
                del liste[j]	
                continue
            j += 1
        i += 1
    #if index == 81:   
    #    print(f'apres {len(liste)}\n')
    return liste

"""
#liste = [[id_nodes],[conflicts]]
def compatible_merge(node,liste,dico):
    l_merge_comp = [{node}, set(dico[str(node)][1]), dico[str(node)][0]]
    compatible = True
    for n in liste[0]:
        if node in dico[str(n)][1]:
            compatible = False
        else:
            l_merge_comp[0].add(n)
            l_merge_comp[1] |= set(dico[str(n)][1])
            l_merge_comp[2] += dico[str(n)][0]
    return (l_merge_comp,compatible)
"""

#liste = [[id_nodes],[conflicts]]
def compatible_merge(node,liste,dico):
    l_merge_comp = [{node}, set(dico[str(node)][1]), dico[str(node)][0]]
    #print(f'node = {node} and liste[1] = {liste[1]}')
    if not(node in liste[1]):
        #print("C'est True")
        compatible = True
        l_merge_comp = []
    else:
        compatible = False
        for n in liste[0]:
            if not(node in dico[str(n)][1]):
                l_merge_comp[0].add(n)
                l_merge_comp[1] |= set(dico[str(n)][1])
                l_merge_comp[2] += dico[str(n)][0]
    return (l_merge_comp,compatible)
		

"""
# Build the solutions
def build_sol(dico,index):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    threshold = int(nb_nodes*0.6)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]

    tmp_comp = 0
    tmp_inc = 0
    taille_inc = 0
    i_taille = 0

    for i in range(1,len(l_dico)):
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste
        while j < len(liste_sol)-h:
            if index < 1:
                start = time.time()
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
            if index < 1:
                end = time.time()
                elapsed = end - start
                tmp_comp += elapsed
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] += l_dico[i][1][0]
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]
                elif i > threshold:
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        del liste_sol[j]
                        j -= 1    
            else:
                exist = False
                for l in liste_sol:
                    if l[0] == l2[0]:
                        exist = True
                        break 
                if not exist:
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
            j += 1

        if index < 1:
                start = time.time()
                taille_inc += len(liste_sol)
                i_taille += 1
                
        if i%2 == 0:
            liste_sol = deletInclude(liste_sol)

        if index < 1:
                end = time.time()
                elapsed = end - start
                tmp_inc += elapsed
    if index == 0:
        print(f'temps de comp à indice {index} = {tmp_comp}')
        print(f'temps de inc à indice {index} = {tmp_inc}')
        print(f'taille moyenne de list_sol dans inc à indice {index} = {taille_inc/i_taille}')
    return liste_sol
"""

#print(build_sol(dico))


# Build the solutions
def build_sol(dico,index):
    liste_sol = []
    l_dico = list(dico.items())
    nb_nodes = len(l_dico)
    threshold = int(nb_nodes*0.6)
    liste_sol.append([{int(l_dico[0][0])},set(l_dico[0][1][1]), l_dico[0][1][0]])
    maxi = l_dico[0][1][0]

    
    tmp_comp = 0
    tmp_inc = 0
    taille_inc_a = 0
    taille_inc_b = 0
    i_taille = 0
    

    for i in range(1,len(l_dico)):
        j = 0
        h = 0 # sert à ne pas compter plusieurs fois les nodes ajoutés en fin de liste
        #print(f'i = {i} and len(liste_sol) = {len(liste_sol)}')
        while j < len(liste_sol)-h:
        #for j in range(0,len(liste_sol)-h):    
            if index < 1:
                start = time.time()
            (l2,bool) = compatible_merge(int(l_dico[i][0]),liste_sol[j],dico)
            #if int(l_dico[i][0]) == 3842:
                #print(f'j = {j} list_sol avant = {liste_sol[j][0]}')
                #print(l2,bool)
            if index < 1:
                end = time.time()
                elapsed = end - start
                tmp_comp += elapsed
            if bool:
                liste_sol[j][0].add(int(l_dico[i][0]))
                #if int(l_dico[i][0]) == 3842:
                #    print(f'i = {i} et j = {j} list_sol après = {liste_sol[j][0]}\n')
                liste_sol[j][1] |= set(l_dico[i][1][1])
                liste_sol[j][2] += l_dico[i][1][0]
                if maxi < liste_sol[j][2]:
                    maxi = liste_sol[j][2]
                
                elif i > threshold:
                    potential_max = liste_sol[j][2]
                    for k in range(i+1,len(l_dico)):
                        potential_max += l_dico[k][1][0]  
                    if potential_max < maxi:
                        #if 3842 in liste_sol[j][0]:
                        #    print(f'on supprime 3842 à {j}')
                        del liste_sol[j]
                        j -= 1    
                
            else:
                """
                include = False
                ind = 0
                x = 0
                while ind < len(liste_sol)-x:                    
                    if liste_sol[ind][0] < l2[0]:
                        del liste_sol[ind]
                        x += 1
                        ind -=  1  
                    elif l2[0] <= liste_sol[ind][0] :
                        include = True     
                        break           
                    ind +=  1
                """
                include = False
                #print(f'Avant test include j = {j} et l2 avec {l2[0]}')
                #printSol(liste_sol)
                #print('\n')
                for l in liste_sol:
                    if l2[0] <= l[0]:# or l2[0]>l[0]:
                        include = True
                        break
                

                if not(include):
                    liste_sol += [[l2[0],l2[1],l2[2]]]
                    h += 1
                    if maxi < l2[2]:
                        maxi = l2[2]
                    #continue
                
            j += 1

        if index < 1:
                start = time.time()
                taille_inc_b += len(liste_sol)
                i_taille += 1
                
        if i%2  == 0:    
            liste_sol = deletInclude(liste_sol,i)
        """
        if i > 82:
            existe = False
            for l in liste_sol:
                if 3842 in l[0]:
                    existe = True
            if not existe:
                print(f'disparition en {i}')
        """
            #printSol(liste_sol)
            #print('\n')
    
        if index < 1:
                end = time.time()
                elapsed = end - start
                taille_inc_a += len(liste_sol)
                tmp_inc += elapsed
    if index == 0:
        print(f'temps de comp à indice {index} = {tmp_comp}')
        print(f'temps de inc à indice {index} = {tmp_inc}')
        print(f'taille moyenne de list_sol before dans inc à indice {index} = {taille_inc_b/i_taille}')
        print(f'taille moyenne de list_sol after dans inc à indice {index} = {taille_inc_a/i_taille}')
    
    return liste_sol

"""
start = time.time()
res = build_sol(d_1)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution inc : {elapsed:.5}s')
print("\n")
printSol(res)
print(len(res))
h = []
for elem in res:
    h.append(elem[2])
print(max(h))

print(max_sum_list_int(d_1,res))
"""



##############################################################################################################
##############################################################################################################
###################################  OPTIMISATION 2 - Algorithme 3+ ########################################## 


##################################### LOAD the data for OPTI 2 ###############################################
#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5kClear.json', 'r') as f: 	
#with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5k.json', 'r') as f: 	
with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_10_5k.json', 'r') as f: 	
    l_dico = json.load(f)


#################################### Apply Opti 1 on the list of dico ########################################
def solutionForList(l_dico):
    output = [0,[]]
    i = 0
    #distrib = [0,0,0,0,0,0,0,0,0,0]
    #sum = 0
    size = len(l_dico["list"])
    #print(size)
    #record = []
    for dico in l_dico["list"]:
        if i == 0:
        #index = int(len(dico)/50)
        #distrib[index] += 1
            print(f'{i} / {size} with length = {len(dico)}')# et distrib = {distrib} ')
            #max = 0
            #avg = 0
            #for k,v in dico.items():
                #avg += len(v[1])
                #if  len(v[1]) > max:
                    #max = len(v[1])
            #record.append((max,avg/len(dico)))
        #sum += len(dico)
        if i == 0:
            start = time.time()
        val,liste = max_sum_list_int(dico,build_sol(dico,i))
        if i == 0:
            end = time.time()
            elapsed = end - start
            print(f'Temps d\'exécution {i} : {elapsed:.5}s')

        output[0] += val
        output[1] += liste
        i+=1
    #print(f'nb total nodes conf = {sum}')
    #print(f'record = {record}')
    return output



start = time.time()
output1 = solutionForList(l_dico)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution conf : {elapsed:.5}s')

print(output1[0])
#print(output1[1])

#print(f'nb nodes clear conf : {len(dico2)}')
#output12 = sum_weight(dico2,dico2)
#print(output12)

#print(f'nb nodes no conf : {len(dico)}')
output2 = sum_weight(dico,dico)
print(output2)

print(f'Score total = {output1[0] + output2}')
#print(f'Score total = {output1[0] + output12 + output2}')
#print(output1[1])

approx     = [2896, 2897, 2898, 2899, 2900, 2901, 2903, 2904, 2905, 2906, 2907, 2909, 2910, 2911, 2912, 2913, 2914, 2915, 2916, 2917, 2918, 2919, 2920, 2921, 2922, 2923, 2924, 2925, 2926, 2927, 2928, 2929, 2930, 2932, 2933, 2935, 2937, 2938, 2940, 2941, 2942, 2943, 2944, 2945, 2946, 2947, 2949, 2951, 2952, 2953, 2954, 2955, 2956, 2957, 2959, 2963, 2964, 2965, 2966, 2967, 2968, 2974, 2975, 2976, 2977, 2978, 2979, 2980, 2982, 2986, 2987, 2989, 2990, 2991, 2992, 2993, 2995, 2999, 3001, 3002, 3003, 3005, 3006, 3009, 3013, 3016, 3017, 3018, 3019, 3020, 3021, 3022, 3024, 3028, 2688, 2690, 2692, 2693, 2694, 2695, 2696, 2698, 2699, 2700, 7309, 2701, 2702, 2704, 2705, 2706, 2707, 2708, 2709, 2703, 2711, 2712, 2713, 2714, 2715, 2716, 2718, 2719, 2720, 2721, 2722, 2723, 2725, 2726, 2727, 2728, 2729, 2730, 2731, 2732, 2733, 2734, 2735, 2736, 2737, 2667, 2668, 2669, 2670, 2671, 2672, 2673, 2674, 2677, 2678, 2680, 2681, 2682, 2683, 2684, 2685, 2686, 2687, 2839, 2840, 2843, 2844, 2845, 2846, 2847, 2848, 2849, 2850, 2851, 2852, 2853, 2854, 2855, 2856, 2857, 2858, 2859, 2860, 2861, 2862, 2863, 2864, 2865, 2866, 2867, 2868, 2869, 2870, 2871, 2872, 2873, 2874, 2876, 2877, 2878, 2879, 2880, 2881, 2882, 2883, 2884, 2885, 2886, 2887, 2889, 2890, 2891, 2894, 3265, 3266, 3267, 3268, 3271, 3274, 3275, 3277, 3278, 3279, 3281, 3282, 3283, 3285, 3286, 3287, 3289, 3290, 3291, 3292, 3294, 3295, 3296, 3297, 3298, 3300, 3301, 3302, 3303, 3304, 3305, 3307, 3310, 3312, 3313, 3316, 3317, 3318, 3321, 3322, 3324, 3325, 3326, 3327, 3330, 3331, 3333, 3334, 3335, 3336, 3340, 3341, 3343, 3344, 3345, 3346, 3351, 3352, 3354, 3355, 3356, 3357, 3363, 3364, 3366, 3367, 3368, 3369, 3376, 3377, 3379, 3380, 3381, 3382, 3389, 3390, 3391, 3393, 3394, 3395, 3396, 3403, 3405, 3408, 3410, 3411, 3418, 2816, 2817, 2818, 2820, 2821, 2822, 2824, 2825, 2828, 2829, 2830, 2831, 2832, 2833, 2835, 2836, 2837, 2838, 2793, 2794, 2795, 2796, 2797, 2798, 2799, 2800, 2801, 2802, 2803, 2804, 2805, 2806, 2807, 2808, 2809, 2811, 2814, 2815, 2639, 2640, 2641, 2642, 2643, 2644, 2645, 2646, 2647, 2648, 2649, 2650, 2651, 2652, 2653, 2654, 2655, 2656, 2657, 2658, 2659, 2660, 2661, 2664, 4352, 4354, 4355, 4356, 4357, 4358, 4360, 4361, 4362, 4363, 4364, 4365, 4366, 4367, 4368, 4370, 4371, 4372, 4373, 4374, 4375, 4376, 4377, 4378, 4379, 4380, 4381, 4382, 4383, 4384, 4385, 4386, 4387, 4388, 4390, 4391, 4392, 4393, 4394, 4395, 4396, 4397, 4400, 4401, 4402, 4403, 4404, 4405, 4406, 4407, 4411, 4423, 4436, 4345, 4346, 4347, 4348, 4349, 4350, 4351, 3655, 3658, 3659, 3662, 3667, 3668, 3669, 3673, 3674, 3675, 3677, 3680, 3681, 3682, 3684, 3688, 3689, 3690, 3692, 3697, 3698, 3699, 3701, 3704, 3707, 3708, 3709, 3711, 3714, 3715, 3718, 3719, 3722, 3725, 3726, 3731, 3732, 3737, 3738, 3743, 3744, 3747, 3750, 3751, 3757, 3758, 3759, 3761, 3764, 3765, 3772, 3773, 3774, 3779, 3780, 3788, 3789, 3790, 3792, 3795, 3796, 3805, 3806, 3807, 3809, 3812, 3813, 3823, 3824, 3825, 3827, 3830, 3831, 3842, 6531, 6500, 6470, 6570, 6476, 6510, 6543, 6483, 6585, 6458, 6491, 6556, 6461, 3139, 3109, 3079, 3209, 3178, 3083, 3118, 3151, 3088, 3094, 3164, 3101, 4993, 5031, 5001, 4973, 5037, 5010, 5043, 4979, 5049, 4986, 5020, 5221, 5191, 5161, 5260, 5165, 5200, 5233, 5176, 5210, 5246, 5183, 6884, 6918, 6863, 6864, 6866, 6899, 6869, 6873, 6908, 6878, 3360, 3361, 3400, 3372, 3349, 3414, 3415, 3350, 3385, 3386, 3909, 3943, 3916, 3888, 3889, 3891, 3924, 3894, 3898, 3933, 3903, 3904, 3910, 3944, 3917, 3890, 3892, 3925, 3895, 3899, 3934, 4864, 4838, 4905, 4873, 4843, 4912, 4849, 4883, 4856, 5540, 5542, 5510, 5514, 5519, 5521, 5525, 5527, 5532, 5534, 3320, 3329, 3398, 3338, 3371, 3348, 3384, 3359, 3923, 3932, 3941, 3951, 3040, 3044, 3049, 3055, 3062, 3035, 3037, 4232, 4673, 4677, 4682, 4688, 4695, 4668, 4670, 4931, 4937, 4944, 4917, 4919, 4922, 4926, 32, 20, 23, 25, 27, 29, 3425, 3428, 3432, 3436, 3422, 3423, 4222, 4674, 4678, 4683, 4689, 4696, 4671, 5316, 5325, 5301, 5335, 5308, 5356, 5360, 5363, 5367, 5372, 5374, 6629, 6632, 6641, 6647, 6654, 2609, 2610, 7182, 2634, 2635, 7207, 2520, 2521, 2522, 71, 3160, 3218, 3235, 3173, 3600, 3601, 3603, 3606, 4032, 4033, 4197, 4225, 5033, 5003, 5012, 5045, 5022, 5658, 5676, 5669, 5663, 5696, 5700, 5690, 5691, 5693, 2593, 2594, 2576, 2577, 2578, 2600, 2512, 63, 44, 45, 2495, 3434, 3427, 3430, 4025, 4697, 4684, 4679, 5729, 5723, 5726, 5930, 5934, 5927, 6080, 6074, 6075, 6604, 6680, 6681, 6683, 6686, 2524, 2525, 7137, 2563, 2485, 2493, 2538, 2535, 7126, 7127, 4201, 4199, 5561, 5566, 5848, 5850, 6606, 6832, 2497, 2498, 2500, 2504, 2506, 2507, 2508, 2511, 2514, 2516, 2526, 7103, 2533, 7113, 7114, 7117, 2545, 2551, 2557, 7139, 2567, 7141, 2570, 2575, 2595, 2598, 2602, 2606, 2608, 2613, 2615, 2619, 2624, 2625, 2627, 2628, 2630, 2632, 2637, 2739, 2741, 3460, 3639, 3959, 4117, 4123, 4294, 5491, 6030, 6175, 6609, 6831, 6944]

not_approx = [2896, 2897, 2898, 2899, 2900, 2901, 2903, 2904, 2905, 2906, 2907, 2909, 2910, 2911, 2912, 2913, 2914, 2915, 2916, 2917, 2918, 2919, 2920, 2921, 2922, 2923, 2924, 2925, 2926, 2927, 2928, 2929, 2930, 2932, 2933, 2935, 2937, 2938, 2940, 2941, 2942, 2943, 2944, 2945, 2946, 2947, 2949, 2951, 2952, 2953, 2954, 2955, 2956, 2957, 2959, 2963, 2964, 2965, 2966, 2967, 2968, 2974, 2975, 2976, 2977, 2978, 2979, 2980, 2982, 2986, 2987, 2989, 2990, 2991, 2992, 2993, 2995, 2999, 3001, 3002, 3003, 3005, 3006, 3009, 3013, 3016, 3017, 3018, 3019, 3020, 3021, 3022, 3024, 3028, 2688, 2690, 2692, 2693, 2694, 2695, 2696, 2698, 2699, 2700, 7309, 2701, 2702, 2704, 2705, 2706, 2707, 2708, 2709, 2703, 2711, 2712, 2713, 2714, 2715, 2716, 2718, 2719, 2720, 2721, 2722, 2723, 2725, 2726, 2727, 2728, 2729, 2730, 2731, 2732, 2733, 2734, 2735, 2736, 2737, 2666, 2667, 2668, 2669, 2670, 2671, 2672, 2673, 2674, 2675, 2677, 2678, 2679, 2680, 2681, 2682, 2683, 2684, 2685, 2686, 2687, 2839, 2840, 2841, 2842, 2843, 2844, 2845, 2846, 2847, 2848, 2849, 2850, 2851, 2852, 2853, 2854, 2855, 2856, 2857, 2858, 2859, 2860, 2861, 2862, 2863, 2864, 2865, 2866, 2867, 2868, 2869, 2870, 2871, 2872, 2873, 2874, 2876, 2877, 2878, 2879, 2880, 2881, 2882, 2883, 2884, 2885, 2886, 2887, 2889, 2890, 2891, 2894, 3265, 3266, 3267, 3268, 3271, 3274, 3275, 3277, 3278, 3279, 3281, 3282, 3283, 3285, 3286, 3287, 3289, 3290, 3291, 3292, 3294, 3295, 3296, 3297, 3298, 3300, 3301, 3302, 3303, 3304, 3305, 3307, 3310, 3312, 3313, 3316, 3317, 3318, 3321, 3322, 3324, 3325, 3326, 3327, 3330, 3331, 3333, 3334, 3335, 3336, 3340, 3341, 3343, 3344, 3345, 3346, 3351, 3352, 3354, 3355, 3356, 3357, 3363, 3364, 3366, 3367, 3368, 3369, 3376, 3377, 3379, 3380, 3381, 3382, 3389, 3390, 3391, 3393, 3394, 3395, 3396, 3403, 3405, 3408, 3410, 3411, 3418, 2816, 2817, 2818, 2820, 2821, 2822, 2824, 2825, 2828, 2829, 2830, 2831, 2832, 2833, 2835, 2836, 2837, 2838, 2793, 2794, 2795, 2796, 2797, 2798, 2799, 2800, 2801, 2802, 2803, 2804, 2805, 2806, 2807, 2808, 2809, 2811, 2814, 2815, 2639, 2640, 2641, 2642, 2643, 2644, 2645, 2646, 2647, 2648, 2649, 2650, 2651, 2652, 2653, 2654, 2655, 2656, 2657, 2658, 2659, 2660, 2661, 2664, 4352, 4354, 4355, 4356, 4357, 4358, 4360, 4361, 4362, 4363, 4364, 4365, 4366, 4367, 4368, 4370, 4371, 4372, 4373, 4374, 4375, 4376, 4377, 4378, 4379, 4380, 4381, 4382, 4383, 4384, 4385, 4386, 4387, 4388, 4390, 4391, 4392, 4393, 4394, 4395, 4396, 4397, 4400, 4401, 4402, 4403, 4404, 4405, 4406, 4407, 4411, 4423, 4436, 4345, 4346, 4347, 4348, 4349, 4350, 4351, 3655, 3658, 3659, 3662, 3667, 3668, 3669, 3673, 3674, 3675, 3677, 3680, 3681, 3682, 3684, 3688, 3689, 3690, 3692, 3697, 3698, 3699, 3701, 3704, 3707, 3708, 3709, 3711, 3714, 3715, 3718, 3719, 3722, 3725, 3726, 3731, 3732, 3737, 3738, 3743, 3744, 3747, 3750, 3751, 3757, 3758, 3759, 3761, 3764, 3765, 3772, 3773, 3774, 3779, 3780, 3788, 3789, 3790, 3792, 3795, 3796, 3805, 3806, 3807, 3809, 3812, 3813, 3823, 3824, 6233, 6236, 6238, 6243, 6246, 6248, 6254, 6257, 6259, 6260, 6261, 6266, 6269, 6271, 7163, 2580, 2581, 2582, 2583, 2584, 2586, 2587, 2588, 2589, 2590, 2591, 5504, 5505, 5507, 5508, 5511, 5512, 5503, 5516, 5517, 5522, 5523, 5528, 5529, 5530, 5501, 5502, 5535, 6050, 6051, 6053, 6056, 6057, 6059, 6060, 6063, 6064, 6066, 6067, 6038, 6041, 6042, 6045, 6046, 3072, 3137, 3074, 3107, 3077, 3207, 3176, 3081, 3116, 3149, 3086, 3092, 3126, 3191, 3224, 3099, 3136, 3073, 3076, 3206, 3175, 3080, 3115, 3148, 3085, 3091, 3125, 3223, 3161, 3098, 3070, 3071, 3530, 3531, 3532, 3533, 3535, 3536, 3538, 3539, 3540, 3542, 3543, 3544, 3545, 3547, 3548, 3549, 3550, 3551, 3553, 3555, 3557, 3558, 3560, 3561, 3562, 5121, 5123, 5125, 5128, 5130, 5133, 5136, 5139, 5141, 5143, 5146, 5148, 5118, 3872, 3873, 3782, 3783, 3816, 3815, 3754, 3767, 3852, 3853, 3753, 3798, 3799, 3768, 3833, 3834, 3740, 4640, 4641, 4642, 4643, 4644, 4648, 4652, 4653, 4657, 4658, 4659, 4663, 4664, 4637, 4638, 4639, 5760, 5793, 5820, 5794, 5765, 5801, 5771, 5803, 5753, 5810, 5813, 5750, 5751, 5785, 5786, 5756, 3937, 3938, 3907, 3908, 3913, 3914, 3947, 3948, 3920, 3921, 3928, 3929, 3902, 6464, 6530, 6499, 6469, 6569, 6475, 6509, 6542, 6482, 6455, 6584, 6490, 6555, 6460, 6465, 6531, 6500, 6470, 6570, 6476, 6510, 6543, 6483, 6585, 6458, 6491, 6556, 6461, 3139, 3109, 3079, 3209, 3178, 3083, 3118, 3151, 3088, 3094, 3164, 3101, 4993, 5031, 5001, 4973, 5037, 5010, 5043, 4979, 5049, 4986, 5020, 5221, 5191, 5161, 5260, 5165, 5200, 5233, 5176, 5210, 5246, 5183, 6884, 6918, 6863, 6864, 6866, 6899, 6869, 6873, 6908, 6878, 3360, 3361, 3400, 3372, 3349, 3414, 3415, 3350, 3385, 3386, 3909, 3943, 3916, 3888, 3889, 3891, 3924, 3894, 3898, 3933, 3903, 3904, 3910, 3944, 3917, 3890, 3892, 3925, 3895, 3899, 3934, 4864, 4838, 4905, 4873, 4843, 4912, 4849, 4883, 4856, 5540, 5542, 5510, 5514, 5519, 5521, 5525, 5527, 5532, 5534, 3320, 3329, 3398, 3338, 3371, 3348, 3384, 3359, 3923, 3932, 3941, 3951, 3040, 3044, 3049, 3055, 3062, 3035, 3037, 4232, 4673, 4677, 4682, 4688, 4695, 4668, 4670, 4931, 4937, 4944, 4917, 4919, 4922, 4926, 32, 20, 23, 25, 27, 29, 3425, 3428, 3432, 3436, 3422, 3423, 4222, 4674, 4678, 4683, 4689, 4696, 4671, 5316, 5325, 5301, 5335, 5308, 5356, 5360, 5363, 5367, 5372, 5374, 6629, 6632, 6641, 6647, 6654, 2609, 2610, 7182, 2634, 2635, 7207, 2520, 2521, 2522, 71, 3160, 3218, 3235, 3173, 3600, 3601, 3603, 3606, 4032, 4033, 4197, 4225, 5033, 5003, 5012, 5045, 5022, 5658, 5676, 5669, 5663, 5696, 5700, 5690, 5691, 5693, 2593, 2594, 2576, 2577, 2578, 2600, 2512, 63, 44, 45, 2495, 3434, 3427, 3430, 4025, 4697, 4684, 4679, 5729, 5723, 5726, 5930, 5934, 5927, 6080, 6074, 6075, 6604, 6680, 6681, 6683, 6686, 2524, 2525, 7137, 2563, 2485, 2493, 2538, 2535, 7126, 7127, 4201, 4199, 5561, 5566, 5848, 5850, 6606, 6832, 2497, 2498, 2500, 2504, 2506, 2507, 2508, 2511, 2514, 2516, 2526, 7103, 2533, 7113, 7114, 7117, 2545, 2551, 2557, 7139, 2567, 7141, 2570, 2575, 2595, 2598, 2602, 2606, 2608, 2613, 2615, 2619, 2624, 2625, 2627, 2628, 2630, 2632, 2637, 2739, 2741, 3460, 3639, 3959, 4117, 4123, 4294, 5491, 6030, 6175, 6609, 6831, 6944]

set_a = set(approx)

set_na =set(not_approx)

#print(set_a - set_na)
#print('\n')
#print(set_na - set_a)

#3842: 3802, 3819, 3837
#3825: 3820, 3857, 3877

#3070 : 3189, 3204, 3205, 3220, 3221, 3237, 3238

############################################ Parallelization #################################################


def task(dico):
	val,liste = max_sum_list_int(dico,build_sol(dico))
	return val,liste


def parallelization(l_dico):
	output = [0,[]]
	#start = time.time()
	pool = multiprocessing.Pool(2)
	result = pool.imap(task, l_dico["list"])
	for val,liste in result:
		output[0] += val
		output[1] += liste
	#end = time.time()
	#elapsed = end - start
	#print(f'Temps d\'exécution : {elapsed:.5}s')
	return output#,elapsed

"""
if __name__ == '__main__':
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_50_50kClear.json', 'r') as f: 
    with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDicotInc_10_50k.json', 'r') as f: 		
    #with open('.\..\..\Data_Json\Dictionnary\listDico\listOfDico2.5k.json', 'r') as f: 
        l_dico = json.load(f)

    start = time.time()
    output1 = parallelization(l_dico)
    end = time.time()
    elapsed = end - start
    print(f'Temps d\'exécution conf : {elapsed:.5}s\n')
    print(output1[0])

    #start = time.time()
    #output2 = sum_weight(dico,dico)
    #print(output2)
    #end = time.time()
    #elapsed2 = end - start
    #print(f'Temps d\'exécution no conf : {elapsed2:.5}s')

    #print(f'Temps d\'exécution total : {elapsed1+elapsed2:.5}s')
    #print(f'Score total = {output1[0]+output2}')
    #print(f'Score total = {output1[0]}')

    #output12 = sum_weight(dico2,dico2)
    #print(output12)

    output2 = sum_weight(dico,dico)
    print(output2)

    #print(f'Score total = {output1[0] + output12 + output2}')
    print(f'Score total = {output1[0] + output2}')
"""