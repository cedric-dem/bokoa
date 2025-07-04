from level_generator.utils.display_functions import describe_given_grid_size
from level_generator.utils.file_level_functions import get_file_prefix_complete, get_file_prefix_reduced
from level_generator.utils.misc_functions import *
from level_generator.utils.reduce_levels_functions import reduce_levels_set

print("========> step 1: describe complete set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(grid_size_id, get_file_prefix_complete(grid_size_id), raw_levels_to_generate, " Complete")

print("========> step 2: reduce set of levels")
reduce_levels_set()

print("========> step 3: describe reduced set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(grid_size_id, get_file_prefix_reduced(grid_size_id), number_levels_to_keep, " Reduced")
