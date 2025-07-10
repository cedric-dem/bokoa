from level_generator.classes.solver_parent import Solver
from level_generator.utils.display_functions import get_approx_function

class BackTrackingWithScoreCheckSolver(Solver):
	def __init__(self, level, variant):
		super().__init__(level)
		self.variant = variant

	def is_solution_worth_trying(self, current_score, current_depth, new_position, new_operation):
		estimated_lower = get_approx_function(self.level_to_solve.grid_size_id)[current_depth]

		# lower the margin => better accuracy, but cost more time
		match self.variant:
			case 0:
				margin = (current_depth * 2) - 1  # starts at 0, increase as depth goes on (really fast,1.2 seconds, and 84% accuracy)
			case 1:
				margin = (current_depth * 1.2)  # starts at 0, increase as depth goes on (really fast, still 93% accuracy approximately, takes 2 seconds for grid size 6x6)
			case 2:
				margin = -1  # slower, roughly 9 sec for grid size 6x6 but 100% reliable on reduced set
			case _:
				raise ValueError("Invalid Variant  (in score check heuristic) : ", self.variant)

		return current_score >= estimated_lower + margin
