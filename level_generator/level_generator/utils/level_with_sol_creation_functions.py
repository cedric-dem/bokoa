from level_generator.classes.game import Game

def get_history_of_scores_for_given_solution_on_given_level(solution, level):
	current_game = Game(level)

	history_of_scores_for_best_solution = [1]

	for move in solution:
		move_direction = get_direction_from_move(move)

		current_game.apply_move_given_direction(move_direction)
		history_of_scores_for_best_solution.append(current_game.score)

	return history_of_scores_for_best_solution

def get_history_of_operations_for_given_solution_on_given_level(solution, level):
	current_game = Game(level)

	history_of_operations_for_best_solution = []

	for move in solution:
		move_direction = get_direction_from_move(move)

		current_game.apply_move_given_direction(move_direction)

		history_of_operations_for_best_solution.append(current_game.level.operations_grid[current_game.current_position_head[0]][current_game.current_position_head[1]])

	return history_of_operations_for_best_solution[1:]

def get_occupation_matrix_for_given_solution_on_given_level(solution, level):
	current_game = Game(level)


	for move in solution:
		move_direction = get_direction_from_move(move)

		current_game.apply_move_given_direction(move_direction)

	return current_game.occupation_matrix

def get_direction_from_move(input_move):
	match input_move:
		case ">":
			direction = [0, 1]
		case "<":
			direction = [0, -1]
		case "u":
			direction = [1, 0]
		case "n":
			direction = [-1, 0]
		case _:
			raise ValueError("Invalid Value  (In Get Direction) : ", input_move)
	return direction
