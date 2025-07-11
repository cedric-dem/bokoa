import numpy
import statistics
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter
from level_generator.config.config import grid_sizes
from level_generator.utils.reduce_levels_functions import get_theoretical_difficulties

def plot_levels_sets_statistics(levels_list, levels_set_names):
	print('\n=> Plot Difficulties <========')
	for current_grid_index in range(len(grid_sizes)):
		plot_levels_sets_difficulty_for_grid(levels_list, levels_set_names, current_grid_index)

	print('\n=> Plot Sizes <========')
	for current_grid_index in range(len(grid_sizes)):
		plot_levels_sets_sizes_for_grid(levels_list, levels_set_names, current_grid_index)

	print('\n=> Plot Scores <========')
	for current_grid_index in range(len(grid_sizes)):
		plot_levels_sets_scores_for_grid(levels_list, levels_set_names, current_grid_index)

	print('\n=> Plot Evolutions <========')
	for current_grid_index in range(len(grid_sizes)):
		plot_levels_sets_evolution_for_grid(levels_list, levels_set_names, current_grid_index)

	print('\n=> Plot Min Values At Each Move <========')
	for current_grid_index in range(len(grid_sizes)):
		plot_min_values_at_each_move(levels_list, levels_set_names, current_grid_index)

def describe_list(lst_name, lst):
	print("====> describe list ", lst_name)
	print(
		"minimum : ", round(min(lst), 2), " ; ",
		"10% low : ", round(numpy.percentile(lst, 10), 2), " ; ",
		"median : ", round(statistics.median(lst), 2), " ; ",
		"10% high : ", round(numpy.percentile(lst, 90), 2), " ; ",
		"maximum : ", round(max(lst), 2)
	)

def describe_levels_set_terminal(levels_list, levels_set_name):
	print("====> Describe levels set terminal ", levels_set_name)
	for current_grid_size_id in range(len(grid_sizes)):
		print("====> current grid size :  ", grid_sizes[current_grid_size_id])
		print("====> Number of levels :  ", len(levels_list[current_grid_size_id]))

		scores, sizes, estimated_difficulties = [], [], []
		for data in levels_list[current_grid_size_id]:
			scores.append(data.best_score)
			sizes.append(len(data.best_moves))
			estimated_difficulties.append(data.estimated_difficulty)

		describe_list("Scores", scores)
		describe_list("Sizes", sizes)
		describe_list("Difficulty", estimated_difficulties)
		print()

def plot_levels_sets_scores_for_grid(levels_list, levels_set_names, grid_size_index):
	scores = [[] for _ in range(len(levels_list))]

	for level_set_index in range(len(levels_list)):
		for current_level_index in range(len(levels_list[level_set_index][grid_size_index])):
			current_level = levels_list[level_set_index][grid_size_index][current_level_index]

			# scores[level_set_index].append(math.log(current_level.best_score))
			scores[level_set_index].append(current_level.best_score)

	print('==> Plot grid size', grid_sizes[grid_size_index])
	display_plot_box(scores, " Scores", str(grid_sizes[grid_size_index]), levels_set_names)

def plot_levels_sets_sizes_for_grid(levels_list, levels_set_names, grid_size_index):
	sizes = [[] for _ in range(len(levels_list))]

	for level_set_index in range(len(levels_list)):
		for current_level_index in range(len(levels_list[level_set_index][grid_size_index])):
			current_level = levels_list[level_set_index][grid_size_index][current_level_index]
			sizes[level_set_index].append(len(current_level.best_moves))

	print('==> Plot grid size', grid_sizes[grid_size_index])
	display_plot_box(sizes, " Sizes ", str(grid_sizes[grid_size_index]), levels_set_names)

def display_plot_box(data, name, grid_size, levels_set_names):
	print("===> now displaying ", name, " for grid size ", grid_size, " number of levels :", str([len(i) for i in data]))

	box = plt.boxplot(data, patch_artist = True, labels = levels_set_names)

	plt.title("Comparing 3 Levels Sets For " + name + "for grid size " + str(grid_size))
	plt.xlabel("Level Set")
	plt.ylabel(name)
	plt.grid(True)

	formatter = ticker.FuncFormatter(get_formatted_integer)
	plt.gca().yaxis.set_major_formatter(formatter)

	colors = ['blue', 'red', 'green']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)
	plt.legend([box["boxes"][0], box["boxes"][1], box["boxes"][2]], levels_set_names, loc = "upper left")

	plt.show()

def get_formatted_integer(x, pos):
	return f'{int(x):,}'.replace(',', ' ')

def get_all_time_max(levels_list, grid_size_index):
	all_time_max = float('-inf')
	for levels_set_index in range(len(levels_list)):
		max_scores = [levels_list[levels_set_index][grid_size_index][level_index].best_score for level_index in range(len(levels_list[levels_set_index][grid_size_index]))]
		all_time_max = max(all_time_max, max(max_scores))
	return all_time_max

