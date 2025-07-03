import json
import time

from level_generator.classes.levelWithSolution import *
from level_generator.classes.level import *
from level_generator.utils.display_functions import describe_list, plot_all_evolutions, plot_graph

def get_complete_levels_list(grid_size_id, prefix, quantity):
	complete_levels_list = []

	for current_level_index in range(quantity):
		# load json :
		with open(prefix + str(current_level_index) + ".json", 'r', encoding = 'utf-8') as file:
			data = json.load(file)

			new_level = Level(grid_size_id, data["operations"])
			new_level_with_sol = LevelWithSolution(new_level, data["bestScore"], data["bestMoves"])
			complete_levels_list.append(new_level_with_sol)

	return complete_levels_list

def describe_given_grid_size(grid_size_id, prefix, quantity, levels_set_name):
	print('====> Current prefix :', prefix)

	complete_levels_list = get_complete_levels_list(grid_size_id, prefix, quantity)

	print("====> Number of levels :  ", len(complete_levels_list))

	# ==== get stats
	scores, sizes, fitness = [], [], []

	for data in complete_levels_list:
		data.set_fitness_score()

		scores.append(data.best_score)
		sizes.append(len(data.best_moves))
		fitness.append(data.estimated_difficulty)

	# ==== Describe stats in terminal
	describe_list("Scores", scores)
	describe_list("Sizes", sizes)
	describe_list("Fitness", fitness)

	# ==== Display stats as plots

	plot_all_evolutions(complete_levels_list, levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]))

	scores.sort()
	fitness.sort()
	sizes.sort()

	plot_graph(scores, "All final scores" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Final Score")
	plot_graph(fitness, "All fitness" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Fitness Score")
	plot_graph(sizes, "All sizes" + levels_set_name + "  - Grid  size : " + str(grid_sizes[grid_size_id]), "Level ID", "Best Solution Size")

def create_level_file(level, filename):
	create_level_file_as_json(level.operations_grid.operations_grid, level.best_score, level.best_moves, filename + ".json")

def get_index_of_closest_from(to_search, levels_list):
	closest_index = 0
	closest_distance = float("inf")

	for current_index in range(len(levels_list)):
		this_distance = abs(to_search - levels_list[current_index].estimated_difficulty)
		if closest_distance > this_distance:
			closest_index = current_index
			closest_distance = this_distance

	return closest_index

def get_levels_size_acceptable(complete_levels_list, current_grid_size_id):
	levels_size_acceptable = []
	lowest_size = lowest_solution_sizes[current_grid_size_id]

	for current_level in complete_levels_list:
		if len(current_level.best_moves) >= lowest_size:
			levels_size_acceptable.append(current_level)
	return levels_size_acceptable

def reduce_levels_set():
	for current_grid_size_id in grid_sizes_id:
		reduce_levels_set_given_grid_size_id(current_grid_size_id)

def reduce_levels_set_given_grid_size_id(current_grid_size_id):
	print('====> Current grid size id ', current_grid_size_id)

	complete_levels_list = get_complete_levels_list(current_grid_size_id, get_file_prefix_complete(current_grid_size_id), raw_levels_to_generate)
	print("====>  Initially total of  ", len(complete_levels_list), " levels")

	levels_size_acceptable = get_levels_size_acceptable(complete_levels_list, current_grid_size_id)
	print("====>  After remove too small levels total of  ", len(levels_size_acceptable), " levels")

	# ===== set fitness of kept levels
	for current_level in levels_size_acceptable:
		current_level.set_fitness_score()

	# ====  sort kept levels
	levels_size_acceptable.sort()

	# ==== Display infos

	fitness = []
	for current_level in levels_size_acceptable:
		fitness.append(current_level.estimated_difficulty)

	# ==== get theoretical fitness to reduce
	theoretical_fitness = get_theoretical_fitness(levels_size_acceptable)

	levels_reduced = get_reduced_levels(theoretical_fitness, levels_size_acceptable)

	fitness = [current_level.estimated_difficulty for current_level in levels_reduced]
	print("====> Real Fitness : ", fitness)

	for index_reduced in range(len(levels_reduced)):
		current_level = levels_reduced[index_reduced]

		create_level_file_as_json(
			current_level.level.operations_grid,
			current_level.best_score,
			current_level.best_moves,
			get_file_prefix_reduced(current_grid_size_id) + str(index_reduced) + ".json"
		)

	print("====>  Keeping ", len(levels_reduced), " levels")

def get_reduced_levels(theoretical_fitness, levels_size_acceptable):
	levels_reduced = []

	for reduced_levels_index in range(number_levels_to_keep):
		index = get_index_of_closest_from(theoretical_fitness[reduced_levels_index], levels_size_acceptable)
		this_one = levels_size_acceptable.pop(index)
		levels_reduced.append(this_one)
	levels_reduced.sort()
	return levels_reduced

def get_theoretical_fitness(levels_list):
	theoretical_fitness = []

	average_step = (levels_list[-1].estimated_difficulty - levels_list[0].estimated_difficulty) / number_levels_to_keep

	current = levels_list[0].estimated_difficulty

	for reduced_levels_index in range(number_levels_to_keep):
		theoretical_fitness.append(current)
		current += average_step

	print('====> Average step', average_step)
	print("====> Theoretical fitness : ", theoretical_fitness)
	return theoretical_fitness

def create_level_file_as_json(operations, best_score, best_moves, filename):
	result = {
		"operations": operations,
		"bestScore": round(float(best_score), 2),
		"bestMoves": best_moves
	}

	with open(filename, 'w') as file:
		json.dump(result, file, indent = 4, separators = (',', ': '), ensure_ascii = False)

def get_file_prefix_complete(grid_size_index):
	return generated_levels_folder_name + "/" + complete_folder_name + "/" + grid_size_folder_prefix + str(grid_size_index) + "/" + level_file_name

def get_file_prefix_reduced(grid_size_index):
	return generated_levels_folder_name + "/" + reduced_folder_name + "/" + grid_size_folder_prefix + str(grid_size_index) + "/" + level_file_name

def get_readable_moves(moves_list):
	result = []
	for move in moves_list:
		if move == [0, -1]:
			result.append('<')

		elif move == [0, 1]:
			result.append('>')

		elif move == [1, 0]:
			result.append('u')

		elif move == [-1, 0]:
			result.append('n')

	return result

def create_one_level(grid_size_id, fn):
	# create level
	temp_level = Level(grid_size_id, None)

	# create game
	temp_game = Game(temp_level)

	# do the backtrack
	grid_size = grid_sizes[grid_size_id]
	best_score, best_moves = back_track(temp_game, grid_size[0] * grid_size[1])

	# save level with solution as json
	create_level_file_as_json(temp_level.operations_grid, best_score, get_readable_moves(best_moves), fn)

def create_levels():
	for grid_size_id in grid_sizes_id:
		grid_size = grid_sizes[grid_size_id]
		prefix = get_file_prefix_complete(grid_size_id)

		print("Currently on size ", grid_size, " prefix", prefix)

		t0 = time.time()

		for current_level_index in range(raw_levels_to_generate):
			print("==> generate level", current_level_index)
			create_one_level(grid_size_id, prefix + str(current_level_index) + ".json")
			print(current_level_index + 1, "/", raw_levels_to_generate, " finished")

		t1 = time.time()

		print("Time taken : " + str((t1 - t0) / raw_levels_to_generate) + ' seconds per it')

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
