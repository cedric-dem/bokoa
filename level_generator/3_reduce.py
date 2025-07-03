import pickle
import json
from config import *

def createLevelFile(level, filename):
    temp=open(filename,"wb")
    pickle.dump(level, temp)

def getIndexOfClosestFrom(to_search,lst):
    closest_index=0

    for i in range (len(lst)):
        if abs(to_search-lst[closest_index].fitness)>abs(to_search-lst[i].fitness):
            closest_index=i

    return closest_index

for difficulty in difficulties:

    print('====> Current difficulty',difficulty)

    #=========================================================================== blabla


    size=all_grid_sizes[difficulty][0]

    #=========================================================================== get data
    L_all=[]

    ##open all the files, put in a list
    for final_index_level in range (raw_levels_to_generate):
        file = open(file_prefixes_raw[difficulty] + str(final_index_level), 'rb')
        data = pickle.load(file)
        
        L_all.append(data)
        
    print("\n==============>  Initially total of  ",len(L_all)," levels")

    #=========================================================================== kept levels
    L=[]
    if size==4:
        lowest_size=6
    elif size==5:
        lowest_size=12
    else:
        lowest_size=18

    for elem in L_all:
        if len(elem.best_moves)>=lowest_size:
            L.append(elem)

    print("\n==============>  After remove  total of  ",len(L)," levels")

    #=========================================================================== set fitness of kept levels
    for elem in L:
        elem.setFitnessScore()

    #=========================================================================== sort kept levels
    L.sort()
    #keep=keep[::-1]

    #=========================================================================== Display infos

    print("********************************************************************************************************************* BEFOR")
    fitness=[]

    for elem in L:
        fitness.append(elem.fitness)

    #=========================================================================== modify it

    #######################################doing the mod
    ###############theoretical
    theoretical=[]

    average_step=(L[-1].fitness-L[0].fitness)/number_levels_to_keep

    current=L[0].fitness

    for final_index_level in range (number_levels_to_keep):
        theoretical.append(current)
        current+=average_step

    #print(len(theoretical))
    #print('avg s',average_step)
    print("THEORETICAL : ",theoretical)

    ###################doing the job

    final_levels_list=[]
    #keep_list.append(keep[0])

    for final_index_level in range (100):
        index=getIndexOfClosestFrom(theoretical[final_index_level], L)
        this_one=L.pop(index)
        final_levels_list.append(this_one)

    print("************************************************************************************************************* AFER")
    fitness=[]

    final_levels_list.sort()

    for elem in final_levels_list:
        fitness.append(elem.fitness)

    print("FITNESS : ",fitness)
    print(len(fitness))

    print('\n==============> Result : ')
    idx=0
    for elem in final_levels_list:

        print("====> NEW")
        #createLevelFileAsJson(elem, file_prefixes_processed[difficulty] + str(idx) + ".json")
        createLevelFile(elem,  file_prefixes_processed[difficulty] + str(idx))

        idx+=1

    print("\n==============>  Keeping ", len(final_levels_list), " levels")
