import numpy
import statistics
import matplotlib.pyplot as plt

from level_generator.config.config import grid_sizes
from level_generator.utils.misc import get_complete_levels_list

def plot_all_evolutions(list_evolutions, context_name):
	plt.title("All evolution" + context_name)
	for elem in list_evolutions:
		plt.plot(elem.historyOfScoresForBestSolution)

	plt.xlabel("Number Of Moves")
	plt.ylabel("Score")
	plt.show()

def plot_graph(evolution, plot_name, x_labels, y_labels):
	plt.title(plot_name)
	plt.xlabel(x_labels)
	plt.ylabel(y_labels)
	plt.plot(evolution)
	plt.show()

def describe_list(lst_name, lst):
	print("====> describe list ", lst_name)
	print(
		"minimum : ", round(min(lst), 2), " ; ",
		"10% low : ", round(numpy.percentile(lst, 10), 2), " ; ",
		"median : ", round(statistics.median(lst), 2), " ; ",
		"10% high : ", round(numpy.percentile(lst, 90), 2), " ; ",
		"maximum : ", round(max(lst), 2)
	)

def describe_given_grid_size(grid_size_id, prefix, quantity, levels_set_name):
	print('====> Current prefix :', prefix)

	complete_levels_list = get_complete_levels_list(grid_size_id, prefix, quantity)

	print("====> Number of levels :  ", len(complete_levels_list))

	# ==== get stats
	scores, sizes, fitness = [], [], []

	for data in complete_levels_list:
		data.set_fitness_score()

		scores.append(data.best_score)
		sizes.append(len(data.best_moves))
		fitness.append(data.estimated_difficulty)

	# ==== Describe stats in terminal
	describe_list("Scores", scores)
	describe_list("Sizes", sizes)
	describe_list("Fitness", fitness)

	# ==== Display stats as plots

	plot_all_evolutions(complete_levels_list, levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]))

	scores.sort()
	fitness.sort()
	sizes.sort()

	plot_graph(scores, "All final scores" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Final Score")
	plot_graph(fitness, "All fitness" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Fitness Score")
	plot_graph(sizes, "All sizes" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Best Solution Size")
