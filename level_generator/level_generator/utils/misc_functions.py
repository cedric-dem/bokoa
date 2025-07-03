import time

from level_generator.classes.game import Game
from level_generator.classes.level import *
from level_generator.utils.file_level_functions import get_level_path_complete, create_level_file_as_json
from level_generator.config.config import *

def get_move_from_direction(move):
	match move:
		case [0, -1]:
			result = '<'
		case [0, 1]:
			result = '>'
		case [1, 0]:
			result = 'u'
		case [-1, 0]:
			result = 'n'
		case _:
			raise ValueError("Invalid Value  (in Get Move) : ", move)
	return result

def get_readable_moves(moves_list):
	result = []
	for move in moves_list:
		result.append(get_move_from_direction(move))

	return result

def create_a_level_and_solution(grid_size_id, fn):
	# create level
	temp_level = Level(grid_size_id, None)

	# create game
	temp_game = Game(temp_level)

	# do the backtrack
	grid_size = grid_sizes[grid_size_id]
	best_score, best_moves = back_track(temp_game, grid_size[0] * grid_size[1])

	# save level with solution as json
	create_level_file_as_json(temp_level.operations_grid, best_score, get_readable_moves(best_moves), fn)

def create_levels_and_solutions():
	for grid_size_id in grid_sizes_id:
		grid_size = grid_sizes[grid_size_id]

		print("Currently on size ", grid_size)

		t0 = time.time()

		for current_level_index in range(raw_levels_to_generate):
			print("==> generate level", current_level_index)
			path = get_level_path_complete(grid_size_id, current_level_index)
			create_a_level_and_solution(grid_size_id, path)
			print(current_level_index + 1, "/", raw_levels_to_generate, " finished")

		t1 = time.time()

		print("Time taken : " + str((t1 - t0) / raw_levels_to_generate) + ' seconds per it')

def get_all_but_inverse_of_last_move(moves_history):
	directions = [[0, -1], [0, 1], [1, 0], [-1, 0]]
	if len(moves_history) == 0:
		result = directions
	else:
		last_move = moves_history[-1]
		inverse = [-last_move[0], -last_move[1]]
		result = [d for d in directions if d != inverse]
	return result

def back_track(game, max_solution_size):
	current_best_score = game.score
	current_best_solution = game.moves_history[::]

	if len(game.moves_history) < max_solution_size:  # else stop
		for new_move in get_all_but_inverse_of_last_move(game.moves_history):

			new_position = [game.position_history[-1][0] + new_move[0], game.position_history[-1][1] + new_move[1]]

			##if move ok + not coming back
			if game.is_move_in_bound(new_position) and (not game.is_move_in_history(new_position)):
				# save old score
				old_score = game.score

				# move
				game.apply_move(new_move)

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
