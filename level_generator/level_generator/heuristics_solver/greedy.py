from level_generator.classes.game import Game
from level_generator.classes.level import Level
from level_generator.classes.solverParent import Solver
from level_generator.config.config import grid_sizes
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level
from level_generator.utils.misc_functions import get_readable_moves

class GreedySolver(Solver):
	def __init__(self, game):
		super().__init__(game)

	def solve(self):
		# TODO clean this mess

		################################################################################################ create temp game, to look for best solution with that heuristic
		# create level
		temp_level = self.game_to_solve.level
		# create game
		temp_game = Game(temp_level)
		# do the backtrack
		grid_size = grid_sizes[self.game_to_solve.grid_size_id]
		# best_score, best_moves = super().back_track_heuristic(temp_game, grid_size[0] * grid_size[1])
		best_score, best_moves = super().back_track_heuristic(temp_game, 10)
		# print('===> best score ', best_score)

		################################################################################################ solve game_to_solve
		best_moves_dir = get_readable_moves(best_moves)
		result = get_history_of_scores_for_given_solution_on_given_level(best_moves_dir, self.game_to_solve.level)[-1]

		return result

	def is_solution_worth_trying(self):
		# TODO
		return True
