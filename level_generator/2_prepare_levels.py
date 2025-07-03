import numpy
import pickle
import statistics
import matplotlib.pyplot as plt
from config import *
import pickle
import json

def displayAll(L):
    plt.title("All evolution")
    for elem in L:
        plt.plot(elem.historyOfScores)
    plt.show()

def describeList(L):
    print("min : ",min(L))
    print("10% low",numpy.percentile(L, 10))
    print("med",statistics.median(L))
    print("10% high",numpy.percentile(L, 90))
    print("max : ",max(L))


def describeBunchOfLevels(prefixes_list, quantity):
    for prefix in prefixes_list:

        print('----> Current prefix', prefix)
        complete_levels_list = []

        ##open all the files, put in a list
        for current_level_index in range(quantity):
            file = open(prefix + str(current_level_index), 'rb')
            elem = pickle.load(file)
            complete_levels_list.append(elem)

        print("\n==============> Nb of levels :  ", len(complete_levels_list), " levels")

        # =========================================================================== get stats
        scores = []
        sizes = []
        fitness = []

        ##open all them files, put in a list
        for data in complete_levels_list:
            data.setFitnessScore()

            scores.append(data.best_score)
            sizes.append(len(data.best_moves))
            fitness.append(data.fitness)

        # =========================================================================== Describe stats in terminal

        print('\n==============> Scores')
        describeList(scores)

        print('\n==============> Sizes')
        describeList(sizes)

        print('\n==============> Fitness')
        describeList(fitness)

        # =========================================================================== Display stats as plots

        displayAll(complete_levels_list)

        scores.sort()
        fitness.sort()
        sizes.sort()

        plt.title("All final scores")
        plt.plot(scores)
        plt.show()

        plt.title("All final fitness")
        plt.plot(fitness)
        plt.show()

        plt.title("All final sizes")
        plt.plot(sizes)
        plt.show()



def createLevelFile(level, filename):
    temp=open(filename,"wb")
    pickle.dump(level, temp)

def getIndexOfClosestFrom(to_search,lst):
    closest_index=0

    for i in range (len(lst)):
        if abs(to_search-lst[closest_index].fitness)>abs(to_search-lst[i].fitness):
            closest_index=i

    return closest_index

def reduceLevelsSet():
    for difficulty in difficulties:

        print('====> Current difficulty',difficulty)

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
            createLevelFile(elem,  file_prefixes_processed[difficulty] + str(idx))

            idx+=1

        print("\n==============>  Keeping ", len(final_levels_list), " levels")

def createLevelFileAsJson(l, filename):
    result={
        "operations":l.level.level,
        "bestScore":round(float(l.best_score),2),
        "bestMoves":l.best_moves
    }

    with open(filename, 'w') as file:
        json.dump(result, file, indent=4, separators=(',', ': '), ensure_ascii=False)

def exportAllLevelsAsJson():
    for difficulty in difficulties:
        print('====> Current difficulty', difficulty)

        ##open all the files, put in a list
        for final_index_level in range(number_levels_to_keep):
            file = open(file_prefixes_processed[difficulty] + str(final_index_level), 'rb')
            data = pickle.load(file)

            createLevelFileAsJson(data, file_prefixes_processed_as_json[difficulty] + str(final_index_level) + ".json")


print("==> step 1")
describeBunchOfLevels(file_prefixes_raw, raw_levels_to_generate)
print("==> step 2")
reduceLevelsSet()
print("==> step 3")
describeBunchOfLevels(file_prefixes_processed, number_levels_to_keep)
print("==> step 4")
exportAllLevelsAsJson()