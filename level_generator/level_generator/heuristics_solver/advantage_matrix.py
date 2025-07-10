from level_generator.classes.solver_parent import Solver
from copy import deepcopy

def get_advantage_matrix(level, variant):
	result = [[None for _ in range(level.grid_size[0])] for _ in range(level.grid_size[1])]

	max_dist = 3  # TODO experiment

	for i in range(level.grid_size[0]):
		for j in range(level.grid_size[1]):

			current_case_advantage = 0
			seen_neighbours = 0

			# Go through neighbourhood of the current case, see if this is interesting to be here
			for delta_i in range(-max_dist, max_dist):
				new_i = i + delta_i
				if 0 < new_i < level.grid_size[0]:

					for delta_j in range(-max_dist, max_dist):
						new_j = j + delta_j
						if (new_i != i or new_j != j) and (0 < new_j < level.grid_size[0]):

							if level.operations_grid[new_i][new_j] != "1":
								seen_neighbours += 1
								distance_with_case_of_interest = abs(delta_j) + abs(delta_i)
								operand = level.operations_grid[new_i][new_j].operand
								match level.operations_grid[new_i][new_j].operation:
									case "×":
										current_case_advantage += (3 + 3 * operand) / distance_with_case_of_interest  # TODO experiment maybe square of distancce ? sqrt ?
									# current_case_advantage += 3
									case "+":
										current_case_advantage += (1.5 + 2 * operand) / distance_with_case_of_interest  # TODO experiment #TODO maybe remove the divider ?
									# current_case_advantage += 3  # TODO experiment #TODO maybe remove the divider ?
									case "-":
										current_case_advantage -= (1.5 + 2 * operand) / distance_with_case_of_interest
									# current_case_advantage -= 3
									case "÷":
										current_case_advantage -= (2 + 3 * operand) / distance_with_case_of_interest
									# current_case_advantage -= 3
									case _:
										raise ValueError("Invalid  operation " + str(level.operations_grid[new_i][new_j].operation))

			# result[i][j] = current_case_advantage / seen_neighbours
			result[i][j] = current_case_advantage

	# return mix_advantages(result)  # TODO see if this improve reliability or not
	return result

def mix_advantages(current):
	result = deepcopy(current)

	max_dist = 2  # TODO experiment

	for i in range(len(result)):
		for j in range(len(result[0])):
			# will adjust result[i][j] depending on the neighbourhood

			correction_coefficient = 0

			# Go through neighbourhood of the current case, see if this is interesting to be around
			for delta_i in range(-max_dist, max_dist):
				new_i = i + delta_i
				if 0 < new_i < len(result):

					for delta_j in range(-max_dist, max_dist):
						new_j = j + delta_j
						if (new_i != i or new_j != j) and (0 < new_j < len(result[0])):

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
	def __init__(self, level, variant):
		super().__init__(variant, level)

		self.advantage_matrix = round_mat(get_advantage_matrix(level, self.variant))

	# display_advantage_matrix(self.advantage_matrix)

	def is_solution_worth_trying(self, current_game, new_position):
		return self.advantage_matrix[new_position[0]][new_position[1]] >= -5
