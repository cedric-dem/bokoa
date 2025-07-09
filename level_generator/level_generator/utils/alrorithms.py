from level_generator.config.config import grid_sizes

def evaluate_algorithm_performance(name, levels_set):
	print('====> Evaluate algorithm: ', name)

	performance = []
	for grid_size_index in range(len(levels_set)):
		reached_goal = 0
		print("==> on grid size ", grid_sizes[grid_size_index], " levels quantity : ", len(levels_set[grid_size_index]))
		for level_index in range(len(levels_set[grid_size_index])):
			reached_score = get_score_of_a_given_level_solved_using_given_algorithm(name, levels_set[grid_size_index][level_index])
			# print("=> level", level_index, " goal ", levels_set[grid_size_index][level_index].best_score, "reached : ", reached_score)

			if abs(reached_score - reached_goal) < 0.01:
				reached_goal += 1
		performance.append(round(reached_goal / len(levels_set[grid_size_index]), 2))

	print('==> Performance : ', performance)

def get_score_of_a_given_level_solved_using_given_algorithm(name, level):
	# TOD
	return 0
