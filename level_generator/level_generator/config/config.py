############################################# Common
grid_sizes = [[4, 4], [5, 5], [6, 6]]

format_json = True

generated_levels_folder_name = "generated_levels/generated_levels_new_balanced"

complete_folder_name = "complete"
reduced_folder_name = "reduced"

grid_size_folder_prefix = "grid_size_"

level_file_name = "level_"

############################################# Generate Levels
raw_levels_to_generate = 1000

balance_operand = True

use_multiple_cores_for_levels_generation = True
n_cores = 6

############################################# Prepare Levels
number_levels_to_keep = 100

ignore_extreme_values = 1  # will ignore top 1%, bottom 1% (scores and sizes)

weights_parameters = [0.4, 0.6, 0, 0, 0, 0, 0]  # will use   [0.95, 0.05, ?, ?, ?, ?, ?] later

compute_constants = "AUTOMATIC"
compute_boundaries = "AUTOMATIC"

difficulty_setting = "linear"
difficulty_function = "sum_two_terms"  # "points_estimate" "sum_two_terms" "hardcoded_constants_sum_two_terms"
