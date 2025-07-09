from level_generator.classes import level
from level_generator.classes.game import Game
from level_generator.classes.solverParent import Solver
from level_generator.config.config import grid_sizes
from level_generator.utils.level_with_sol_creation_functions import get_history_of_scores_for_given_solution_on_given_level
from level_generator.utils.misc_functions import get_readable_moves
from copy import deepcopy

def get_advantage_matrix(level):
	result = [[None for _ in range(level.grid_size[0])] for _ in range(level.grid_size[1])]

	max_dist = 3  # TODO experiment

	for i in range(level.grid_size[0]):
		for j in range(level.grid_size[1]):

			current_case_advantage = 0
			seen_neighbours = 0

			# Go through neighbourhood of the current case, see if this is interesting to be here
			for delta_i in range(-max_dist, max_dist):
				new_i = i + delta_i
				if (new_i > 0 and new_i < level.grid_size[0]):

					for delta_j in range(-max_dist, max_dist):
						new_j = j + delta_j
						if (new_i != i or new_j != j) and (new_j > 0 and new_j < level.grid_size[0]):

							if (level.operations_grid[new_i][new_j] != "1"):
								seen_neighbours += 1
								distance_with_case_of_interest = abs(delta_j) + abs(delta_i)
								operand = level.operations_grid[new_i][new_j].operand
								match level.operations_grid[new_i][new_j].operation:
									case "+":
										current_case_advantage += (1.5 + 2 * operand) / distance_with_case_of_interest  # TODO experiment #TODO maybe remove the divider ?
									case "-":
										current_case_advantage -= (1.5 + 2 * operand) / distance_with_case_of_interest
									case "×":
										current_case_advantage += (3 + 3 * operand) / distance_with_case_of_interest  # TODO experiment maybe square of distancce ? sqrt ?
									case "÷":
										current_case_advantage -= (3 + 3 * operand) / distance_with_case_of_interest
									case _:
										print("not found error")

			# result[i][j] = current_case_advantage / seen_neighbours
			result[i][j] = current_case_advantage

	# return result
	return mix_advantages(result)  # TODO see if this improve reliability or not

def mix_advantages(current):
	result = deepcopy(current)

	max_dist = 3  # TODO experiment

	for i in range(len(result)):
		for j in range(len(result[0])):
			# will adjust result[i][j] depending on the neighbourhood

			correction_coefficient = 0

			# Go through neighbourhood of the current case, see if this is interesting to be around
			for delta_i in range(-max_dist, max_dist):
				new_i = i + delta_i
				if (new_i > 0 and new_i < len(result)):

					for delta_j in range(-max_dist, max_dist):
						new_j = j + delta_j
						if (new_i != i or new_j != j) and (new_j > 0 and new_j < len(result[0])):

							if result[i][j] > 0:  # TODO maybe remove that if
								distance_with_case_of_interest = abs(delta_j) + abs(delta_i)

								correction_coefficient += result[i][j] / distance_with_case_of_interest  # TODO experiment

			result[i][j] += correction_coefficient
	return result

def round_mat(mat):
	return [[round(mat[i][j], 2) for i in range(len(mat[0]))] for j in range(len(mat))]

def display_advantage_matrix(mat):
	print('==> advantage matrix : ')
	for line in mat:
		print(line)

class AdvantageMatrixSolver(Solver):
	def __init__(self, level):
		super().__init__(level)

		self.advantage_matrix = round_mat(get_advantage_matrix(level))

	# display_advantage_matrix(self.advantage_matrix)

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
		return self.advantage_matrix[new_position[0]][new_position[1]] >= -1
