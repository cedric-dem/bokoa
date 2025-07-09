from level_generator.utils.misc_heuristics import evaluate_heuristic_performance
from level_generator.utils.reduce_levels_functions import get_complete_set_levels, get_reduced_set_levels

print('=====> Test Proportion of levels passed by each heuristics : ')

#set_of_levels = get_complete_set_levels()
set_of_levels = get_reduced_set_levels()
# set_of_levels = [levels_for_that_grid_size[:10] for levels_for_that_grid_size in get_reduced_set_levels()]

# evaluate_heuristic_performance("Greedy", set_of_levels)
evaluate_heuristic_performance("Advantage Matrix", set_of_levels)
# evaluate_heuristic_performance("BackTracking Limited Depth", set_of_levels)
# evaluate_heuristic_performance("BackTracking With Score Check", set_of_levels)
