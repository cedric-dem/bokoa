raw_levels_to_generate = 1000

number_levels_to_keep = 100

grid_sizes = [[4, 4], [5, 5], [6, 6]]

lowest_solution_sizes = [6, 12, 18]

grid_sizes_id = [i for i in range(len(grid_sizes))]

display_new_levels = True

coefficient_difficulty_first_term = 0.4
coefficient_difficulty_second_term = 0.6

# OLD
# coefficient_difficulty_first_term_a = [2.0998, 2.332, 1.92]
# coefficient_difficulty_first_term_b = [2.34, 2.666, 2.026]
# coefficient_difficulty_second_term_a = [0.826446281, 1.597444089, 1.34589502]

# NEW
coefficient_difficulty_first_term_a = [2.076923076923077, 2.2, 1.9109589041095891]
coefficient_difficulty_first_term_b = [2.3076923076923075, 2.4000000000000004, 2.017123287671233]
coefficient_difficulty_second_term_a = [0.8157894736842106, 1.5814696485623003, 1.3325587613008851]

generated_levels_folder_name = "generated_levels_published"

complete_folder_name = "complete"
reduced_folder_name = "reduced"

grid_size_folder_prefix = "grid_size_"

level_file_name = "level_"
