from level_generator.config.config import grid_sizes, compute_constants, weights_parameters

def get_offset(delta, min_value):
	return -min_value / delta

def get_multiply_factor(delta):
	return 1 / delta

def get_constants_automatically(set_of_levels):
	result = {name: [[], []] for name in weights_parameters}

	for grid_size_id in range(len(grid_sizes)):
		print('====> Retrieving Automatically constants  grid size :', grid_sizes[grid_size_id])

		current_grid_size_constants = retrieve_constants_automatically(set_of_levels[grid_size_id])

		for current_constant_name in current_grid_size_constants:
			result[current_constant_name][0].append(current_grid_size_constants[current_constant_name][0])
			result[current_constant_name][1].append(current_grid_size_constants[current_constant_name][1])
	return result

def get_constants_old():
	return {
		"proportion_increasing_steps": [
			[2.0998, 2.332, 1.92],
			[2.34, 2.666, 2.026]
		],
		"proportion_score_decreasing": [
			[0.00, 0.00, 0.00],
			[0.826446281, 1.597444089, 1.34589502],
		],
		"lowest_score": [
			[0, 0, 0],
			[0, 0, 0]
		],
		"solution_length": [
			[0, 0, 0],
			[0, 0, 0]
		],
		"latest_negative_score_at": [
			[0, 0, 0],
			[0, 0, 0]
		],
		"operations_used": [
			[0, 0, 0],
			[0, 0, 0]
		],
		"remaining_operations": [
			[0, 0, 0],
			[0, 0, 0]
		]
	}

def get_constants_new():
	return {
		"proportion_increasing_steps": [
			[1.8181818181818183, 2.0909090909090913, 2.391304347826087],
			[2.045454545454546, 2.2809917355371905, 2.608695652173913]
		],
		"proportion_score_decreasing": [
			[-0.0, -0.0, -0.0],
			[0.9677419354838711, 0.873015873015873, 1.33217764193335]
		],
		"lowest_score": [
			[0, 0, 0],
			[0, 0, 0]
		],
		"solution_length": [
			[0, 0, 0],
			[0, 0, 0]
		],
		"latest_negative_score_at": [
			[0, 0, 0],
			[0, 0, 0]
		],
		"operations_used": [
			[0, 0, 0],
			[0, 0, 0]
		],
		"remaining_operations": [
			[0, 0, 0],
			[0, 0, 0]
		]
	}

def retrieve_all_constants(set_of_levels):
	match compute_constants:
		case "AUTOMATIC":
			result = get_constants_automatically(set_of_levels)

		case "USE_OLD":
			print('====> Retrieving HardCoded old constants ')
			result = get_constants_old()

		case "USE_NEW":
			print('====> Retrieving HardCoded new constants ')
			result = get_constants_new()

		case _:
			raise ValueError("Invalid compute constant method : ", compute_constants)

	return result

def retrieve_constants_automatically(complete_levels_list):
	raw_terms = get_all_raw_terms(complete_levels_list)

	coefficients = {}
	for raw_term_name in raw_terms:
		min_raw_term = min(raw_terms[raw_term_name])
		max_raw_term = max(raw_terms[raw_term_name])

		delta = max_raw_term - min_raw_term

		this_term_offset = get_offset(delta, min_raw_term)
		this_term_multiply_factor = get_multiply_factor(delta)

		# describe_list("Difficulty Term Raw", raw_terms[raw_term_name])
		# print("==> Computed coefficients for index :", raw_term_name, this_term_offset, this_term_multiply_factor)

		coefficients[raw_term_name] = [this_term_offset, this_term_multiply_factor]

	print("==> Result ", coefficients)
	return coefficients

def get_all_raw_terms(complete_levels_list):
	raw_terms = {name: [] for name in weights_parameters}

	for level in complete_levels_list:
		level.compute_raw_terms()

		this_raw_terms = level.raw_difficulty_terms

		for current_constant_name in weights_parameters:
			raw_terms[current_constant_name].append(this_raw_terms[current_constant_name])
	return raw_terms
