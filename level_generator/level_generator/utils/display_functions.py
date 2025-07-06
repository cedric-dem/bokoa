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

		list_evolutions = [levels_list[levels_set_index][grid_size_index][level_index].historyOfScoresForBestSolution for level_index in range(len(levels_list[levels_set_index][grid_size_index]))]

		num_curves = len(list_evolutions)

		for idx, current_evolution in enumerate(list_evolutions):
			g = int(255 * (1 - idx / (num_curves - 1)))
			r = int(255 * (idx / (num_curves - 1)))

			axes[levels_set_index].plot(current_evolution, color = f'#{r:02x}{g:02x}{0:02x}')

		axes[levels_set_index].set_title("Evolution of all scores for " + levels_set_names[levels_set_index] + str(grid_sizes[grid_size_index]))

		axes[levels_set_index].set_xlabel("Number of Moves")
		axes[levels_set_index].set_ylabel("Score")

		ymin, _ = axes[levels_set_index].get_ylim()

		axes[levels_set_index].set_ylim(ymin, 1.05 * all_time_max)
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
		axes[levels_set_index].set_ylim(0, 1)

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

			for current_position in range(len(this_level.historyOfScoresForBestSolution)):
				current_value = this_level.historyOfScoresForBestSolution[current_position]

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

	for levels_set_index in range(len(levels_list)):
		axes[levels_set_index].plot(mins_at_each_step[levels_set_index], color = 'red')

		axes[levels_set_index].set_title("Evolution of min score at each move for " + levels_set_names[levels_set_index] + str(grid_sizes[grid_size_index]))

		axes[levels_set_index].set_xlabel("Number of Moves")
		axes[levels_set_index].set_ylabel("Score")

		ymin, _ = axes[levels_set_index].get_ylim()

		axes[levels_set_index].set_ylim(ymin - 10, all_time_max_min * 1.05)
		axes[levels_set_index].set_xlim(0, (grid_sizes[grid_size_index][0] * grid_sizes[grid_size_index][1]))

		axes[levels_set_index].grid(True)
		axes[levels_set_index].yaxis.set_major_formatter(FuncFormatter(get_formatted_integer))

	plt.tight_layout()
	plt.show()
