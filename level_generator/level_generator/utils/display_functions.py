import numpy
import statistics
import matplotlib.pyplot as plt

from level_generator.config.config import grid_sizes
from level_generator.utils.file_level_functions import get_complete_levels_list

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

def describe_difficulty_terms(grid_size_id, quantity):
	print('"====> Describe  difficulty terms')
	print('====> Current grid size :', grid_sizes[grid_size_id])

	complete_levels_list = get_complete_levels_list(grid_size_id, quantity)


	# ==== get stats
	first_term_raw, second_term_raw, first_term_normalized, second_term_normalized = [], [], [], []

	for data in complete_levels_list:
		data.set_estimated_difficulty()

		first_term_raw.append(data.first_term_raw)
		second_term_raw.append(data.second_term_raw)
		first_term_normalized.append(data.first_term_normalized)
		second_term_normalized.append(data.second_term_normalized)

	describe_list("Difficulty Term 1 Raw", first_term_raw)
	describe_list("Difficulty Term 2 Raw", second_term_raw)

	describe_list("Difficulty Term 1 Normalized", first_term_normalized)
	describe_list("Difficulty Term 2 Normalized", second_term_normalized)

def describe_given_grid_size(grid_size_id, quantity, levels_set_name):
	print('====> Current grid size :', grid_sizes[grid_size_id])

	complete_levels_list = get_complete_levels_list(grid_size_id, quantity)

	print("====> Number of levels :  ", len(complete_levels_list))

	# ==== get stats
	scores, sizes, estimated_difficulties = [], [], []

	for data in complete_levels_list:
		data.set_estimated_difficulty()

		scores.append(data.best_score)
		sizes.append(len(data.best_moves))
		estimated_difficulties.append(data.estimated_difficulty)

	# ==== Describe stats in terminal
	describe_list("Scores", scores)
	describe_list("Sizes", sizes)
	describe_list("Difficulty", estimated_difficulties)

	# ==== Display stats as plots

	display_multiple_evolution(complete_levels_list, levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]))

	scores.sort()
	estimated_difficulties.sort()
	sizes.sort()

	display_one_evolution(scores, "All final scores" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Final Score")
	display_one_evolution(estimated_difficulties, "All estimated_difficulties" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Difficulty Score")
	display_one_evolution(sizes, "All sizes" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Best Solution Size")
