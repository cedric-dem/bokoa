from level_generator.classes.game import Game
from level_generator.classes.solverParent import Solver
from level_generator.config.config import grid_sizes
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level
from level_generator.utils.misc_functions import get_readable_moves

def get_advantage_matrix(level):
	result = [[None for i in range(level.grid_size[0])] for j in range(level.grid_size[1])]

	max_dist = 3

	for i in range(level.grid_size[0]):
		for j in range(level.grid_size[1]):

			current_case_advantage = 0
			seen_neighbours = 0

			# Go through neighbourhood of the current case, see if this is interesting to be here
			for delta_i in range(max_dist):
				new_i = i + delta_i
				if (new_i > 0 and new_i < level.grid_size[0]):

					for delta_j in range(max_dist):
						new_j = j + delta_j
						if (new_j > 0 and new_j < level.grid_size[0]):

							if (level.operations_grid[new_i][new_j] != "1"):
								seen_neighbours += 1
								operand = level.operations_grid[new_i][new_j].operand
								match level.operations_grid[new_i][new_j].operation:
									case "+":
										current_case_advantage += 1.5 + 2 * operand
									case "-":
										current_case_advantage -= 1.5 + 2 * operand
									case "×":
										current_case_advantage += 3 + 3 * operand
									case "÷":
										current_case_advantage -= 3 + 3 * operand
									case _:
										print("not found error")

			# result[i][j] = current_case_advantage / seen_neighbours
			result[i][j] = current_case_advantage
	return result

class AdvantageMatrixSolver(Solver):
	def __init__(self, level):
		super().__init__(level)

		self.advantage_matrix = get_advantage_matrix(level)
		print('advantage matrix : ')
		for line in self.advantage_matrix:
			print(line)

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

	def is_solution_worth_trying(self, current_score, current_depth, new_position, new_operation):
		return self.advantage_matrix[new_position[0]][new_position[1]] > 0
