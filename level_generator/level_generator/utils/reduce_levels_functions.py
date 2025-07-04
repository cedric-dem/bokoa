from level_generator.classes.level import *
from level_generator.utils.file_level_functions import get_complete_levels_list, create_level_file_as_json, get_level_path_reduced

def get_index_of_closest_difficulty(difficulty_to_search, levels_list):
	closest_index = 0
	closest_distance = float("inf")

	for current_index in range(len(levels_list)):
		this_distance = abs(difficulty_to_search - levels_list[current_index].estimated_difficulty)
		if closest_distance > this_distance:
			closest_index = current_index
			closest_distance = this_distance

	return closest_index

def reduce_levels_set():
	for current_grid_size_id in grid_sizes_id:
		reduce_levels_set_given_grid_size_id(current_grid_size_id)

def reduce_levels_set_given_grid_size_id(current_grid_size_id):
	print('====> Current grid size id ', current_grid_size_id)

	complete_levels_list = get_complete_levels_list(current_grid_size_id,  raw_levels_to_generate)
	print("====>  Initially total of  ", len(complete_levels_list), " levels")

	levels_size_acceptable = get_levels_size_acceptable(complete_levels_list, current_grid_size_id)
	print("====>  After remove too small levels total of  ", len(levels_size_acceptable), " levels")

	# ===== set difficulty  of kept levels
	for current_level in levels_size_acceptable:
		current_level.set_estimated_difficulty()

	# ====  sort kept levels
	levels_size_acceptable.sort()

	# ==== Display infos

	estimated_difficulties = []
	for current_level in levels_size_acceptable:
		estimated_difficulties.append(current_level.estimated_difficulty)

	# ==== get theoretical estimated_difficulties to reduce
	theoretical_difficulties = get_theoretical_difficulties(levels_size_acceptable)

	levels_reduced = get_reduced_levels(theoretical_difficulties, levels_size_acceptable)

	estimated_difficulties = [current_level.estimated_difficulty for current_level in levels_reduced]
	print("====> Real Difficulties : ", estimated_difficulties)

	for index_reduced in range(len(levels_reduced)):
		current_level = levels_reduced[index_reduced]

		create_level_file_as_json(
			current_level.level.operations_grid,
			current_level.best_score,
			current_level.best_moves,
			get_level_path_reduced(current_grid_size_id, index_reduced) + str(index_reduced) + ".json"
		)

	print("====>  Keeping ", len(levels_reduced), " levels")

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
