from level_generator.utils.misc_heuristics import evaluate_heuristic_performance
from level_generator.utils.reduce_levels_functions import get_complete_set_levels, get_reduced_set_levels

print('=====> Test Proportion of levels passed by each heuristics : ')

# initial_set_of_levels = get_complete_set_levels()
reduced_set_of_levels = get_reduced_set_levels()

# tiny_portion= [grid_size[:10] for grid_size in reduced_set_of_levels]

# evaluate_heuristic_performance("Greedy", reduced_set_of_levels)
# evaluate_heuristic_performance("Advantage Matrix", reduced_set_of_levels)
# evaluate_heuristic_performance("BackTracking Limited Depth", reduced_set_of_levels)
evaluate_heuristic_performance("BackTracking With Score Check", reduced_set_of_levels)
