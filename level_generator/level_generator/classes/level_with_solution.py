from level_generator.classes.level import Level
from level_generator.config.config import *
from level_generator.utils.indicators import get_all_indicators
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level, get_occupation_matrix_for_given_solution_on_given_level, get_history_of_operations_for_given_solution_on_given_level

class LevelWithSolution(Level):
	def __init__(self, operations_grid, best_score, best_moves, grid_size_id):
		super().__init__(grid_size_id, operations_grid)

		self.best_score = best_score

		self.best_moves = best_moves

		self.history_of_scores_for_best_solution = get_history_of_scores_for_given_solution_on_given_level(self.best_moves, self)

		self.first_term_raw = None
		self.second_term_raw = None

		self.first_term_normalized = None
		self.second_term_normalized = None

		self.estimated_difficulty = None

	def compute_raw_terms(self):
		self.raw_terms = get_all_indicators(self)

	def set_estimated_difficulty(self, constants):

		self.compute_raw_terms()

		result = 0

		self.normalized_terms = {}

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
