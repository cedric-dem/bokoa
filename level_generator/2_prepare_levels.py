import numpy
import statistics
import matplotlib.pyplot as plt
from config import *
import pickle
import json

def plotAllEvolutions(list_evolutions):
    plt.title("All evolution")
    for elem in list_evolutions:
        plt.plot(elem.historyOfScores)
    plt.show()

def describeList(lst):
    print("min : ", min(lst))
    print("10% low", numpy.percentile(lst, 10))
    print("med", statistics.median(lst))
    print("10% high", numpy.percentile(lst, 90))
    print("max : ", max(lst))

def describeBunchOfLevels(prefixes_list, quantity):

    for prefix in prefixes_list:
        print('====> Current prefix :', prefix)
        complete_levels_list = []

        ##open all the files, put in a list
        for current_level_index in range(quantity):
            file = open(prefix + str(current_level_index), 'rb')
            elem = pickle.load(file)
            complete_levels_list.append(elem)

        print("====> Number of levels :  ", len(complete_levels_list))

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

        print('====> Scores')
        describeList(scores)

        print('====> Sizes')
        describeList(sizes)

        print('====> Fitness')
        describeList(fitness)

        # =========================================================================== Display stats as plots

        plotAllEvolutions(complete_levels_list)

        scores.sort()
        fitness.sort()
        sizes.sort()

        plotGraph(scores, "All final scores")
        plotGraph(fitness, "All fitness")
        plotGraph(sizes, "All sizes")

def plotGraph(scores, plotname):
    plt.title(plotname)
    plt.plot(scores)
    plt.show()

def createLevelFile(level, filename):
    temp=open(filename,"wb")
    pickle.dump(level, temp)

def getIndexOfClosestFrom(to_search, levels_list):
    closest_index=0

    for i in range (len(levels_list)):
        if abs(to_search - levels_list[closest_index].fitness)>abs(to_search - levels_list[i].fitness):
            closest_index=i

    return closest_index

def reduceLevelsSet():
    for difficulty in difficulties:

        print('====> Current difficulty',difficulty)

        size=all_grid_sizes[difficulty][0]

        #=========================================================================== get data
        complete_levels_list=[]

        ##open all the files, put in a list
        for reduced_levels_index in range (raw_levels_to_generate):
            file = open(file_prefixes_raw[difficulty] + str(reduced_levels_index), 'rb')
            data = pickle.load(file)

            complete_levels_list.append(data)

        print("====>  Initially total of  ",len(complete_levels_list)," levels")

        #=========================================================================== kept levels
        levels_size_acceptable=[]
        if size==4:
            lowest_size=6
        elif size==5:
            lowest_size=12
        else:
            lowest_size=18

        for current_level in complete_levels_list:
            if len(current_level.best_moves)>=lowest_size:
                levels_size_acceptable.append(current_level)

        print("====>  After remove too small levels total of  ",len(levels_size_acceptable)," levels")

        #=========================================================================== set fitness of kept levels
        for current_level in levels_size_acceptable:
            current_level.setFitnessScore()

        #=========================================================================== sort kept levels
        levels_size_acceptable.sort()

        #=========================================================================== Display infos

        fitness=[]

        for current_level in levels_size_acceptable:
            fitness.append(current_level.fitness)

        #=========================================================================== modify it

        #######################################doing the mod
        ###############theoretical_fitness
        theoretical_fitness=[]

        average_step=(levels_size_acceptable[-1].fitness-levels_size_acceptable[0].fitness)/number_levels_to_keep

        current=levels_size_acceptable[0].fitness

        for reduced_levels_index in range (number_levels_to_keep):
            theoretical_fitness.append(current)
            current+=average_step

        print('====> Average step',average_step)
        print("====> Theoretical fitness : ",theoretical_fitness)

        ###################doing the job
        levels_reduced=[]

        for reduced_levels_index in range (number_levels_to_keep):
            index=getIndexOfClosestFrom(theoretical_fitness[reduced_levels_index], levels_size_acceptable)
            this_one=levels_size_acceptable.pop(index)
            levels_reduced.append(this_one)

        fitness=[]

        levels_reduced.sort()

        for current_level in levels_reduced:
            fitness.append(current_level.fitness)

        print("====> Real Fitness : ",fitness)

        for index_reduced in range (len(levels_reduced)):
            current_level=levels_reduced[index_reduced]
            createLevelFile(current_level,  file_prefixes_processed[difficulty] + str(index_reduced))

        print("====>  Keeping ", len(levels_reduced), " levels")

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

print("========> step 1: describe complete set of levels")
describeBunchOfLevels(file_prefixes_raw, raw_levels_to_generate)
print("========> step 2: reduce set of levels")
reduceLevelsSet()
print("========> step 3: describe reduced set of levels")
describeBunchOfLevels(file_prefixes_processed, number_levels_to_keep)
print("========> step 4: export as json")
exportAllLevelsAsJson()