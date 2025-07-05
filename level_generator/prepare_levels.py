from level_generator.utils.constant_computation import retrieve_all_constants
from level_generator.utils.display_functions import describe_all_grid_sizes
from level_generator.utils.file_level_functions import save_all_levels
from level_generator.utils.misc_functions import get_boundaries
from level_generator.utils.reduce_levels_functions import reduce_levels_set, remove_out_of_bounds_levels, get_all_levels, set_difficulty_for_all_levels

print("========> step 0: Retrieve initial set of levels")
initial_set_of_levels = get_all_levels()

print("========> step 1: Retrieve Boundaries")
boundaries = get_boundaries(initial_set_of_levels)

print("========> step 2: retrieve constants")
constants = retrieve_all_constants(initial_set_of_levels)

print("========> step 3: compute difficulty")
set_difficulty_for_all_levels(initial_set_of_levels, constants)

print("========> step 4: describe initial state of levels")
describe_all_grid_sizes(initial_set_of_levels, " Initial ")

print("========> step 5; remove unacceptable sizes")
#TODO maybe move step 5 before ? to ensure a flatter difficulty ?
acceptable_levels_set = remove_out_of_bounds_levels(initial_set_of_levels, boundaries)

print("========> step 6: describe level set after first reduce")
describe_all_grid_sizes(acceptable_levels_set, " Acceptable Levels ")

print("========> step 7: reduce level to desired quantity")
reduced_to_final_set = reduce_levels_set(acceptable_levels_set)

print("========> step 8: describe levels after second reduction")
describe_all_grid_sizes(reduced_to_final_set, " Reduced to final set ")

print("========> step 9: save levels")
save_all_levels(reduced_to_final_set)
