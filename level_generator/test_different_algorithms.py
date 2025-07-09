from level_generator.utils.algorithms import evaluate_algorithm_performance
from level_generator.utils.reduce_levels_functions import  get_complete_set_levels

print('=====> Test Proportion of levels passed by each algorithm : ')

initial_set_of_levels = get_complete_set_levels()
# reduced_set_of_levels = get_reduced_set_levels()

evaluate_algorithm_performance("Greedy", initial_set_of_levels)
evaluate_algorithm_performance("Advantage Matrix", initial_set_of_levels)