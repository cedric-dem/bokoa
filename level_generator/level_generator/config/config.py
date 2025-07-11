############################################# Common
grid_sizes = [[4, 4], [5, 5], [6, 6]]

format_json = True

generated_levels_folder_name = "generated_levels/generated_levels_new_balanced_final"

complete_folder_name = "complete"
reduced_folder_name = "reduced"

grid_size_folder_prefix = "grid_size_"

level_file_name = "level_"

############################################# Generate Levels
raw_levels_to_generate = 1000

balance_operands = True

use_multiple_cores_for_levels_generation = False
n_cores = 6

save_plots = True

############################################# Prepare Levels
number_levels_to_keep = 100

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
"""
####################################### configs to test
"proportion_increasing_steps": 0.5
"remaining_operations": 0.25,
"lowest_score": 0.125,
"latest_negative_score_at": 0.03125,
"proportion_score_decreasing": 0.03125,
"solution_length": 0.03125,
"operations_used": 0.03125,

####################################### 
"proportion_increasing_steps": 0.4
"remaining_operations": 0.4,
"lowest_score": 0.1,
"latest_negative_score_at": 0.025,
"proportion_score_decreasing": 0.025,
"solution_length": 0.025,
"operations_used": 0.025,
"""

compute_constants = "AUTOMATIC"
compute_boundaries = "AUTOMATIC"

difficulty_setting = "linear"
