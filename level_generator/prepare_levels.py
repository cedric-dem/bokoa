from level_generator.utils.constant_computation import retrieve_all_constants
from level_generator.utils.display_functions import describe_given_grid_size
from level_generator.utils.file_level_functions import get_levels_list
from level_generator.utils.misc_functions import *
from level_generator.utils.reduce_levels_functions import reduce_levels_set, remove_unacceptable_sizes, get_all_levels, set_difficulty_for_all_levels

print("========> step 0: Retrieve initial set of levels")
initial_set_of_levels = get_all_levels()

print("========> step 1: retrieve constants")
constants = retrieve_all_constants(initial_set_of_levels)

print("========> step 2: compute difficulty")
set_difficulty_for_all_levels(initial_set_of_levels, constants)

print("========> step 3: describe initial state of levels")
for grid_size_id in range(len(initial_set_of_levels)):
	describe_given_grid_size(initial_set_of_levels[grid_size_id], constants, grid_size_id, " Initial ")

print("========> step 4; remove unacceptable sizes")
first_reduced_set=remove_unacceptable_sizes(initial_set_of_levels)

print("========> step 5: describe level set after first reduce")
for grid_size_id in range(len(first_reduced_set)):
	describe_given_grid_size(first_reduced_set[grid_size_id], constants, grid_size_id, " After First Reduction ")

print("========> step 6: reduce level to desired quantity")

print("========> step 7: describe levels after second reduction")


"""
print("========> step 0: retrieve constants")

print("========> step 1: describe complete set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(complete_folder_name, constants, grid_size_id, raw_levels_to_generate, " Complete")

print("========> step 2: first reduced set of levels")
pre_reduced_set=remove_unacceptable_sizes()

#TODO descreibe between 2 and 3

print("========> step 3: reduce reduced set of levels")
reduce_levels_set(constants,pre_reduced_set)

print("========> step 4: describe reduced set of levels")
for grid_size_id in grid_sizes_id:
	describe_given_grid_size(reduced_folder_name, constants, grid_size_id, number_levels_to_keep, " Reduced")

"""