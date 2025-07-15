from level_generator.classes.case.initial_case import InitialCase
from level_generator.classes.level.level_with_solution import *
from level_generator.classes.level.level import *
from level_generator.classes.case.operation import Operation

def save_all_levels(levels_reduced):
	for current_grid_size_id in range(len(grid_sizes)):
		for level_index in range(len(levels_reduced[current_grid_size_id])):
			current_level = levels_reduced[current_grid_size_id][level_index]

			filename = get_level_path_reduced(current_grid_size_id, level_index)

			current_level.save_level_as_json(filename)

def get_levels_list(set_name, grid_size_id, quantity):
	complete_levels_list = []

	for current_level_index in range(quantity):
		# this_file_path = get_level_path_complete(grid_size_id, current_level_index)
		this_file_path = get_level_path(set_name, grid_size_id, current_level_index)

		with open(this_file_path, 'r', encoding = 'utf-8') as file:
			data = json.load(file)

			new_level_with_sol = LevelWithSolution(read_as_operations_grid(data["operations"]), data["bestScore"], data["bestMoves"], grid_size_id)
			complete_levels_list.append(new_level_with_sol)

	return complete_levels_list

def read_as_operations_grid(operations_grid_as_str):
	operation_grid = [[None for _ in range(len(operations_grid_as_str))] for _ in range(len(operations_grid_as_str[0]))]

	for line_index in range(len(operations_grid_as_str)):
		for column_index in range(len(operations_grid_as_str[line_index])):
			if line_index == 0 and column_index == 0:
				new_case = InitialCase()
			else:
				new_case = Operation(operations_grid_as_str[line_index][column_index][0], int(operations_grid_as_str[line_index][column_index][1]))
			operation_grid[line_index][column_index] = new_case
	return operation_grid

def get_level_path_complete(grid_size_index, level_index):
	return get_level_path(complete_folder_name, grid_size_index, level_index)

def get_level_path_reduced(grid_size_index, level_index):
	return get_level_path(reduced_folder_name, grid_size_index, level_index)

def get_level_path(levels_set_folder_name, grid_size_index, level_index):
	return generated_levels_folder_name + "/" + levels_set_folder_name + "/" + grid_size_folder_prefix + str(grid_size_index) + "/" + level_file_name + (6 - len(str(level_index))) * "0" + str(level_index) + ".json"

def get_complete_folder_path(folder, grid_size_index):
	return generated_levels_folder_name + "/" + folder + "/" + grid_size_folder_prefix + str(grid_size_index) + "/"
