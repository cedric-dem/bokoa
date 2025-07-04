from level_generator.config.config import *
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level

class LevelWithSolution(object):
	def __init__(self, level, best_score, best_moves):
		self.level = level

		self.best_score = best_score
		self.best_moves = best_moves

		self.historyOfScoresForBestSolution = None

		self.grid_size_id = level.grid_size_id
		self.grid_size = level.grid_size

		self.historyOfScoresForBestSolution = get_history_of_scores_for_given_solution_on_given_level(self.best_moves, self.level)

	def set_estimated_difficulty(self):

		increasing_steps_counter = 0

		total_score_decreasing = 0
		total_score_increasing = 0

		for current_score_index in range(1, len(self.historyOfScoresForBestSolution)):
			old_score = self.historyOfScoresForBestSolution[current_score_index - 1]
			new_score = self.historyOfScoresForBestSolution[current_score_index]

			if new_score > old_score:
				increasing_steps_counter += 1
				total_score_increasing += (new_score - old_score)

			if new_score < old_score:
				total_score_decreasing += (old_score - new_score)

		proportion_of_increasing_steps = increasing_steps_counter / (len(self.historyOfScoresForBestSolution))
		score_decreasing_normalized = (total_score_decreasing / self.historyOfScoresForBestSolution[-1])

		difficulty_first_term = coefficient_difficulty_first_term_a[self.grid_size_id] - (coefficient_difficulty_first_term_b[self.grid_size_id] * proportion_of_increasing_steps)
		difficulty_second_term = score_decreasing_normalized / coefficient_difficulty_second_term_a[self.grid_size_id]

		self.estimated_difficulty = ((coefficient_difficulty_second_term * difficulty_second_term) + difficulty_first_term) / 2

	def display_everything(self):
		print('==> Grid :')
		self.level.display_level()
		print('==> Solution :', self.best_moves)
		print('==> Best Score : ', self.best_score)

	def __gt__(self, other):
		return self.estimated_difficulty > other.estimated_difficulty

	def __eq__(self, other):
		return self.estimated_difficulty == other.estimated_difficulty
