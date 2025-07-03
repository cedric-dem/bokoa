import numpy
import statistics
import matplotlib.pyplot as plt
from config import *
import pickle
import json

def plot_all_evolutions(list_evolutions, context_name):
    plt.title("All evolution" + context_name)
    for elem in list_evolutions:
        plt.plot(elem.historyOfScores)

    plt.xlabel("Number Of Moves")
    plt.ylabel("Score")
    plt.show()

def plot_graph(evolution, plot_name, x_labels, y_labels):
    plt.title(plot_name)
    plt.xlabel(x_labels)
    plt.ylabel(y_labels)
    plt.plot(evolution)
    plt.show()

def describe_list(lst_name,lst):
    print("====> describe list ", lst_name)
    print("min : ", min(lst))
    print("10% low", numpy.percentile(lst, 10))
    print("med", statistics.median(lst))
    print("10% high", numpy.percentile(lst, 90))
    print("max : ", max(lst))


def get_complete_levels_list(prefix, quantity):
    complete_levels_list = []

    ##open all the files, put in a list
    for current_level_index in range(quantity):
        file = open(prefix + str(current_level_index), 'rb')
        elem = pickle.load(file)
        complete_levels_list.append(elem)
    return complete_levels_list

def describe_bunch_of_levels(prefixes_list, quantity, levels_set_name):

    for grid_size_id in grid_sizes_id:
        prefix=prefixes_list[grid_size_id]
        print('====> Current prefix :', prefix)

        complete_levels_list=get_complete_levels_list(prefix, quantity)

        print("====> Number of levels :  ", len(complete_levels_list))

        # =========================================================================== get stats
        scores, sizes, fitness = [], [], []

        ##open all them files, put in a list
        for data in complete_levels_list:
            data.setFitnessScore()

            scores.append(data.best_score)
            sizes.append(len(data.best_moves))
            fitness.append(data.fitness)

        # =========================================================================== Describe stats in terminal

        describe_list("Scores",scores)
        describe_list("Sizes",sizes)
        describe_list("Fitness",fitness)

        # =========================================================================== Display stats as plots

        plot_all_evolutions(complete_levels_list, levels_set_name + "  - Grid  size : " + str(grid_size_id))

        scores.sort()
        fitness.sort()
        sizes.sort()

        plot_graph(scores, "All final scores" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Final Score")
        plot_graph(fitness, "All fitness" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Fitness Score")
        plot_graph(sizes, "All sizes" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Best Solution Size")

def create_level_file(level, filename):
    temp=open(filename,"wb")
    pickle.dump(level, temp)

def get_index_of_closest_from(to_search, levels_list):
    closest_index=0

    for i in range (len(levels_list)):
        if abs(to_search - levels_list[closest_index].fitness)>abs(to_search - levels_list[i].fitness):
            closest_index=i

    return closest_index

def reduce_levels_set():
    for current_grid_size_id in grid_sizes_id:

        print('====> Current grid size id ',current_grid_size_id)
        print('====> Current grid size id ',current_grid_size_id)

        #=========================================================================== get data
        complete_levels_list=[]

        ##open all the files, put in a list
        for reduced_levels_index in range (raw_levels_to_generate):
            file = open(file_prefixes_raw[current_grid_size_id] + str(reduced_levels_index), 'rb')
            data = pickle.load(file)

            complete_levels_list.append(data)

        print("====>  Initially total of  ",len(complete_levels_list)," levels")

        #=========================================================================== kept levels
        levels_size_acceptable=[]
        lowest_size=lowest_solution_sizes[current_grid_size_id]

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
            index=get_index_of_closest_from(theoretical_fitness[reduced_levels_index], levels_size_acceptable)
            this_one=levels_size_acceptable.pop(index)
            levels_reduced.append(this_one)

        fitness=[]

        levels_reduced.sort()

        for current_level in levels_reduced:
            fitness.append(current_level.fitness)

        print("====> Real Fitness : ",fitness)

        for index_reduced in range (len(levels_reduced)):
            current_level=levels_reduced[index_reduced]
            create_level_file(current_level, file_prefixes_processed[current_grid_size_id] + str(index_reduced))

        print("====>  Keeping ", len(levels_reduced), " levels")

def create_level_file_as_json(l, filename):
    result={
        "operations":l.level.level,
        "bestScore":round(float(l.best_score),2),
        "bestMoves":l.best_moves
    }

    with open(filename, 'w') as file:
        json.dump(result, file, indent=4, separators=(',', ': '), ensure_ascii=False)

def export_all_levels_as_json():
    for difficulty in grid_sizes_id:
        print('====> Current difficulty', difficulty)

        ##open all the files, put in a list
        for final_index_level in range(number_levels_to_keep):
            file = open(file_prefixes_processed[difficulty] + str(final_index_level), 'rb')
            data = pickle.load(file)

            create_level_file_as_json(data, file_prefixes_processed_as_json[difficulty] + str(final_index_level) + ".json")

print("========> step 1: describe complete set of levels")
describe_bunch_of_levels(file_prefixes_raw, raw_levels_to_generate, " Complete")
print("========> step 2: reduce set of levels")
reduce_levels_set()
print("========> step 3: describe reduced set of levels")
describe_bunch_of_levels(file_prefixes_processed, number_levels_to_keep, " Reduced")
print("========> step 4: export as json")
export_all_levels_as_json()