def plot_levels_sets_evolution_for_grid(levels_list, levels_set_names, grid_size_index):
	fig, axes = plt.subplots(1, len(levels_list), figsize = (15, 5))

	print('==> plot evolution for grid size ', grid_sizes[grid_size_index], "number of levels :", str([len(elem[grid_size_index]) for elem in levels_list]))

	all_time_max = get_all_time_max(levels_list, grid_size_index)

	for levels_set_index in range(len(levels_list)):

		list_evolutions = [levels_list[levels_set_index][grid_size_index][level_index].history_of_scores_for_best_solution for level_index in range(len(levels_list[levels_set_index][grid_size_index]))]

		num_curves = len(list_evolutions)

		for idx, current_evolution in enumerate(list_evolutions):
			g = int(255 * (1 - idx / (num_curves - 1)))
			r = int(255 * (idx / (num_curves - 1)))

			axes[levels_set_index].plot(current_evolution, color = f'#{r:02x}{g:02x}{0:02x}')

		axes[levels_set_index].set_title("Evolution of all scores for " + levels_set_names[levels_set_index] + str(grid_sizes[grid_size_index]))

		axes[levels_set_index].set_xlabel("Number of Moves")
		axes[levels_set_index].set_ylabel("Score")

		min_value_y, _ = axes[levels_set_index].get_ylim()

		axes[levels_set_index].set_ylim(min_value_y, 1.05 * all_time_max)
		axes[levels_set_index].set_xlim(0, (grid_sizes[grid_size_index][0] * grid_sizes[grid_size_index][1]))

		axes[levels_set_index].grid(True)
		axes[levels_set_index].yaxis.set_major_formatter(FuncFormatter(get_formatted_integer))

	plt.tight_layout()
	plt.show()

def plot_levels_sets_difficulty_for_grid(levels_list, levels_set_names, grid_size_index):
	fig, axes = plt.subplots(1, len(levels_list), figsize = (15, 5))

	print('==> plot difficulty for grid size ', grid_sizes[grid_size_index], "number of levels :", str([len(elem[grid_size_index]) for elem in levels_list]))

	ideal_diff = get_theoretical_difficulties(levels_list[2][grid_size_index], False)
	axes[2].plot(ideal_diff, label = "Theoretical Difficulty", color = "green")

	for levels_set_index in range(len(levels_list)):
		estimated_difficulties = [levels_list[levels_set_index][grid_size_index][level_index].estimated_difficulty for level_index in range(len(levels_list[levels_set_index][grid_size_index]))]

		axes[levels_set_index].plot(estimated_difficulties, label = "Estimated Difficulty", color = "red")
		axes[levels_set_index].set_title("Evolution of difficulty for " + levels_set_names[levels_set_index] + str(grid_sizes[grid_size_index]))

		axes[levels_set_index].set_xlabel("Level ID")
		axes[levels_set_index].set_ylabel("Estimated Difficulty")
		#axes[levels_set_index].set_ylim(-0.1, 1.1)

		axes[levels_set_index].legend()
		axes[levels_set_index].grid(True)

	plt.tight_layout()
	plt.show()

def get_mins_at_each_step(levels_list, grid_size_index):
	result = []

	for levels_set_index in range(len(levels_list)):
		current_mins_list = []
		for level_index in range(len(levels_list[levels_set_index][grid_size_index])):
			this_level = levels_list[levels_set_index][grid_size_index][level_index]

			for current_position in range(len(this_level.history_of_scores_for_best_solution)):
				current_value = this_level.history_of_scores_for_best_solution[current_position]

				if current_position >= len(current_mins_list):
					current_mins_list.append(current_value)
				else:
					current_mins_list[current_position] = min(current_mins_list[current_position], current_value)

		result.append(current_mins_list)

	return result

def plot_min_values_at_each_move(levels_list, levels_set_names, grid_size_index):
	fig, axes = plt.subplots(1, len(levels_list), figsize = (15, 5))

	print('==> plot min score at each move for grid size ', grid_sizes[grid_size_index], "number of levels :", str([len(elem[grid_size_index]) for elem in levels_list]))

	mins_at_each_step = get_mins_at_each_step(levels_list, grid_size_index)

	all_time_max_min = max([mins_at_each_step[i][-1] for i in range(len(mins_at_each_step))])
	print("==> All time min max : ", all_time_max_min)

	approximation_lower_bound_function = get_approx_function(grid_size_index)
	axes[0].plot(approximation_lower_bound_function, label = "Lower Bound Estimation", color = "green")

	for levels_set_index in range(len(levels_list)):
		axes[levels_set_index].plot(mins_at_each_step[levels_set_index], color = 'red')

		axes[levels_set_index].set_title("Evolution of min score at each move for " + levels_set_names[levels_set_index] + str(grid_sizes[grid_size_index]))

		axes[levels_set_index].set_xlabel("Number of Moves")
		axes[levels_set_index].set_ylabel("Score")

		min_value_y, _ = axes[levels_set_index].get_ylim()

		axes[levels_set_index].set_ylim(min_value_y - 10, all_time_max_min * 1.05)
		axes[levels_set_index].set_xlim(0, (grid_sizes[grid_size_index][0] * grid_sizes[grid_size_index][1]))

		axes[levels_set_index].grid(True)
		axes[levels_set_index].yaxis.set_major_formatter(FuncFormatter(get_formatted_integer))

	plt.tight_layout()
	plt.show()

