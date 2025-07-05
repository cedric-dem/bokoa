from level_generator.classes.level import *
from level_generator.utils.file_level_functions import get_levels_list
import copy

def get_index_of_closest_difficulty(difficulty_to_search, levels_list):
	closest_index = 0
	closest_distance = float("inf")

	for current_index in range(len(levels_list)):
		this_distance = abs(difficulty_to_search - levels_list[current_index].estimated_difficulty)
		if closest_distance > this_distance:
			closest_index = current_index
			closest_distance = this_distance

	return closest_index

def get_all_levels():
	result = [None for _ in range(len(grid_sizes))]

	for current_grid_size_id in range(len(grid_sizes)):
		complete_levels_list = get_levels_list(complete_folder_name, current_grid_size_id, raw_levels_to_generate)
		result[current_grid_size_id] = complete_levels_list

	return result

def is_passing_criterias(current_level, current_grid_size_id, boundaries):
	this_size = len(current_level.best_moves)
	min_size = boundaries["min_size"][current_grid_size_id]
	max_size = boundaries["max_size"][current_grid_size_id]

	this_score = current_level.best_score
	min_score = boundaries["min_score"][current_grid_size_id]
	max_score = boundaries["max_score"][current_grid_size_id]

	return this_size >= min_size and this_size <= max_size and this_score >= min_score and this_score <= max_score

def remove_out_of_bounds_levels(current_set_of_levels, boundaries):
	acceptable_levels = [[] for _ in range(len(grid_sizes))]
	for current_grid_size_id in range(len(grid_sizes)):
		print('====> Current grid size : ', current_grid_size_id)
		for current_old_level_index in range(len(current_set_of_levels[current_grid_size_id])):
			current_level = current_set_of_levels[current_grid_size_id][current_old_level_index]

			if is_passing_criterias(current_level, current_grid_size_id, boundaries):
				acceptable_levels[current_grid_size_id].append(current_level)

	return acceptable_levels

def set_difficulty_for_all_levels(initial_set_of_levels, constants):
	for current_grid_size_id in range(len(grid_sizes)):
		for level_index in range(len(initial_set_of_levels[current_grid_size_id])):
			initial_set_of_levels[current_grid_size_id][level_index].set_estimated_difficulty(constants)

def reduce_levels_set(acceptable_levels):
	reduced_to_final_set = [[] for _ in range(len(grid_sizes))]

	for current_grid_size_id in grid_sizes_id:
		print('====> Current grid size id ', current_grid_size_id)

		# ====  sort kept levels
		acceptable_levels[current_grid_size_id].sort()

		# ==== Display infos

		estimated_difficulties = []
		for current_level in acceptable_levels[current_grid_size_id]:
			estimated_difficulties.append(current_level.estimated_difficulty)

		# ==== get theoretical estimated_difficulties to reduce
		theoretical_difficulties = get_theoretical_difficulties(acceptable_levels[current_grid_size_id], True)

		levels_reduced = get_reduced_levels(theoretical_difficulties, copy.deepcopy(acceptable_levels[current_grid_size_id]))

		estimated_difficulties = [current_level.estimated_difficulty for current_level in levels_reduced]
		print("====> Real Difficulties : ", estimated_difficulties)

		for index_reduced in range(len(levels_reduced)):
			current_level = levels_reduced[index_reduced]
			reduced_to_final_set[current_grid_size_id].append(current_level)
	return reduced_to_final_set

def get_reduced_levels(theoretical_difficulties, levels_size_acceptable):
	levels_reduced = []

	for reduced_levels_index in range(number_levels_to_keep):
		index = get_index_of_closest_difficulty(theoretical_difficulties[reduced_levels_index], levels_size_acceptable)
		this_one = levels_size_acceptable.pop(index)
		levels_reduced.append(this_one)
	levels_reduced.sort()
	return levels_reduced

def get_theoretical_difficulties(levels_list, verbose):
	theoretical_difficulties = []

	average_step = (levels_list[-1].estimated_difficulty - levels_list[0].estimated_difficulty) / number_levels_to_keep

	current = levels_list[0].estimated_difficulty

	for reduced_levels_index in range(number_levels_to_keep):
		theoretical_difficulties.append(current)
		current += average_step

	if verbose:
		print('====> Average step', average_step)
		print("====> Theoretical difficulties : ", theoretical_difficulties)
	return theoretical_difficulties
