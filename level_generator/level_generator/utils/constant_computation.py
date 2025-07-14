from level_generator.config.config import grid_sizes, compute_constants, weights_parameters
from level_generator.utils.display_functions import describe_list

def get_coef_affine(min_value, max_value):
	first_coef = -min_value / (max_value - min_value)
	second_coef = 1 / (max_value - min_value)
	return first_coef, second_coef

def retrieve_all_constants(set_of_levels):
	match compute_constants:
		case "AUTOMATIC":

			# result = [[[], []] for _ in range(len(weights_parameters))]
			result = {}
			for w in weights_parameters:
				result[w] = [[], []]

			for grid_size_id in range(len(grid_sizes)):
				print('=' * 190)
				print('====> Retrieving Automatically constants  grid size :', grid_sizes[grid_size_id])

				current_grid_size_constants = retrieve_constants_automatically(set_of_levels[grid_size_id])

				for current_constant_name in current_grid_size_constants:
					result[current_constant_name][0].append(current_grid_size_constants[current_constant_name][0])
					result[current_constant_name][1].append(current_grid_size_constants[current_constant_name][1])

		case "USE_OLD":
			print('====> Retrieving HardCoded old constants ')

			result = [
				[
					[2.0998, 2.332, 1.92],
					[2.34, 2.666, 2.026]
				],
				[
					[0.00, 0.00, 0.00],
					[0.826446281, 1.597444089, 1.34589502],
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				]
			]

		case "USE_NEW":
			print('====> Retrieving HardCoded new constants ')

			result = [
				[
					[1.8181818181818183, 2.0909090909090913, 2.391304347826087],
					[2.045454545454546, 2.2809917355371905, 2.608695652173913]
				],
				[
					[-0.0, -0.0, -0.0],
					[0.9677419354838711, 0.873015873015873, 1.33217764193335]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				],
				[
					[0, 0, 0],
					[0, 0, 0]
				]
			]

		case _:
			raise ValueError("Invalid compute constant method : ", compute_constants)

	return result

def retrieve_constants_automatically(complete_levels_list):
	# ==== get stats
	# raw_terms = [[] for _ in range(len(weights_parameters))]
	raw_terms = {}
	for w in weights_parameters:
		raw_terms[w] = []

	for data in complete_levels_list:
		data.compute_raw_terms()

		this_raw_terms = data.raw_terms

		# for raw_term_name in range(len(this_raw_terms)):
		#	raw_terms[raw_term_name].append(this_raw_terms[raw_term_name])
		for w in weights_parameters:
			raw_terms[w].append(this_raw_terms[w])

	coefficients = {}
	for raw_term_name in raw_terms:
		coefficient_difficulty_a, coefficient_difficulty_b = get_coef_affine(min(raw_terms[raw_term_name]), max(raw_terms[raw_term_name]))

		describe_list("Difficulty Term 2 Raw", raw_terms[raw_term_name])
		print("==> Computed coefficients for index :", raw_term_name, coefficient_difficulty_a, coefficient_difficulty_b)
		# coefficients.append([coefficient_difficulty_a, coefficient_difficulty_b])
		coefficients[raw_term_name] = [coefficient_difficulty_a, coefficient_difficulty_b]

	print("==> Result ", coefficients)
	return coefficients
