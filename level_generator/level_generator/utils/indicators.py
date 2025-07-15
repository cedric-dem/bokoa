from level_generator.utils.level_with_sol_creation_functions import get_history_of_operations_for_given_solution_on_given_level, get_occupation_matrix_for_given_solution_on_given_level

def get_all_indicators(level):
	increasing_steps_counter = 0

	total_score_decreasing = 0
	total_score_increasing = 0

	latest_negative_score_at = 0

	operations = get_history_of_operations_for_given_solution_on_given_level(level.solution, level)
	occupation_matrix = get_occupation_matrix_for_given_solution_on_given_level(level.solution, level)

	current_case_estimate_difficulty = 1

	for current_score_index in range(len(level.history_of_scores_for_solution)):
		if current_score_index >= 1:
			old_score = level.history_of_scores_for_solution[current_score_index - 1]
			new_score = level.history_of_scores_for_solution[current_score_index]

			if new_score > old_score:
				increasing_steps_counter += 1
				total_score_increasing += (new_score - old_score)

			if new_score < old_score:
				total_score_decreasing += (old_score - new_score)

			if new_score < 0:
				latest_negative_score_at = current_score_index

		progression_proportion = current_score_index / len(operations)

		current_case_estimate_difficulty += get_points_adjustment_difficulty(operations[current_score_index - 1], current_score_index)

	# TODO try with srqt or squared
	proportion_increasing_steps = -increasing_steps_counter / (len(level.history_of_scores_for_solution))
	proportion_score_decreasing = (total_score_decreasing / level.history_of_scores_for_solution[-1])
	lowest_score = - min(level.history_of_scores_for_solution)
	solution_length = len(level.history_of_scores_for_solution)
	operations_used_indicator = -round(current_case_estimate_difficulty, 2)
	remaining_operations_indicator = get_remaining_operations_indicator(occupation_matrix, level)

	return {
		"proportion_increasing_steps": proportion_increasing_steps,
		"proportion_score_decreasing": proportion_score_decreasing,
		"lowest_score": lowest_score,
		"solution_length": solution_length,
		"latest_negative_score_at": latest_negative_score_at,
		"operations_used": operations_used_indicator,
		"remaining_operations": remaining_operations_indicator
	}

def get_remaining_operations_indicator(occupation_matrix, level):
	remaining_operations_indicator = 0

	for matrix_line_index in range(len(occupation_matrix)):
		for matrix_column_index in range(len(occupation_matrix[matrix_line_index])):
			if not occupation_matrix[matrix_line_index][matrix_column_index]:
				this_unused_operation = level.operations_grid[matrix_line_index][matrix_column_index]
				if this_unused_operation.operator == "+":
					remaining_operations_indicator += 3 + (2 * this_unused_operation.operand)

				elif this_unused_operation.operator == "×":
					remaining_operations_indicator += 5 + (3 * this_unused_operation.operand)

	return remaining_operations_indicator

def get_points_adjustment_difficulty(current_operation, current_score_index):
	match current_operation.operator:
		case "+":
			if current_score_index < 5:
				result = 5 * (current_operation.operand + 5)
			else:
				result = 2 * (current_operation.operand + 5)

		case '-':
			if current_score_index < 5:
				result = - 5 * (current_operation.operand + 5)
			else:
				result = - 2 * (current_operation.operand + 5)
		case '×':
			if current_score_index < 5:
				result = 3 * (current_operation.operand + 5)
			else:
				result = 7 * (current_operation.operand + 5)
		case '÷':
			if current_score_index < 5:
				result = - 2 * (current_operation.operand + 5)
			else:
				result = - 7 * (current_operation.operand + 5)
		case _:
			raise ValueError("Invalid Value  (Operation not found) : ", current_operation.operator)
	return result
