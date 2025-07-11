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

ignore_extreme_values = 1  # will ignore top 10%, bottom 10% (scores and sizes)

coefficient_difficulty_first_term = 0.4
coefficient_difficulty_second_term = 0.6

compute_constants = "AUTOMATIC"
compute_boundaries = "AUTOMATIC"

difficulty_setting = "linear"
difficulty_function = "points_estimate"  # "sum_two_terms"
