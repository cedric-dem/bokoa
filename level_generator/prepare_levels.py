from level_generator.utils.misc import *

print("========> step 1: describe complete set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(grid_size_id, get_file_prefix_complete(grid_size_id), raw_levels_to_generate, " Complete")

print("========> step 2: reduce set of levels")
reduce_levels_set()

print("========> step 3: describe reduced set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(grid_size_id, get_file_prefix_reduced(grid_size_id), number_levels_to_keep, " Reduced")
