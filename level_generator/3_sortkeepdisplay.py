import pickle
import json
from config import *


def createLevelFileAsJson(l, filename):
    result={
        "operations":l.level.level,
        "bestScore":round(float(l.best_score),2),
        "bestMoves":l.best_moves
    }

    with open(filename, 'w') as file:
        json.dump(result, file, indent=4, separators=(',', ': '), ensure_ascii=False)


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
    for i in range (raw_levels_to_generate):
        file = open(file_prefixes_raw[difficulty]+str(i), 'rb')
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

    for i in range (number_levels_to_keep):
        theoretical.append(current)
        current+=average_step

    #print(len(theoretical))
    #print('avg s',average_step)
    print("THEORETICAL : ",theoretical)

    ###################doing the job

    keep_list=[]
    #keep_list.append(keep[0])

    for i in range (100):
        index=getIndexOfClosestFrom(theoretical[i], L)
        this_one=L.pop(index)
        keep_list.append(this_one)

    #keep_list.append(keep[-1])

    #print(keep_list)

    print("************************************************************************************************************* AFER")
    fitness=[]

    keep_list.sort()

    for elem in keep_list:
        fitness.append(elem.fitness)

    print("FITNESS : ",fitness)
    print(len(fitness))

    print('\n==============> Result : ')
    idx=0
    for elem in keep_list:
        #print(elem.id,elem.getGoodFormat())
        #print(elem.getGoodFormat())

        print("====> NEW")
        createLevelFileAsJson(elem, file_prefixes_processed[difficulty] + str(idx) + ".json")

        idx+=1

    print("\n==============>  Keeping ",len(keep_list)," levels")
