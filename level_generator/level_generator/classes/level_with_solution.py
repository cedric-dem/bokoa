from level_generator.classes.level import Level
from level_generator.config.config import *
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level, get_occupation_matrix_for_given_solution_on_given_level, get_history_of_operations_for_given_solution_on_given_level
import random

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
		if difficulty_function in ["sum_two_terms", "min_two_terms", "max_two_terms"]:
			increasing_steps_counter = 0

			total_score_decreasing = 0
			total_score_increasing = 0

			for current_score_index in range(1, len(self.history_of_scores_for_best_solution)):
				old_score = self.history_of_scores_for_best_solution[current_score_index - 1]
				new_score = self.history_of_scores_for_best_solution[current_score_index]

				if new_score > old_score:
					increasing_steps_counter += 1
					total_score_increasing += (new_score - old_score)

				if new_score < old_score:
					total_score_decreasing += (old_score - new_score)

			# TODO try with srqt or squared
			self.first_term_raw = -increasing_steps_counter / (len(self.history_of_scores_for_best_solution))
			self.second_term_raw = (total_score_decreasing / self.history_of_scores_for_best_solution[-1])
		else:
			self.first_term_raw = random.randint(1, 10)  ##TODO refactor
			self.second_term_raw = random.randint(1, 10)

	def set_estimated_difficulty(self, constants):
		match difficulty_function:
			case "sum_two_terms" | "min_two_terms" | "max_two_terms":
				self.compute_raw_terms()

				self.first_term_normalized = constants["coefficient_difficulty_first_term_a"][self.grid_size_id] + (constants["coefficient_difficulty_first_term_b"][self.grid_size_id] * self.first_term_raw)
				self.second_term_normalized = self.second_term_raw * constants["coefficient_difficulty_second_term_a"][self.grid_size_id]

				t1 = coefficient_difficulty_first_term * self.first_term_normalized
				t2 = coefficient_difficulty_second_term * self.second_term_normalized

				match difficulty_function:
					case "min_two_terms":
						self.estimated_difficulty = round(min(t1, t2), 6)
					case "max_two_terms":
						self.estimated_difficulty = round(max(t1, t2), 6)
					case "sum_two_terms":
						self.estimated_difficulty = round(t1 + t2, 6)
					case _:
						raise ValueError("Not found difficulty : ", difficulty_function)

			case "points_estimate":

				lst_operations = get_history_of_operations_for_given_solution_on_given_level(self.best_moves, self)
				occupation_matrix = get_occupation_matrix_for_given_solution_on_given_level(self.best_moves, self)

				self.estimated_difficulty = get_points_estimate(lst_operations, occupation_matrix, self.history_of_scores_for_best_solution, self.best_moves, self.operations_grid)

			case _:
				raise ValueError("Not found difficulty : ", difficulty_function)

	def display_everything(self):
		print('==> Grid :')
		super().display_level()
		print('==> Solution :', self.best_moves)
		print('==> Best Score : ', self.best_score)

	def __gt__(self, other):
		return self.estimated_difficulty > other.estimated_difficulty

	def __eq__(self, other):
		return self.estimated_difficulty == other.estimated_difficulty

def get_points_estimate(operations, occupation, scores_history, best_moves, operations_grid):
	current_difficulty_estimate = 1

	for current_score_index in range(len(operations)):
		current_operation = operations[current_score_index - 1]

		progression_proportion = current_score_index / len(operations)

		match current_operation.operation:
			case "+":
				if current_score_index < 5:
					current_difficulty_estimate += 5 * (current_operation.operand + 5)
				else:
					current_difficulty_estimate += 2 * (current_operation.operand + 5)

			case '-':
				if current_score_index < 5:
					current_difficulty_estimate -= 5 * (current_operation.operand + 5)
				else:
					current_difficulty_estimate -= 2 * (current_operation.operand + 5)
			case '×':
				if current_score_index < 5:
					current_difficulty_estimate += 3 * (current_operation.operand + 5)
				else:
					current_difficulty_estimate += 7 * (current_operation.operand + 5)
			case '÷':
				if current_score_index < 5:
					current_difficulty_estimate -= 2 * (current_operation.operand + 5)
				else:
					current_difficulty_estimate -= 7 * (current_operation.operand + 5)
			case _:
				raise ValueError("Invalid Value  (Operation not found) : ", current_operation.operation)

	return -round(current_difficulty_estimate, 2)
