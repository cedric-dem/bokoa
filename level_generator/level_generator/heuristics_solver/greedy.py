from level_generator.classes.game import Game
from level_generator.classes.level import Level
from level_generator.classes.solverParent import Solver
from level_generator.config.config import grid_sizes

class GreedySolver(Solver):
	def __init__(self, game):
		super().__init__(game)

	def solve(self):
		# TODO clean this mess

		# create level
		# temp_level = Level(self.game.grid_size_id, self.game.level.operations_grid)
		temp_level = Level(self.game.grid_size_id, None)

		# create game
		temp_game = Game(temp_level)

		# do the backtrack
		grid_size = grid_sizes[self.game.grid_size_id]

		# best_score, best_moves = super().back_track_heuristic(temp_game, grid_size[0] * grid_size[1])
		best_score, best_moves = super().back_track_heuristic(temp_game, 10)

		print('===> best score ', best_score)

	def is_solution_worth_trying(self):
		# TODO
		return True
