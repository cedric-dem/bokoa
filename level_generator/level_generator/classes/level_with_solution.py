from level_generator.classes.level import Level
from level_generator.config.config import *
from level_generator.utils.indicators import get_all_indicators
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level, get_occupation_matrix_for_given_solution_on_given_level
import json

class LevelWithSolution(Level):
	def __init__(self, operations_grid, best_score, best_moves, grid_size_id):
		super().__init__(grid_size_id, operations_grid)

		self.best_score = best_score

		self.best_moves = best_moves

		self.history_of_scores_for_best_solution = get_history_of_scores_for_given_solution_on_given_level(self.best_moves, self)

		self.estimated_difficulty = None

		self.raw_terms = {}
		self.normalized_terms = {}

	def compute_raw_terms(self):
		self.raw_terms = get_all_indicators(self)

	def set_estimated_difficulty(self, constants):

		self.compute_raw_terms()

		result = 0

		for raw_term_name in self.raw_terms:
			this_offset = constants[raw_term_name][0][self.grid_size_id]
			this_multiply_factor = constants[raw_term_name][1][self.grid_size_id]

			this_term_normalized = this_offset + self.raw_terms[raw_term_name] * this_multiply_factor

			result += this_term_normalized * weights_parameters[raw_term_name]
			self.normalized_terms[raw_term_name] = this_term_normalized

		self.estimated_difficulty = round(result, 6)

	def display_everything(self):
		print('==> Grid :')
		# super().display_level() #without solution
		self.display_level_with_solution()
		print('==> Solution :', self.best_moves)
		print('==> Best Score : ', self.best_score)
		print('==> Evolution of  Score : ', self.history_of_scores_for_best_solution)

	def display_level_with_solution(self):
		occupation = get_occupation_matrix_for_given_solution_on_given_level(self.best_moves, self)
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

	def save_level_as_json(self, filename):  # TODO split into get repr, with boolean show sol
		if format_json:
			resulting_str = "{\n"

			# add operations
			resulting_str += "  \"operations\": [\n"
			for line_index in range(len(self.operations_grid)):
				line = self.operations_grid[line_index]
				resulting_str += "    ["
				for col_index in range(len(line)):
					col = line[col_index]
					resulting_str += '"' + str(col) + '"'
					if col_index != len(line) - 1:
						resulting_str += ","

				if line_index != len(self.operations_grid) - 1:
					resulting_str += "],\n"
				else:
					resulting_str += "]\n"

			resulting_str += "  ],\n"

			# add best score
			resulting_str += "  \"bestScore\": " + str(round(float(self.best_score), 2)) + ",\n"

			# add best moves
			resulting_str += "  \"bestMoves\": [\n    "
			for move_index in range(len(self.best_moves)):
				move = self.best_moves[move_index]
				resulting_str += '"' + move + '"'
				if move_index != len(self.best_moves) - 1:
					resulting_str += ","
			resulting_str += "\n  ]\n"

			resulting_str += "}"

			# print("=> Str :\n", resulting_str)

			with open(filename, "w", encoding = "utf-8") as f:
				f.write(resulting_str)

		else:
			result = {
				"operations": [[str(car) for car in line] for line in self.operations_grid],  # neutral will be converted as string "1" and operation will go trough the __str__ function
				"bestScore": round(float(self.best_score), 2),
				"bestMoves": self.best_moves,
			}

			with open(filename, 'w') as file:
				json.dump(result, file, indent = 4, separators = (',', ': '), ensure_ascii = False)
