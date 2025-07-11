import json

from level_generator.classes.level_with_solution import *
from level_generator.classes.level import *

def save_all_levels(levels_reduced):
	for current_grid_size_id in range(len(grid_sizes)):
		for level_index in range(len(levels_reduced[current_grid_size_id])):
			current_level = levels_reduced[current_grid_size_id][level_index]

			create_level_file_as_json(
				current_level.operations_grid,
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

			new_level_with_sol = LevelWithSolution(data["operations"], data["bestScore"], data["bestMoves"], grid_size_id)
			complete_levels_list.append(new_level_with_sol)

	return complete_levels_list

def create_level_file_as_json(operations, best_score, best_moves, filename):
	if format_json:
		resulting_str = "{\n"

		# add operations
		resulting_str += "  \"operations\": [\n"
		for line_index in range(len(operations)):
			line = operations[line_index]
			resulting_str += "    ["
			for col_index in range(len(line)):
				col = line[col_index]
				resulting_str += '"' + str(col) + '"'
				if col_index != len(line) - 1:
					resulting_str += ","

			if line_index != len(operations) - 1:
				resulting_str += "],\n"
			else:
				resulting_str += "]\n"

		resulting_str += "  ],\n"

		# add best score
		resulting_str += "  \"bestScore\": " + str(round(float(best_score), 2)) + ",\n"

		# add best moves
		resulting_str += "  \"bestMoves\": [\n    "
		for move_index in range(len(best_moves)):
			move = best_moves[move_index]
			resulting_str += '"' + move + '"'
			if move_index != len(best_moves) - 1:
				resulting_str += ","
		resulting_str += "\n  ]\n"

		resulting_str += "}"

		# print("=> Str :\n", resulting_str)

		with open(filename, "w", encoding = "utf-8") as f:
			f.write(resulting_str)

	else:
		result = {
			"operations": [[str(car) for car in line] for line in operations],  # neutral will be converted as string "1" and operation will go trough the __str__ function
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
	return generated_levels_folder_name + "/" + levels_set_folder_name + "/" + grid_size_folder_prefix + str(grid_size_index) + "/" + level_file_name + (6 - len(str(level_index))) * "0" + str(level_index) + ".json"

def get_complete_folder_path(folder, grid_size_index):
	return generated_levels_folder_name + "/" + folder + "/" + grid_size_folder_prefix + str(grid_size_index) + "/"
