from level_generator.classes.solverParent import Solver

class BackTrackingLimitedDepthSolver(Solver):
	def __init__(self, level):
		super().__init__(level)

	def solve(self):
		# TODO
		return 6096.0

	def is_solution_worth_trying(self):
		# TODO
		return True

