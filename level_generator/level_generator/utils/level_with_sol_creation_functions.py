from level_generator.classes.game import Game

def get_history_of_scores_for_given_solution_on_given_level(solution, level):
	current_game = Game(level)

	history_of_scores_for_best_solution = [1]

	for move in solution:
		move_direction = get_direction(move)
		current_game.move(move_direction)
		history_of_scores_for_best_solution.append(current_game.score)

	return history_of_scores_for_best_solution

def get_direction(move):
	if move == ">":
		result = [0, 1]

	elif move == "<":
		result = [0, -1]

	elif move == "u":
		result = [1, 0]

	elif move == "n":
		result = [-1, 0]

	return result
