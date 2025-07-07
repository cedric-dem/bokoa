from level_generator.classes.game import Game

def get_history_of_scores_for_given_solution_on_given_level(solution, level):
	current_game = Game(level)

	history_of_scores_for_best_solution = [1]

	for move in solution:
		move_direction = get_direction_from_move(move)

		current_game.apply_move_given_direction(move_direction)
		history_of_scores_for_best_solution.append(current_game.score)

	return history_of_scores_for_best_solution

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
