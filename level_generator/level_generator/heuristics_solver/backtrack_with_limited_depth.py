from level_generator.classes.game import Game
from level_generator.classes.solverParent import Solver
from level_generator.config.config import grid_sizes
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level
from level_generator.utils.misc_functions import get_readable_moves

class BackTrackingLimitedDepthSolver(Solver):
	def __init__(self, level):
		super().__init__(level)

	def solve(self):
		# TODO clean this mess

		################################################################################################ create temp game, to look for best solution with that heuristic
		temp_game = Game(self.level_to_solve)

		max_depth = int(grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1] * 0.5) #TODO fine tune, find best tradeoff than this

		best_score, best_moves = super().back_track_heuristic(temp_game, max_depth)

		################################################################################################ solve level_to_solve
		best_moves_dir = get_readable_moves(best_moves)
		result = get_history_of_scores_for_given_solution_on_given_level(best_moves_dir, self.level_to_solve)[-1]

		return result

	def is_solution_worth_trying(self):
		# TODO
		return True