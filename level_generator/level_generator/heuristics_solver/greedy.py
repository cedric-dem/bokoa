from level_generator.classes.game import Game
from level_generator.classes.solverParent import Solver
from level_generator.config.config import grid_sizes
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level
from level_generator.utils.misc_functions import get_readable_moves
import random

class GreedySolver(Solver):
	def __init__(self, level):
		super().__init__(level)

	def solve(self):
		# TODO clean this mess

		################################################################################################ create temp game, to look for best solution with that heuristic
		temp_game = Game(self.level_to_solve)

		max_depth = int(grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1])

		best_score, best_moves = super().back_track_heuristic(temp_game, max_depth)

		################################################################################################ solve level_to_solve
		best_moves_dir = get_readable_moves(best_moves)
		result = get_history_of_scores_for_given_solution_on_given_level(best_moves_dir, self.level_to_solve)[-1]
		return result

	def is_solution_worth_trying(self, current_score, current_depth, new_operation):
		half_max_length = int(grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1] / 2)
		early_point= int(grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1] / 4)

		is_after_half_max_length = current_depth > half_max_length
		is_after_early_point = current_depth > early_point

		is_positive = (new_operation.operation == "+" or new_operation.operation == "×")
		is_divide_and_late = (is_after_half_max_length and new_operation.operation == "÷")
		is_minus_and_early = ((not is_after_half_max_length) and new_operation.operation == "-")

		# result = is_positive or (is_divide_and_late or is_minus_and_early) # Absolute greed, not reliable but quite instantaneous
		result = is_positive or is_divide_and_late or is_minus_and_early or is_after_half_max_length  # slightly better, still instantaneous

		return result
