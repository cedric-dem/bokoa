from level_generator.utils.misc_functions import *

for grid_size_id in range(len(grid_sizes)):
	print("==> Generating levels for grid size  ", grid_sizes[grid_size_id])
	create_levels_and_solutions(grid_size_id)
	print()
