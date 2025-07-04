from level_generator.utils.constant_computation import retrieve_all_constants
from level_generator.utils.display_functions import describe_given_grid_size
from level_generator.utils.misc_functions import *
from level_generator.utils.reduce_levels_functions import reduce_levels_set

print("========> step 0: retrieve constants")
constants = retrieve_all_constants()

print("========> step 1: describe complete set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(complete_folder_name, constants, grid_size_id, raw_levels_to_generate, " Complete")

print("========> step 2: reduce set of levels")
reduce_levels_set(constants)

print("========> step 3: describe reduced set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(reduced_folder_name, constants, grid_size_id, number_levels_to_keep, " Reduced")
