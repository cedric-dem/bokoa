import numpy
import pickle
import statistics
import matplotlib.pyplot as plt
from config import *



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

#=========================================================================== get data

for prefix in file_prefixes_raw:

    print('----> Current prefix', prefix)
    complete_levels_list=[]

    ##open all the files, put in a list
    for current_level_index in range (raw_levels_to_generate):
        file = open(prefix + str(current_level_index), 'rb')
        elem = pickle.load(file)
        complete_levels_list.append(elem)

    print("\n==============> Nb of levels :  ", len(complete_levels_list), " levels")

    #=========================================================================== get stats
    scores=[]
    sizes=[]
    fitness=[]

    ##open all them files, put in a list
    for data in complete_levels_list:
        data.setFitnessScore()

        scores.append(data.best_score)
        sizes.append(len(data.best_moves))
        fitness.append(data.fitness)

    #=========================================================================== Describe stats in terminal

    print('\n==============> Scores')
    describeList(scores)

    print('\n==============> Sizes')
    describeList(sizes)

    print('\n==============> Fitness')
    describeList(fitness)

    #=========================================================================== Display stats as plots

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
