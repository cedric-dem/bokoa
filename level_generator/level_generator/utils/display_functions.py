import numpy
import statistics
import matplotlib.pyplot as plt

from level_generator.config.config import grid_sizes
from level_generator.utils.reduce_levels_functions import get_theoretical_difficulties

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

######################################################

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

def plot_levels_sets_statistics(levels_list, levels_set_names):
	print('\n=> Plot Sizes and scores <========')
	for current_grid_index in range(len(grid_sizes)):
		plot_levels_sets_sizes_scores_for_grid(levels_list, levels_set_names, current_grid_index)

	print('\n=> Plot Evolutions <========')
	for current_grid_index in range(len(grid_sizes)):
		plot_levels_sets_evolution_for_grid(levels_list, levels_set_names, current_grid_index)

	print('\n=> Plot Difficulties <========')
	for current_grid_index in range(len(grid_sizes)):
		plot_levels_sets_difficulty_for_grid(levels_list, levels_set_names, current_grid_index)

def plot_levels_sets_sizes_scores_for_grid(levels_list, levels_set_names, grid_size_index):
	sizes = [[] for _ in range(len(levels_list))]
	scores = [[] for _ in range(len(levels_list))]

	for level_set_index in range(len(levels_list)):
		for current_level_index in range(len(levels_list[level_set_index][grid_size_index])):
			current_level = levels_list[level_set_index][grid_size_index][current_level_index]

			sizes[level_set_index].append(len(current_level.best_moves))

			# scores[level_set_index].append(math.log(current_level.best_score))
			scores[level_set_index].append(current_level.best_score)

	print('==> Plot grid size', grid_sizes[grid_size_index])
	display_plot_box(sizes, " Sizes ", str(grid_sizes[grid_size_index]), levels_set_names)
	display_plot_box(scores, " Scores", str(grid_sizes[grid_size_index]), levels_set_names)

def display_plot_box(data, name, grid_size, levels_set_names):
	print("===> now displaying ", name, " for grid size ", grid_size, " number of levels :", str([len(i) for i in data]))

	box = plt.boxplot(data, patch_artist = True, labels = levels_set_names)

	plt.title("Comparing 3 Levels Sets For " + name + "for grid size " + str(grid_size))
	plt.xlabel("Level Set")
	plt.ylabel(name)
	plt.grid(True)

	colors = ['yellow', 'orange', 'green']
	for patch, color in zip(box['boxes'], colors):
		patch.set_facecolor(color)
	plt.legend([box["boxes"][0], box["boxes"][1], box["boxes"][2]], levels_set_names, loc = "upper left")

	plt.show()

def plot_levels_sets_evolution_for_grid(levels_list, levels_set_names, grid_size_index):
	fig, axes = plt.subplots(1, len(levels_list), figsize = (15, 5))

	print('==> plot evolution for grid size ', grid_sizes[grid_size_index], "number of levels :", str([len(elem[grid_size_index]) for elem in levels_list]))

	for levels_set_index in range(3):

		list_evolutions = [levels_list[levels_set_index][grid_size_index][level_index].historyOfScoresForBestSolution for level_index in range(len(levels_list[levels_set_index][grid_size_index]))]

		num_curves = len(list_evolutions)

		for idx, current_evolution in enumerate(list_evolutions):
			r = int(255 * (1 - idx / (num_curves - 1)))
			g = int(255 * (idx / (num_curves - 1)))

			axes[levels_set_index].plot(current_evolution, color = f'#{r:02x}{g:02x}{0:02x}')

		axes[levels_set_index].set_title("Evolution of all scores for " + levels_set_names[levels_set_index] + str(grid_sizes[grid_size_index]))

	plt.tight_layout()
	plt.show()

def plot_levels_sets_difficulty_for_grid(levels_list, levels_set_names, grid_size_index):
	fig, axes = plt.subplots(1, len(levels_list), figsize = (15, 5))

	print('==> plot difficulty for grid size ', grid_sizes[grid_size_index], "number of levels :", str([len(elem[grid_size_index]) for elem in levels_list]))

	ideal_diff = get_theoretical_difficulties(levels_list[2][grid_size_index], False)
	axes[2].plot(ideal_diff, label = "Theoretical Difficulty")

	for levels_set_index in range(3):
		estimated_difficulties = [levels_list[levels_set_index][grid_size_index][level_index].estimated_difficulty for level_index in range(len(levels_list[levels_set_index][grid_size_index]))]

		axes[levels_set_index].plot(estimated_difficulties, label = "Estimated Difficulty")
		axes[levels_set_index].set_title("Evolution of difficulty for " + levels_set_names[levels_set_index] + str(grid_sizes[grid_size_index]))

		axes[levels_set_index].set_xlabel("Level ID")
		axes[levels_set_index].set_ylabel("Estimated Difficulty")
		axes[levels_set_index].set_ylim(0, 1)

		axes[levels_set_index].legend()

	plt.tight_layout()
	plt.show()
