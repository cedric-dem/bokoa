from level_generator.classes.game import Game
from level_generator.config.config import *

def get_history_of_scores_for_given_solution_on_given_level(solution, level):
	current_game = Game(level)

	history_of_scores_for_best_solution = [1]

	for move in solution:
		move_direction = get_direction(move)
		current_game.move(move_direction)
		history_of_scores_for_best_solution.append(current_game.score)

	return history_of_scores_for_best_solution

def get_direction(move):
	if move == ">":
		result = [0, 1]

	elif move == "<":
		result = [0, -1]

	elif move == "u":
		result = [1, 0]

	elif move == "n":
		result = [-1, 0]

	return result

class LevelWithSolution(object):
	def __init__(self, level, best_score, best_moves):
		self.level = level

		self.best_score = best_score
		self.best_moves = best_moves

		self.historyOfScoresForBestSolution = None

		self.grid_size_id = level.grid_size_id
		self.grid_size = level.grid_size

	def set_fitness_score(self):
		self.historyOfScoresForBestSolution = get_history_of_scores_for_given_solution_on_given_level(self.best_moves, self.level)

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

		fitness_first_term = coefficient_fitness_first_term_a[self.grid_size_id] - (coefficient_fitness_first_term_b[self.grid_size_id] * proportion_of_increasing_steps)
		fitness_second_term = score_decreasing_normalized / coefficient_fitness_second_term_a[self.grid_size_id]

		self.estimated_difficulty = (coefficient_fitness_second_term * fitness_second_term) + fitness_first_term

	def display_everything(self):
		print('==> Grid :')
		self.level.display_level()
		print('==> Solution :', self.best_moves)
		print('==> Best Score : ', self.best_score)

	def __gt__(self, other):
		return self.estimated_difficulty > other.estimated_difficulty

	def __eq__(self, other):
		return self.estimated_difficulty == other.estimated_difficulty
