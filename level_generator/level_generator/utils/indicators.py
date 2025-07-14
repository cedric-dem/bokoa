from level_generator.utils.level_with_sol_creation_functions import get_history_of_operations_for_given_solution_on_given_level, get_occupation_matrix_for_given_solution_on_given_level

def get_all_indicators(level):
	increasing_steps_counter = 0

	total_score_decreasing = 0
	total_score_increasing = 0

	latest_negative_score_at = 0

	operations = get_history_of_operations_for_given_solution_on_given_level(level.best_moves, level)
	occupation = get_occupation_matrix_for_given_solution_on_given_level(level.best_moves, level)
	scores_history = level.history_of_scores_for_best_solution

	current_case_estimate_difficulty = 1

	for current_score_index in range(len(level.history_of_scores_for_best_solution)):
		if current_score_index >= 1:
			old_score = level.history_of_scores_for_best_solution[current_score_index - 1]
			new_score = level.history_of_scores_for_best_solution[current_score_index]

			if new_score > old_score:
				increasing_steps_counter += 1
				total_score_increasing += (new_score - old_score)

			if new_score < old_score:
				total_score_decreasing += (old_score - new_score)

			if new_score < 0:
				latest_negative_score_at = current_score_index

		current_operation = operations[current_score_index - 1]

		progression_proportion = current_score_index / len(operations)

		match current_operation.operation:
			case "+":
				if current_score_index < 5:
					current_case_estimate_difficulty += 5 * (current_operation.operand + 5)
				else:
					current_case_estimate_difficulty += 2 * (current_operation.operand + 5)

			case '-':
				if current_score_index < 5:
					current_case_estimate_difficulty -= 5 * (current_operation.operand + 5)
				else:
					current_case_estimate_difficulty -= 2 * (current_operation.operand + 5)
			case '×':
				if current_score_index < 5:
					current_case_estimate_difficulty += 3 * (current_operation.operand + 5)
				else:
					current_case_estimate_difficulty += 7 * (current_operation.operand + 5)
			case '÷':
				if current_score_index < 5:
					current_case_estimate_difficulty -= 2 * (current_operation.operand + 5)
				else:
					current_case_estimate_difficulty -= 7 * (current_operation.operand + 5)
			case _:
				raise ValueError("Invalid Value  (Operation not found) : ", current_operation.operation)

	# TODO try with srqt or squared
	proportion_increasing_steps = -increasing_steps_counter / (len(level.history_of_scores_for_best_solution))
	proportion_score_decreasing = (total_score_decreasing / level.history_of_scores_for_best_solution[-1])

	lowest_score = - min(level.history_of_scores_for_best_solution)

	solution_length = len(level.history_of_scores_for_best_solution)

	operations_used_indicator = -round(current_case_estimate_difficulty, 2)

	# todo remove code duplication
	occupation_matrix = get_occupation_matrix_for_given_solution_on_given_level(level.best_moves, level)

	current_indicator_value = 0

	for i in range(len(occupation_matrix)):
		for j in range(len(occupation_matrix[i])):
			if not occupation_matrix[i][j]:
				this_unused_operation = level.operations_grid[i][j]
				if this_unused_operation.operation == "+":
					current_indicator_value += 3 + (2 * this_unused_operation.operand)

				elif this_unused_operation.operation == "×":
					current_indicator_value += 5 + (3 * this_unused_operation.operand)
	remaining_operations_indicator = current_indicator_value

	return [proportion_increasing_steps, proportion_score_decreasing, lowest_score, solution_length, latest_negative_score_at, operations_used_indicator, remaining_operations_indicator]
