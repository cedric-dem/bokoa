from level_generator.utils.misc_functions import get_all_but_inverse_of_last_move

class Solver(object):
	def __init__(self, game):
		self.game = game

	def solve(self):
		# TODO
		pass

	def is_solution_worth_trying(self):
		# TODO
		return True

	def back_track_heuristic(self, game, max_solution_size):  # Common to all solvers : a backtracking

		current_best_score = game.score
		current_best_solution = None

		if len(game.moves_history) < max_solution_size:  # else stop
			for new_move in get_all_but_inverse_of_last_move(game.moves_history):

				new_position = [game.current_position_head[0] + new_move[0], game.current_position_head[1] + new_move[1]]

				##if move ok + not coming back
				if game.is_move_in_bound_and_not_in_history(new_position):

					if self.is_solution_worth_trying():
						# save old score
						old_score = game.score
						old_head_position = game.current_position_head

						# move
						game.apply_move_given_direction_and_new_pos(new_move, new_position)

						# launch backtrack
						temp_best_score, temp_best_moves = self.back_track_heuristic(game, max_solution_size)

						##restore old state
						game.score = old_score
						game.moves_history.pop()
						game.current_position_head = old_head_position

						# game.occupation_matrix[old_head_position[0]][old_head_position[1]] = False
						game.occupation_matrix[new_position[0]][new_position[1]] = False

						if current_best_score < temp_best_score:  # if new res better than prev:
							current_best_score = temp_best_score
							current_best_solution = temp_best_moves[::]

		if not current_best_solution:
			current_best_solution = game.moves_history[::]

		return current_best_score, current_best_solution
