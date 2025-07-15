from level_generator.classes.game import Game

def get_history_of_scores_for_given_solution_on_given_level(solution, level):
	current_game = Game(level)

	history_of_scores = [1]

	for current_move in solution:
		move_direction = get_direction_from_move(current_move)

		current_game.apply_move_given_direction(move_direction)
		history_of_scores.append(current_game.score)

	return history_of_scores

def get_history_of_operations_for_given_solution_on_given_level(solution, level):  # TODO : merge this function and above
	current_game = Game(level)

	history_of_operations = []
	# level.display_level()
	for current_move in solution:
		move_direction = get_direction_from_move(current_move)

		current_game.apply_move_given_direction(move_direction)

		new_operation = current_game.level.operations_grid[current_game.current_cursor_position[0]][current_game.current_cursor_position[1]]

		history_of_operations.append(new_operation)

	return history_of_operations

def get_occupation_matrix_for_given_solution_on_given_level(solution, level):  # TODO : merge this function and the two above
	current_game = Game(level)

	for current_move in solution:
		move_direction = get_direction_from_move(current_move)

		current_game.apply_move_given_direction(move_direction)

	return current_game.occupation_matrix

def get_direction_from_move(move):
	match move:
		case ">":
			direction = [0, 1]
		case "<":
			direction = [0, -1]
		case "u":
			direction = [1, 0]
		case "n":
			direction = [-1, 0]
		case _:
			raise ValueError("Invalid Value  (In Get Direction) : ", move)
	return direction
