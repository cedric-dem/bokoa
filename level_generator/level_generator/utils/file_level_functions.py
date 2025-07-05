import json

from level_generator.classes.levelWithSolution import *
from level_generator.classes.level import *

def save_all_levels(levels_reduced):
	for current_grid_size_id in range(len(grid_sizes)):
		for level_index in range(len(levels_reduced[current_grid_size_id])):
			current_level = levels_reduced[current_grid_size_id][level_index]

			create_level_file_as_json(
				current_level.level.operations_grid,
				current_level.best_score,
				current_level.best_moves,
				get_level_path_reduced(current_grid_size_id, level_index)
			)

def get_levels_list(set_name, grid_size_id, quantity):
	complete_levels_list = []

	for current_level_index in range(quantity):
		# load json :

		# this_file_path = get_level_path_complete(grid_size_id, current_level_index)
		this_file_path = get_level_path(set_name, grid_size_id, current_level_index)

		with open(this_file_path, 'r', encoding = 'utf-8') as file:
			data = json.load(file)

			new_level = Level(grid_size_id, data["operations"])
			new_level_with_sol = LevelWithSolution(new_level, data["bestScore"], data["bestMoves"])
			complete_levels_list.append(new_level_with_sol)

	return complete_levels_list

def create_level_file_as_json(operations, best_score, best_moves, filename):
	result = {
		"operations": operations,
		"bestScore": round(float(best_score), 2),
		"bestMoves": best_moves
	}

	with open(filename, 'w') as file:
		json.dump(result, file, indent = 4, separators = (',', ': '), ensure_ascii = False)

def get_level_path_complete(grid_size_index, level_index):
	return get_level_path(complete_folder_name, grid_size_index, level_index)

def get_level_path_reduced(grid_size_index, level_index):
	return get_level_path(reduced_folder_name, grid_size_index, level_index)

def get_level_path(levels_set_folder_name, grid_size_index, level_index):
	return generated_levels_folder_name + "/" + levels_set_folder_name + "/" + grid_size_folder_prefix + str(grid_size_index) + "/" + level_file_name + str(level_index) + ".json"
