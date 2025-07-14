from unittest import case

from level_generator.classes.level import Level
from level_generator.config.config import *
from level_generator.utils.indicators import get_all_indicators
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level, get_occupation_matrix_for_given_solution_on_given_level, get_history_of_operations_for_given_solution_on_given_level

class LevelWithSolution(Level):  # TODO : inherit from Level
	def __init__(self, operations_grid, best_score, best_moves, grid_size_id):
		super().__init__(grid_size_id, operations_grid)

		self.best_score = best_score

		self.best_moves = best_moves

		self.history_of_scores_for_best_solution = get_history_of_scores_for_given_solution_on_given_level(self.best_moves, self)

		self.predictions_of_heuristics = {}

		self.first_term_raw = None
		self.second_term_raw = None

		self.first_term_normalized = None
		self.second_term_normalized = None

		self.estimated_difficulty = None

	def compute_raw_terms(self):
		self.raw_terms = get_all_indicators(self)

	def set_estimated_difficulty(self, constants):

		self.compute_raw_terms()

		raw_terms_normalized = []
		for raw_term_index in range(len(self.raw_terms)):
			raw_term = self.raw_terms[raw_term_index]

			this_term_normalized = constants[raw_term_index][0][self.grid_size_id] + raw_term * constants[raw_term_index][1][self.grid_size_id]

			raw_terms_normalized.append(this_term_normalized)

		result = 0
		for raw_term_index in range(len(raw_terms_normalized)):
			result += raw_terms_normalized[raw_term_index] * weights_parameters[raw_term_index]

		self.estimated_difficulty = round(result, 6)

	def display_everything(self):
		print('==> Grid :')
		super().display_level()
		print('==> Solution :', self.best_moves)
		print('==> Best Score : ', self.best_score)

	def __gt__(self, other):
		return self.estimated_difficulty > other.estimated_difficulty

	def __eq__(self, other):
		return self.estimated_difficulty == other.estimated_difficulty
