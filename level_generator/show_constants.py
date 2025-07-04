from level_generator.utils.display_functions import  describe_difficulty_terms
from level_generator.utils.misc_functions import *

for grid_size_id in grid_sizes_id:
	print('=====> ',grid_size_id)
	describe_difficulty_terms(grid_size_id, raw_levels_to_generate)
	print()