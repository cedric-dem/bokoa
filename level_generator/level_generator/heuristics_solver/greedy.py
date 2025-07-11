from level_generator.classes.solver_parent import Solver
from level_generator.config.config import grid_sizes

class GreedySolver(Solver):
	def __init__(self, level, variant):
		super().__init__(variant, level)

	def is_solution_worth_trying(self, current_game, new_position):
		half_max_length = int(grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1] / 2)
		early_point = int(grid_sizes[self.level_to_solve.grid_size_id][0] * grid_sizes[self.level_to_solve.grid_size_id][1] / 4)

		is_after_half_max_length = len(current_game.moves_history) > half_max_length
		is_after_early_point = len(current_game.moves_history) > early_point

		new_operation = current_game.level.operations_grid[new_position[0]][new_position[1]]

		is_positive = (new_operation.operation == "+" or new_operation.operation == "×")
		is_divide_and_late = (is_after_half_max_length and new_operation.operation == "÷")
		is_minus_and_early = ((not is_after_half_max_length) and new_operation.operation == "-")

		match self.variant:
			case 0:
				result = is_positive or (is_divide_and_late or is_minus_and_early)  # Absolute greed, not reliable but quite instantaneous
			case 1:
				result = is_positive or is_divide_and_late or is_minus_and_early or is_after_half_max_length  # slightly better, still instantaneous
			case _:
				raise ValueError("Invalid Variant  (in greedy heuristic) : ", self.variant)

		return result
