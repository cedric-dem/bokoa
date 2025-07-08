from level_generator.classes.solver_parent import Solver
from level_generator.config.config import grid_sizes

class BackTrackingLimitedDepthSolver(Solver):
	def __init__(self, level, variant):
		super().__init__(level)
		self.variant = variant

	def is_solution_worth_trying(self, current_score, current_depth, new_position, new_operation):
		match self.variant:
			case 0:
				k = 0.2
			case 1:
				k = 0.3
			case _:
				raise ValueError("Invalid Variant  (in limited depth heuristic) : ", self.variant)

		max_depth = int(grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1] * k)
		return current_depth < max_depth
