############################################# Common
grid_sizes = [[4, 4], [5, 5], [6, 6]]

format_json = True

generated_levels_folder_name = "generated_levels/generated_levels_published"

complete_folder_name = "complete"
reduced_folder_name = "reduced"

grid_size_folder_prefix = "grid_size_"

level_file_name = "level_"

############################################# Generate Levels
raw_levels_to_generate = 1000

balance_operand = True

use_multiple_cores_for_levels_generation = True
n_cores = 6

save_plots = True

############################################# Prepare Levels
number_levels_to_keep = 100

ignore_extreme_values = 10  # will ignore top 1%, bottom 1% (scores and sizes)

weights_parameters = {
	"proportion_increasing_steps": 0.4,
	"proportion_score_decreasing": 0.6,
	"lowest_score": 0,
	"solution_length": 0,
	"latest_negative_score_at": 0,
	"operations_used": 0,
	"remaining_operations": 0
}

compute_constants = "USE_OLD"
compute_boundaries = "USE_OLD"

difficulty_setting = "linear"
