from level_generator.utils.display_functions import describe_given_grid_size, describe_difficulty_terms
from level_generator.utils.misc_functions import *
from level_generator.utils.reduce_levels_functions import reduce_levels_set

print("========> step 1: describe complete set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(grid_size_id, raw_levels_to_generate, " Complete")

print("========> step 2: display difficulty terms")
for grid_size_id in grid_sizes_id:
	describe_difficulty_terms(grid_size_id, raw_levels_to_generate)

print("========> step 3: reduce set of levels")
reduce_levels_set()

print("========> step 4: describe reduced set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(grid_size_id, number_levels_to_keep, " Reduced")
