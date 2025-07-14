def get_all_indicators(level):
	increasing_steps_counter = 0

	total_score_decreasing = 0
	total_score_increasing = 0

	for current_score_index in range(1, len(level.history_of_scores_for_best_solution)):
		old_score = level.history_of_scores_for_best_solution[current_score_index - 1]
		new_score = level.history_of_scores_for_best_solution[current_score_index]

		if new_score > old_score:
			increasing_steps_counter += 1
			total_score_increasing += (new_score - old_score)

		if new_score < old_score:
			total_score_decreasing += (old_score - new_score)

	# TODO try with srqt or squared
	first_term_raw = -increasing_steps_counter / (len(level.history_of_scores_for_best_solution))
	second_term_raw = (total_score_decreasing / level.history_of_scores_for_best_solution[-1])

	"""
	lst_operations = get_history_of_operations_for_given_solution_on_given_level(self.best_moves, self)
	occupation_matrix = get_occupation_matrix_for_given_solution_on_given_level(self.best_moves, self)
	third_term = get_points_estimate(lst_operations, occupation_matrix, self.history_of_scores_for_best_solution, self.best_moves, self.operations_grid)
	"""

	return [first_term_raw, second_term_raw]