from level_generator.utils.misc_functions import back_track
from level_generator.classes.game import Game
from level_generator.config.config import grid_sizes

class Solver(object):
	def __init__(self, variant, level):
		self.variant = variant
		self.level_to_solve = level

	def solve(self):
		# create temp game, to look for best solution with that heuristic
		temp_game = Game(self.level_to_solve)
		max_depth = grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1]
		best_score, _ = back_track(temp_game, max_depth, self)

		return best_score

	def is_solution_worth_trying(self, current_game, new_position):
		return None
