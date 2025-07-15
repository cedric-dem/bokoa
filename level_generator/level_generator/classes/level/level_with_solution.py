from level_generator.classes.level.level import Level
from level_generator.config.config import *
from level_generator.utils.indicators import get_all_indicators
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level, get_occupation_matrix_for_given_solution_on_given_level
import json

class LevelWithSolution(Level):
	def __init__(self, operations_grid, highest_possible_score, solution, grid_size_id):
		super().__init__(grid_size_id, operations_grid)

		self.highest_possible_score = highest_possible_score

		self.solution = solution

		self.history_of_scores_for_solution = get_history_of_scores_for_given_solution_on_given_level(self.solution, self)

		self.estimated_difficulty = None

		self.raw_difficulty_terms = {}
		self.normalized_difficulty_terms = {}

	def compute_raw_terms(self):
		self.raw_difficulty_terms = get_all_indicators(self)

	def set_estimated_difficulty(self, constants):

		self.compute_raw_terms()

		result = 0

		for raw_term_name in self.raw_difficulty_terms:
			this_offset = constants[raw_term_name][0][self.grid_size_id]
			this_multiply_factor = constants[raw_term_name][1][self.grid_size_id]

			this_term_normalized = this_offset + self.raw_difficulty_terms[raw_term_name] * this_multiply_factor

			result += this_term_normalized * weights_parameters[raw_term_name]
			self.normalized_difficulty_terms[raw_term_name] = this_term_normalized

		self.estimated_difficulty = round(result, 6)

	def display_everything(self):
		print('==> Grid :')
		self.display_level_with_solution()
		print('==> Solution :', self.solution)
		print('==> Best Score : ', self.highest_possible_score)
		print('==> Evolution of  Score : ', self.history_of_scores_for_solution)

	def display_level_with_solution(self):
		occupation = get_occupation_matrix_for_given_solution_on_given_level(self.solution, self)
		for line_index in range(len(self.operations_grid)):
			for cell_index in range(len(self.operations_grid[line_index])):
				cell_repr = str(self.operations_grid[line_index][cell_index])

				if occupation[line_index][cell_index]:
					cell_repr = "(" + cell_repr + ")"
				else:
					cell_repr = " " + cell_repr + " "

				print(cell_repr, end = " ")
			print()

	def __gt__(self, other):
		return self.estimated_difficulty > other.estimated_difficulty

	def __eq__(self, other):
		return self.estimated_difficulty == other.estimated_difficulty

	def save_level_as_json(self, filename):
		if format_json:
			resulting_str = self.get_level_representation()

			with open(filename, "w", encoding = "utf-8") as f:
				f.write(resulting_str)

		else:
			result = {
				"operations": [[str(car) for car in line] for line in self.operations_grid],
				"bestScore": round(float(self.highest_possible_score), 2),
				"bestMoves": self.solution,
			}

			with open(filename, 'w') as file:
				json.dump(result, file, indent = 4, separators = (',', ': '), ensure_ascii = False)

	def get_level_representation(self):
		resulting_str = "{\n"

		# add operations
		resulting_str += get_formatted_operations_grid(self.operations_grid)

		# add best score
		resulting_str += get_formatted_best_score(self.highest_possible_score)

		# add best moves
		resulting_str += get_best_moves_formatted(self.solution)

		resulting_str += "}"

		# print("=> Str :\n", resulting_str)
		return resulting_str

def get_formatted_operations_grid(operations_grid):
	operations_grid_string = "  \"operations\": [\n"
	for line_index in range(len(operations_grid)):
		line = operations_grid[line_index]
		operations_grid_string += "    ["
		for col_index in range(len(line)):
			col = line[col_index]
			operations_grid_string += '"' + str(col) + '"'
			if col_index != len(line) - 1:
				operations_grid_string += ","

		if line_index != len(operations_grid) - 1:
			operations_grid_string += "],\n"
		else:
			operations_grid_string += "]\n"

	operations_grid_string += "  ],\n"
	return operations_grid_string

def get_formatted_best_score(best_score):
	return "  \"bestScore\": " + str(round(float(best_score), 2)) + ",\n"

def get_best_moves_formatted(best_moves):
	solution_string = "  \"bestMoves\": [\n    "
	for move_index in range(len(best_moves)):
		move = best_moves[move_index]
		solution_string += '"' + move + '"'
		if move_index != len(best_moves) - 1:
			solution_string += ","
	solution_string += "\n  ]\n"
	return solution_string
