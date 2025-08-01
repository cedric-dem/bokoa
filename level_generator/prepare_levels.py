from level_generator.utils.constant_computation import retrieve_all_constants
from level_generator.utils.display_functions import describe_levels_set_terminal, plot_all_graphs
from level_generator.utils.file_level_functions import save_all_levels
from level_generator.utils.misc_functions import get_boundaries, sort_levels_set
from level_generator.utils.reduce_levels_functions import reduce_levels_set, remove_out_of_bounds_levels, get_complete_set_levels, set_difficulty_for_all_levels, remove_duplicated

print("========> step 0: Retrieve initial set of levels")
initial_set_of_levels = get_complete_set_levels()

print("========> step 1: Retrieve Boundaries")
boundaries = get_boundaries(initial_set_of_levels)

print("========> step 2: retrieve constants")
constants = retrieve_all_constants(initial_set_of_levels)

print("========> step 3: compute difficulty")
set_difficulty_for_all_levels(initial_set_of_levels, constants)

print("========> step 4: initial sort")
sort_levels_set(initial_set_of_levels)

print("========> step 5: remove unacceptable levels (too big, too small, end score too high, end score too low, duplicated)")
# TODO maybe move step 5 before ? to ensure a flatter difficulty ?
acceptable_levels_set = remove_duplicated(remove_out_of_bounds_levels(initial_set_of_levels, boundaries))

print("========> step 6: acceptable sort")
sort_levels_set(acceptable_levels_set)

print("========> step 7: reduce level to desired quantity")
reduced_to_final_set = reduce_levels_set(acceptable_levels_set)

print("========> step 8: save levels")
save_all_levels(reduced_to_final_set)

print("========> step 9: show statistics in terminal")
describe_levels_set_terminal(initial_set_of_levels, "Initial Set Of Levels")
describe_levels_set_terminal(acceptable_levels_set, "Acceptable Levels")
describe_levels_set_terminal(reduced_to_final_set, "Reduced Set Of Levels")

print("========> step 10: plot statistics")
plot_all_graphs(
	[
		initial_set_of_levels,
		acceptable_levels_set,
		reduced_to_final_set
	],
	[
		"Initial Set Of Levels",
		"Acceptable Levels",
		"Reduced Set Of Levels",
	]
)
