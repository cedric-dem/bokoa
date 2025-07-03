import numpy
import statistics
import matplotlib.pyplot as plt
from misc import *
from levelWithSolution import *
from level import *

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

def get_complete_levels_list(grid_size_id, prefix, quantity):
	complete_levels_list = []

	for current_level_index in range(quantity):
		# load json :
		with open(prefix + str(current_level_index) + ".json", 'r', encoding = 'utf-8') as file:
			data = json.load(file)

			new_level = Level(grid_size_id, data["operations"])
			new_level_with_sol = LevelWithSolution(new_level, data["bestScore"], data["bestMoves"])
			complete_levels_list.append(new_level_with_sol)

	return complete_levels_list

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

def create_level_file(level, filename):
	create_level_file_as_json(level.operations_grid.operations_grid, level.best_score, level.best_moves, filename + ".json")

def get_index_of_closest_from(to_search, levels_list):
	closest_index = 0
	closest_distance = float("inf")

	for current_index in range(len(levels_list)):
		this_distance = abs(to_search - levels_list[current_index].estimated_difficulty)
		if closest_distance > this_distance:
			closest_index = current_index
			closest_distance = this_distance

	return closest_index

def get_levels_size_acceptable(complete_levels_list, current_grid_size_id):
	levels_size_acceptable = []
	lowest_size = lowest_solution_sizes[current_grid_size_id]

	for current_level in complete_levels_list:
		if len(current_level.best_moves) >= lowest_size:
			levels_size_acceptable.append(current_level)
	return levels_size_acceptable

def reduce_levels_set():
	for current_grid_size_id in grid_sizes_id:
		reduce_levels_set_given_grid_size_id(current_grid_size_id)

def reduce_levels_set_given_grid_size_id(current_grid_size_id):
	print('====> Current grid size id ', current_grid_size_id)

	complete_levels_list = get_complete_levels_list(current_grid_size_id, get_file_prefix_complete(current_grid_size_id), raw_levels_to_generate)
	print("====>  Initially total of  ", len(complete_levels_list), " levels")

	levels_size_acceptable = get_levels_size_acceptable(complete_levels_list, current_grid_size_id)
	print("====>  After remove too small levels total of  ", len(levels_size_acceptable), " levels")

	# ===== set fitness of kept levels
	for current_level in levels_size_acceptable:
		current_level.set_fitness_score()

	# ====  sort kept levels
	levels_size_acceptable.sort()

	# ==== Display infos

	fitness = []
	for current_level in levels_size_acceptable:
		fitness.append(current_level.estimated_difficulty)

	# ==== get theoretical fitness to reduce
	theoretical_fitness = get_theoretical_fitness(levels_size_acceptable)

	levels_reduced = get_reduced_levels(theoretical_fitness, levels_size_acceptable)

	fitness = [current_level.estimated_difficulty for current_level in levels_reduced]
	print("====> Real Fitness : ", fitness)

	for index_reduced in range(len(levels_reduced)):
		current_level = levels_reduced[index_reduced]

		create_level_file_as_json(
			current_level.level.operations_grid,
			current_level.best_score,
			current_level.best_moves,
			get_file_prefix_reduced(current_grid_size_id) + str(index_reduced) + ".json"
		)

	print("====>  Keeping ", len(levels_reduced), " levels")

def get_reduced_levels(theoretical_fitness, levels_size_acceptable):
	levels_reduced = []

	for reduced_levels_index in range(number_levels_to_keep):
		index = get_index_of_closest_from(theoretical_fitness[reduced_levels_index], levels_size_acceptable)
		this_one = levels_size_acceptable.pop(index)
		levels_reduced.append(this_one)
	levels_reduced.sort()
	return levels_reduced

def get_theoretical_fitness(levels_list):
	theoretical_fitness = []

	average_step = (levels_list[-1].estimated_difficulty - levels_list[0].estimated_difficulty) / number_levels_to_keep

	current = levels_list[0].estimated_difficulty

	for reduced_levels_index in range(number_levels_to_keep):
		theoretical_fitness.append(current)
		current += average_step

	print('====> Average step', average_step)
	print("====> Theoretical fitness : ", theoretical_fitness)
	return theoretical_fitness

print("========> step 1: describe complete set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(grid_size_id, get_file_prefix_complete(grid_size_id), raw_levels_to_generate, " Complete")

print("========> step 2: reduce set of levels")
reduce_levels_set()

print("========> step 3: describe reduced set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(grid_size_id, get_file_prefix_reduced(grid_size_id), number_levels_to_keep, " Reduced")
