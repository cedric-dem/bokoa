from level_generator.config.config import grid_sizes, compute_constants, weights_parameters
from level_generator.utils.display_functions import describe_list

def get_coef_affine(min_value, max_value):
	first_coef = -min_value / (max_value - min_value)
	second_coef = 1 / (max_value - min_value)
	return first_coef, second_coef

def retrieve_all_constants(set_of_levels):
	match compute_constants:
		case "AUTOMATIC":
			t1, t2, t3, t4 = [], [], [], []
			for grid_size_id in range(len(grid_sizes)):
				print('=' * 190)
				print('====> Retrieving Automatically constants  grid size :', grid_sizes[grid_size_id])
				[tt1, tt2], [tt3, tt4] = retrieve_constants_automatically(set_of_levels[grid_size_id])

				t1.append(tt1)
				t2.append(tt2)
				t3.append(tt3)
				t4.append(tt4)

		case "USE_OLD":
			print('====> Retrieving HardCoded old constants ')
			t1 = [2.0998, 2.332, 1.92]
			t2 = [2.34, 2.666, 2.026]
			t3 = [0.826446281, 1.597444089, 1.34589502]
			t4 = [1.00, 0.00, 0.00]

		case "USE_NEW":
			print('====> Retrieving HardCoded new constants ')
			t1 = [2.076923076923077, 2.2, 1.9109589041095891]
			t2 = [2.3076923076923075, 2.4000000000000004, 2.017123287671233]
			t3 = [0.8157894736842106, 1.5814696485623003, 1.3325587613008851]
			t4 = [1.00, 0.00, 0.00]

		case _:
			raise ValueError("Invalid compute constant method : ", compute_constants)

	return [
		[t1, t2],
		[t3, t4]
	]

def retrieve_constants_automatically(complete_levels_list):
	# ==== get stats
	raw_terms = [[] for _ in range(len(weights_parameters))]

	for data in complete_levels_list:
		data.compute_raw_terms()

		this_raw_terms = data.raw_terms

		for raw_term_index in range(len(this_raw_terms)):
			raw_terms[raw_term_index].append(this_raw_terms[raw_term_index])

	coefficients = []
	for raw_term_index in range(len(raw_terms)):
		coefficient_difficulty_a, coefficient_difficulty_b = get_coef_affine(min(raw_terms[raw_term_index]), max(raw_terms[raw_term_index]))

		describe_list("Difficulty Term 2 Raw", raw_terms[raw_term_index])
		print("==> Computed coefficients for index :", raw_term_index, coefficient_difficulty_a, coefficient_difficulty_b)
		coefficients.append([coefficient_difficulty_a, coefficient_difficulty_b])

	print("==> Result ", coefficients)
	return coefficients