def get_approx_function(grid_size_index):
	size_wanted = grid_sizes[grid_size_index][0] * grid_sizes[grid_size_index][1]
	match grid_size_index:
		case 0:
			result = [1, -4, -6.68, -10.63, -14.38, -14.32, -13.92, -13.4, -10.77, -6.44, -3.93, -1.22, 4.36, 10.21, 20.733, 83.66]
		case 1:
			result = [1, -4, -17.4, -20.4, -22.2, -22.4, -18.6, -13.4, -11.97, -11.13, -8.09, -5.66, -3.5, -2.07, 0.15, 1.41, 5.23, 8.11, 23.28, 69.86, 251.61, 655.41, 1574.68, 2037.2000000000003, 6111.6]
		case 2:
			result = [1, -4, -10.4, -12.6, -14.0, -12.6, -10.68, -9.28, -8.46, -7.31, -8.85, -7.4, -6.51, -5.43, -4.41, -0.87, -0.08, 0.78, 2.25, 2.82, 2.7, 3.82, 9.86, 18.17, 56.28, 93.67, 237.07, 374.96, 940.12, 1647.26, 3333.68, 4912.09, 5983.26, 8615.449999999999, 43077.24999999999]
		case _:
			raise ValueError("Invalid grid size index : ", grid_size_index)
	return result

def display_performance_time_heuristic(dict_time, dict_perf):
	for grid_size_index in range(len(grid_sizes)):
		this_grid_size_list_times = []
		this_grid_size_list_accuracy = []
		list_heuristic_names = []
		for heuristic_setting in dict_time:
			this_grid_size_list_times.append(dict_time[heuristic_setting][grid_size_index])
			this_grid_size_list_accuracy.append(dict_perf[heuristic_setting][grid_size_index])
			list_heuristic_names.append(heuristic_setting)

		plt.scatter(this_grid_size_list_times, this_grid_size_list_accuracy)

		for current_heuristic_index in range(len(this_grid_size_list_times)):
			plt.text(this_grid_size_list_times[current_heuristic_index], this_grid_size_list_accuracy[current_heuristic_index], list_heuristic_names[current_heuristic_index], fontsize = 9)

		plt.xlabel("Time per level")
		plt.ylabel("Accuracy")
		plt.title("Performance VS Time of each heuristic for grid size" + str(grid_sizes[grid_size_index]))

		plt.grid(True)
		plt.show()

def plot_performance_of_each_solver(set_of_levels, heuristics_list):
	for current_heuristic in heuristics_list:
		fig, axes = plt.subplots(1, len(set_of_levels), figsize = (15, 5))

		for grid_size_index in range(len(set_of_levels)):
			this_evolution = []
			for level_index in range(len(set_of_levels[grid_size_index])):
				if set_of_levels[grid_size_index][level_index].predictions_of_heuristics[current_heuristic]:
					this_evolution.append(1)
				else:
					this_evolution.append(0)

			# print("==> number levels : ", len(this_evolution))
			axes[grid_size_index].plot(this_evolution, color = 'red')

			axes[grid_size_index].set_title("Scores predicted for  grid size " + str(grid_sizes[grid_size_index]) + "heuristic " + current_heuristic)

			axes[grid_size_index].set_ylim(-0.1, 1.1)
			axes[grid_size_index].set_xlabel("Level Id")
			axes[grid_size_index].set_ylabel("Found Solution")

			axes[grid_size_index].grid(True)

		plt.tight_layout()
		plt.show()

def plot_quantity_predictor_passing_each_levels(set_of_levels, list_heuristics_str):
	fig, axes = plt.subplots(1, len(set_of_levels), figsize = (15, 5))
	for grid_size_index in range(len(set_of_levels)):

		this_evolution = []
		for level_index in range(len(set_of_levels[grid_size_index])):
			this_passed = 0
			for current_heuristic in list_heuristics_str:
				if set_of_levels[grid_size_index][level_index].predictions_of_heuristics[current_heuristic]:
					this_passed += 1
			this_evolution.append(this_passed)

		axes[grid_size_index].plot(this_evolution, color = 'red')

		axes[grid_size_index].set_title("Nb of predictors predicted each levels of grid size  " + str(grid_sizes[grid_size_index]))

		axes[grid_size_index].set_ylim(-0.1, len(list_heuristics_str) + 0.1)
		axes[grid_size_index].set_xlabel("Level Id")
		axes[grid_size_index].set_ylabel("Nb of Predictors predicted good")

		axes[grid_size_index].grid(True)

	plt.tight_layout()
	plt.show()
