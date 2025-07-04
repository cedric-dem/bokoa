from level_generator.utils.display_functions import describe_given_grid_size, describe_difficulty_terms, compare_fitness_functions
from level_generator.utils.misc_functions import *
from level_generator.utils.reduce_levels_functions import reduce_levels_set


for grid_size_id in grid_sizes_id:
	print('='*190)
	compare_fitness_functions(grid_size_id, raw_levels_to_generate)