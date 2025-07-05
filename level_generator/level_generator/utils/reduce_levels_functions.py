from level_generator.classes.level import *
from level_generator.utils.file_level_functions import get_levels_list, create_level_file_as_json, get_level_path_reduced

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
	result=[None for _ in range (len(grid_sizes))]

	for current_grid_size_id in range(len(grid_sizes)):
		complete_levels_list = get_levels_list(complete_folder_name, current_grid_size_id, raw_levels_to_generate)
		result[current_grid_size_id] = complete_levels_list

	return result


def remove_unacceptable_sizes(current_set_of_levels):

	levels_size_acceptable = [None for i in range (len(grid_sizes))]\

	for current_grid_size_id in range (len(grid_sizes)):
		print('====> Current grid size : ',current_grid_size_id)
		levels_size_acceptable[current_grid_size_id] = get_levels_size_acceptable(current_set_of_levels[current_grid_size_id], current_grid_size_id)
		print("====>  After remove too small levels total of  ", len(levels_size_acceptable), " levels")

	return levels_size_acceptable


def set_difficulty_for_all_levels(initial_set_of_levels, constants):
	for current_grid_size_id in range(len(grid_sizes)):
		for level_index in range(len(initial_set_of_levels[current_grid_size_id])):
			initial_set_of_levels[current_grid_size_id][level_index].set_estimated_difficulty(constants)

def reduce_levels_set(levels_size_acceptable):
	result=[[] for _ in range (len(grid_sizes))]

	for current_grid_size_id in grid_sizes_id:
		print('====> Current grid size id ', current_grid_size_id)

		# ====  sort kept levels
		levels_size_acceptable[current_grid_size_id].sort()

		# ==== Display infos

		estimated_difficulties = []
		for current_level in levels_size_acceptable[current_grid_size_id]:
			estimated_difficulties.append(current_level.estimated_difficulty)

		# ==== get theoretical estimated_difficulties to reduce
		theoretical_difficulties = get_theoretical_difficulties(levels_size_acceptable[current_grid_size_id])

		levels_reduced = get_reduced_levels(theoretical_difficulties, levels_size_acceptable[current_grid_size_id])

		estimated_difficulties = [current_level.estimated_difficulty for current_level in levels_reduced]
		print("====> Real Difficulties : ", estimated_difficulties)

		for index_reduced in range(len(levels_reduced)):
			current_level = levels_reduced[index_reduced]
			result[current_grid_size_id].append(current_level)
	return result

def get_levels_size_acceptable(complete_levels_list, current_grid_size_id):
	levels_size_acceptable = []
	lowest_size = lowest_solution_sizes[current_grid_size_id]

	for current_level in complete_levels_list:
		if len(current_level.best_moves) >= lowest_size:
			levels_size_acceptable.append(current_level)
	return levels_size_acceptable

def get_reduced_levels(theoretical_difficulties, levels_size_acceptable):
	levels_reduced = []

	for reduced_levels_index in range(number_levels_to_keep):
		index = get_index_of_closest_difficulty(theoretical_difficulties[reduced_levels_index], levels_size_acceptable)
		this_one = levels_size_acceptable.pop(index)
		levels_reduced.append(this_one)
	levels_reduced.sort()
	return levels_reduced

def get_theoretical_difficulties(levels_list):
	theoretical_difficulties = []

	average_step = (levels_list[-1].estimated_difficulty - levels_list[0].estimated_difficulty) / number_levels_to_keep

	current = levels_list[0].estimated_difficulty

	for reduced_levels_index in range(number_levels_to_keep):
		theoretical_difficulties.append(current)
		current += average_step

	print('====> Average step', average_step)
	print("====> Theoretical difficulties : ", theoretical_difficulties)
	return theoretical_difficulties
