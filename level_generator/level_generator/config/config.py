############################################# Common
grid_sizes = [[4, 4], [5, 5], [6, 6]]

format_json = True

generated_levels_folder_name = "generated_levels/temp_levels"

complete_folder_name = "complete"
reduced_folder_name = "reduced"

grid_size_folder_prefix = "grid_size_"

level_file_name = "level_"

############################################# Generate Levels
raw_levels_to_generate = 5

balance_operand = False

use_multiple_cores_for_levels_generation = True
n_cores = 6

save_plots = True

############################################# Prepare Levels
number_levels_to_keep = 4

ignore_extreme_values = 1  # will ignore top 1%, bottom 1% (scores and sizes)

weights_parameters = {
	"proportion_increasing_steps": 0.64,  # will use 0.95 later
	"proportion_score_decreasing": 0.06,  # will use 0.05 later ?
	"lowest_score": 0.06,
	"solution_length": 0.06,
	"latest_negative_score_at": 0.06,
	"operations_used": 0.06,
	"remaining_operations": 0.06
}

compute_constants = "AUTOMATIC"
compute_boundaries = "AUTOMATIC"

difficulty_setting = "linear"
