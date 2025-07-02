import numpy
import pickle
import statistics
import matplotlib.pyplot as plt
import random


nb_levels=10



def displayAll(L):
    plt.title("All evolution")
    for elem in L:
        plt.plot(elem.historyOfScores)
    plt.show()


#=========================================================================== get data

     
for prefix in ["generated_levels/raw/levels_0/level_","generated_levels/raw/levels_1/level_","generated_levels/raw/levels_2/level_"]:

    print('----> Current prefix', prefix)
    L=[]

    ##open all the files, put in a list
    for i in range (nb_levels):
        file = open(prefix+str(i), 'rb')
        elem = pickle.load(file)
        L.append(elem)

    print("\n==============> Nb of levels :  ",len(L)," levels")


    #=========================================================================== get stats
    scores=[]
    sizes=[]
    fitness=[]

    ##open all them files, put in a list
    for data in L:
        data.setFitnessScore()

        scores.append(data.best_score)
        sizes.append(len(data.best_moves))
        fitness.append(data.fitness)


    print('\n==============> Scores')
    print("min : ",min(scores))
    print("10% low",numpy.percentile(scores, 10))
    print("med",statistics.median(scores))
    print("10% high",numpy.percentile(scores, 90))
    print("max : ",max(scores))

    print('\n==============> Sizes')
    print("min : ",min(sizes))
    print("10% low",numpy.percentile(sizes, 10))
    print("med",statistics.median(sizes))
    print("10% high",numpy.percentile(sizes, 90))
    print("max : ",max(sizes))

    print('\n==============> Fitness')
    print("min : ",min(fitness))
    print("10% low",numpy.percentile(fitness, 10))
    print("med",statistics.median(fitness))
    print("10% high",numpy.percentile(fitness, 90))
    print("max : ",max(fitness))


    #=========================================================================== Display stats

    for elem in L:
        elem.setFitnessScore()
        
    displayAll(L)


    scores=[]
    fitness=[]
    sizes=[]

    for elem in L:
        #for elem in keep:
        scores.append(elem.historyOfScores[-1])
        fitness.append(elem.fitness)
        sizes.append(len(elem.historyOfScores))


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
