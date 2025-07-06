import numpy
import statistics
import matplotlib.pyplot as plt

from level_generator.config.config import grid_sizes

def display_multiple_evolution(list_evolutions, context_name):
	plt.title("All evolution" + context_name)
	for elem in list_evolutions:
		plt.plot(elem.historyOfScoresForBestSolution)

	plt.xlabel("Number Of Moves")
	plt.ylabel("Score")
	plt.show()

def display_one_evolution(evolution, plot_name, x_labels, y_labels):
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

def describe_all_grid_sizes(levels_list, levels_set_name):
	for grid_size_id in range(len(grid_sizes)):
		describe_given_grid_size(levels_list[grid_size_id], grid_size_id, levels_set_name)

def describe_given_grid_size(levels_list, grid_size_id, levels_set_name):
	print('====> Current grid size :', grid_sizes[grid_size_id])

	print("====> Number of levels :  ", len(levels_list))

	# ==== get stats
	scores, sizes, estimated_difficulties = [], [], []

	for data in levels_list:
		scores.append(data.best_score)
		sizes.append(len(data.best_moves))
		estimated_difficulties.append(data.estimated_difficulty)

	# ==== Describe stats in terminal
	describe_list("Scores", scores)
	describe_list("Sizes", sizes)
	describe_list("Difficulty", estimated_difficulties)

	# ==== Display stats as plots

	display_multiple_evolution(levels_list, levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]))

	scores.sort()
	estimated_difficulties.sort()
	sizes.sort()

	display_one_evolution(scores, "All final scores" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Final Score")
	display_one_evolution(estimated_difficulties, "All estimated_difficulties" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Difficulty Score")
	display_one_evolution(sizes, "All sizes" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Best Solution Size")


def describe_levels_set_terminal(levels_list, levels_set_name):
	pass

def plot_levels_sets_statistics(levels_list, levels_set_names):
	pass