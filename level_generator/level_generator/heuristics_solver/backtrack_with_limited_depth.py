from level_generator.classes.solverParent import Solver
from level_generator.config.config import grid_sizes

class BackTrackingLimitedDepthSolver(Solver):
	def __init__(self, level, variant):
		super().__init__(level)
		self.variant = variant

	def is_solution_worth_trying(self, current_score, current_depth, new_position, new_operation):
		max_depth = int(grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1] * 0.5)  # TODO fine tune, find best tradeoff than this
		return current_depth < max_depth
