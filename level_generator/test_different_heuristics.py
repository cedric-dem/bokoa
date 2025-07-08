from level_generator.utils.misc_heuristics import test_proportion_of_every_variant_every_solver
from level_generator.utils.reduce_levels_functions import get_complete_set_levels, get_reduced_set_levels

print('=====> retrieve data')
# set_of_levels = get_complete_set_levels()
# set_of_levels = get_reduced_set_levels()
set_of_levels = [levels_for_that_grid_size[:2] for levels_for_that_grid_size in get_reduced_set_levels()]

print('=====> Test Proportion of levels passed by each heuristics : ')
test_proportion_of_every_variant_every_solver(set_of_levels)
