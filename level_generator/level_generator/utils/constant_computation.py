from level_generator.config.config import grid_sizes, compute_constants, grid_sizes_id, raw_levels_to_generate, complete_folder_name
from level_generator.utils.display_functions import describe_list
from level_generator.utils.file_level_functions import get_levels_list

def get_coef_affine(min_value, max_value):
	K1 = -min_value / (max_value - min_value)
	K2 = 1 / (max_value - min_value)
	return K1, K2

def get_coef_linear(max_value):
	K2 = 1 / (max_value)
	return K2

def retrieve_all_constants(set_of_levels):
	if compute_constants:
		t1, t2, t3 = [], [], []
		for grid_size_id in grid_sizes_id:
			print('=' * 190)
			print('====> Current grid size :', grid_sizes[grid_size_id])
			tt1, tt2, tt3 = retrieve_constants_automatically(set_of_levels[grid_size_id], raw_levels_to_generate)

			t1.append(tt1)
			t2.append(tt2)
			t3.append(tt3)
	else:
		# OLD
		# t1 = [2.0998, 2.332, 1.92]
		# t2 = [2.34, 2.666, 2.026]
		# t3 = [0.826446281, 1.597444089, 1.34589502]

		# NEW
		t1 = [2.076923076923077, 2.2, 1.9109589041095891]
		t2 = [2.3076923076923075, 2.4000000000000004, 2.017123287671233]
		t3 = [0.8157894736842106, 1.5814696485623003, 1.3325587613008851]

	return {
		"coefficient_difficulty_first_term_a": t1,
		"coefficient_difficulty_first_term_b": t2,
		"coefficient_difficulty_second_term_a": t3
	}

def retrieve_constants_automatically(complete_levels_list, quantity):
	print('====> Retrieving automatically constants')

	# ==== get stats
	first_term_raw, second_term_raw = [], []

	for data in complete_levels_list:
		data.compute_raw_terms()

		first_term_raw.append(data.first_term_raw)
		second_term_raw.append(data.second_term_raw)

	coefficient_difficulty_first_term_a, coefficient_difficulty_first_term_b = get_coef_affine(min(first_term_raw), max(first_term_raw))
	coefficient_difficulty_second_term_a = get_coef_linear(max(second_term_raw))

	print("==> Computed coefficients :", coefficient_difficulty_first_term_a, coefficient_difficulty_first_term_b, coefficient_difficulty_second_term_a)

	describe_list("Difficulty Term 1 Raw", first_term_raw)
	describe_list("Difficulty Term 2 Raw", second_term_raw)

	return coefficient_difficulty_first_term_a, coefficient_difficulty_first_term_b, coefficient_difficulty_second_term_a
