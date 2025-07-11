from level_generator.classes.level import *
from level_generator.utils.file_level_functions import get_levels_list
import copy
import math

from level_generator.utils.misc_functions import get_amount_of_existing_levels_for_given_grid_size

def get_index_of_closest_difficulty(difficulty_to_search, levels_list):
	closest_index = 0
	closest_distance = float("inf")

	for current_index in range(len(levels_list)):
		this_distance = abs(difficulty_to_search - levels_list[current_index].estimated_difficulty)
		if closest_distance > this_distance:
			closest_index = current_index
			closest_distance = this_distance

	return closest_index

def get_complete_set_levels():
	return get_levels(complete_folder_name)

def get_reduced_set_levels():
	return get_levels(reduced_folder_name)

def get_levels(folder):
	result = [None for _ in range(len(grid_sizes))]

	for current_grid_size_id in range(len(grid_sizes)):
		complete_levels_list = get_levels_list(folder, current_grid_size_id, get_amount_of_existing_levels_for_given_grid_size(folder, current_grid_size_id))
		result[current_grid_size_id] = complete_levels_list

	return result

def is_passing_criteria(current_level, current_grid_size_id, boundaries):
	this_size = len(current_level.best_moves)
	min_size = boundaries["min_size"][current_grid_size_id]
	max_size = boundaries["max_size"][current_grid_size_id]

	this_score = current_level.best_score
	min_score = boundaries["min_score"][current_grid_size_id]
	max_score = boundaries["max_score"][current_grid_size_id]

	return min_size <= this_size <= max_size and min_score <= this_score <= max_score

def remove_out_of_bounds_levels(current_set_of_levels, boundaries):
	print("====> remove out of bounds levels")
	acceptable_levels = [[] for _ in range(len(grid_sizes))]
	for current_grid_size_id in range(len(grid_sizes)):
		print('====> Current grid size : ', current_grid_size_id)
		for current_old_level_index in range(len(current_set_of_levels[current_grid_size_id])):
			current_level = current_set_of_levels[current_grid_size_id][current_old_level_index]

			if is_passing_criteria(current_level, current_grid_size_id, boundaries):
				acceptable_levels[current_grid_size_id].append(current_level)

	return acceptable_levels

def are_levels_exactly_the_same(level_a, level_b):
	found_one_difference = False
	i = 0
	while i < (len(level_a.operations_grid)) and not found_one_difference:
		j = 0
		while j < (len(level_a.operations_grid)) and not found_one_difference:
			if level_a.operations_grid[i][j] != level_b.operations_grid[i][j]:
				found_one_difference = True
			j += 1
		i += 1
	return not found_one_difference

def remove_duplicated(set_of_levels):
	print("====> remove duplicated levels")
	set_without_duplicated = []
	for grid_size_id in range(len(grid_sizes)):
		print('====> Current grid size : ', grid_size_id)
		indexes_to_remove = []
		for level_index_a in range(len(set_of_levels[grid_size_id])):
			for level_index_b in range(len(set_of_levels[grid_size_id])):
				if level_index_a != level_index_b:  # Not itself
					score_a = set_of_levels[grid_size_id][level_index_a].best_score
					score_b = set_of_levels[grid_size_id][level_index_b].best_score
					if abs(score_a - score_b) < 0.1:  # worth trying to verify
						if are_levels_exactly_the_same(set_of_levels[grid_size_id][level_index_a], set_of_levels[grid_size_id][level_index_b]):
							indexes_to_remove.append(level_index_a)

		if len(indexes_to_remove) > 0:
			print("Found " + str(len(indexes_to_remove)) + " duplicated  in grid size ", grid_sizes[grid_size_id], " index ", indexes_to_remove)
		else:
			print("Did not found duplicated levels in grid size ", grid_sizes[grid_size_id])

		set_without_duplicated.append([level for current_level_index, level in enumerate(set_of_levels[grid_size_id]) if current_level_index not in indexes_to_remove])
	return set_without_duplicated

def set_difficulty_for_all_levels(initial_set_of_levels, constants):
	for current_grid_size_id in range(len(grid_sizes)):
		for level_index in range(len(initial_set_of_levels[current_grid_size_id])):
			initial_set_of_levels[current_grid_size_id][level_index].set_estimated_difficulty(constants)

def reduce_levels_set(acceptable_levels):
	reduced_to_final_set = [[] for _ in range(len(grid_sizes))]

	for current_grid_size_id in range(len(grid_sizes)):
		print('====> Current grid size id ', current_grid_size_id)

		if number_levels_to_keep > len(acceptable_levels[current_grid_size_id]):
			raise ValueError("More reduced levels wanted(", number_levels_to_keep, ")", " than available (", len(acceptable_levels[current_grid_size_id]), ")")

		# ==== get theoretical estimated_difficulties to reduce
		theoretical_difficulties = get_theoretical_difficulties(acceptable_levels[current_grid_size_id], True)

		# approach theoretical difficulties
		reduced_to_final_set[current_grid_size_id] = get_levels_approaching_theoretical_difficulties(theoretical_difficulties, copy.deepcopy(acceptable_levels[current_grid_size_id]))

		display_all_estimated_difficulties(reduced_to_final_set[current_grid_size_id])

	return reduced_to_final_set

def display_all_estimated_difficulties(lst_levels):
	estimated_difficulties = [current_level.estimated_difficulty for current_level in lst_levels]

	print("====> Real Difficulties : ", estimated_difficulties)

def get_levels_approaching_theoretical_difficulties(theoretical_difficulties, acceptable_levels):
	levels_reduced = []

	for reduced_levels_index in range(number_levels_to_keep):
		index = get_index_of_closest_difficulty(theoretical_difficulties[reduced_levels_index], acceptable_levels)
		this_one = acceptable_levels.pop(index)
		levels_reduced.append(this_one)
	levels_reduced.sort()
	return levels_reduced

def get_theoretical_difficulties(levels_list, verbose):  # hypothesis : levels list already sorted
	theoretical_difficulties = []

	initial_difficulty = levels_list[0].estimated_difficulty
	end_difficulty = levels_list[-1].estimated_difficulty

	match difficulty_setting:
		case "linear":
			average_step = (end_difficulty - initial_difficulty) / number_levels_to_keep

			for reduced_levels_index in range(number_levels_to_keep):
				theoretical_difficulties.append(round(initial_difficulty + (reduced_levels_index * average_step), 6))

			if verbose:
				print('====> Linear difficulty, average step', average_step)

		case "logarithmic":
			delta_y = end_difficulty - initial_difficulty

			base = 10

			a = 1 / (base ** delta_y - 1)
			c = initial_difficulty - math.log(a) / math.log(base)

			for reduced_levels_index in range(number_levels_to_keep):
				x = reduced_levels_index / number_levels_to_keep
				theoretical_difficulties.append(round(math.log(a + x, base) + c, 6))

			if verbose:
				print('====> log difficulty, settings ', a, c)
	if verbose:
		print("====> Theoretical difficulties : ", theoretical_difficulties)
	return theoretical_difficulties
