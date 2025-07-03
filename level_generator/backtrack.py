def is_move_in_bound(gm, new_pos):
	return new_pos[0] >= 0 and new_pos[1] >= 0 and new_pos[0] < gm.grid_size[1] and new_pos[1] < gm.grid_size[0]

def is_move_in_history(gm, new_pos):
	return new_pos in gm.position_history

def get_all_but_inverse_of_last_move(moves_history):
	if len(moves_history) == 0:
		return [[0, -1], [0, 1], [1, 0], [-1, 0]]

	elif moves_history[-1] == [1, 0]:
		return [[0, -1], [0, 1], [1, 0]]

	elif moves_history[-1] == [-1, 0]:
		return [[0, -1], [0, 1], [-1, 0]]

	elif moves_history[-1] == [0, -1]:
		return [[0, -1], [1, 0], [-1, 0]]

	elif moves_history[-1] == [0, 1]:
		return [[0, 1], [1, 0], [-1, 0]]

	else:
		print('Error')
		return None

def back_track(game, max_solution_size):
	current_best_score = game.score
	current_best_solution = game.moves_history[::]

	if len(game.moves_history) < max_solution_size:  # else stop
		for new_move in get_all_but_inverse_of_last_move(game.moves_history):

			new_position = [game.position_history[-1][0] + new_move[0], game.position_history[-1][1] + new_move[1]]

			##if move ok + not coming back
			if is_move_in_bound(game, new_position) and (not is_move_in_history(game, new_position)):
				# save old score
				old_score = game.score

				# move
				game.move(new_move)

				# launch backtrack
				temp_best_score, temp_best_moves = back_track(game, max_solution_size)

				##restore old state
				game.score = old_score
				game.moves_history.pop()
				game.position_history.pop()

				if current_best_score < temp_best_score:  # if new res better than prev:
					# current_best_score and current_best_solution refresh
					current_best_score = temp_best_score
					current_best_solution = temp_best_moves[::]

	return current_best_score, current_best_solution
