from level_generator.utils.reduce_levels_functions import  get_complete_set_levels, get_reduced_set_levels

print('=====> Test Proportion of levels passed by each alorithm : ')

initial_set_of_levels = get_complete_set_levels()
reduced_set_of_levels = get_reduced_set_levels()

print('==>  Greedy ')
# TODO