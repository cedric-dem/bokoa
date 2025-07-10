from level_generator.heuristics_solver.backtrack_with_limited_depth import BackTrackingLimitedDepthSolver
from level_generator.heuristics_solver.backtrack_with_score_check import BackTrackingWithScoreCheckSolver
from level_generator.heuristics_solver.greedy import GreedySolver
from level_generator.heuristics_solver.advantage_matrix import AdvantageMatrixSolver
import time

from level_generator.utils.display_functions import display_performance_time_heuristic, plot_performance_of_each_solver, plot_quantity_predictor_passing_each_levels

def evaluate_heuristic_performance(name, variant, levels_set):
	print('====> Evaluate heuristic: ', name, "variant ", variant)

	accuracy_total = []
	time_taken = []

	for grid_size_index in range(len(levels_set)):
		t0 = time.time()
		reached_goal = 0
		# print("==> on grid size ", grid_sizes[grid_size_index], " levels quantity : ", len(levels_set[grid_size_index]))
		for level_index in range(len(levels_set[grid_size_index])):
			reached_score = get_score_of_a_given_level_solved_using_given_heuristic(name, variant, levels_set[grid_size_index][level_index])

			this_goal = levels_set[grid_size_index][level_index].best_score
			# print("=> level", level_index, " goal ", this_goal, "reached : ", reached_score)

			passed = abs(reached_score - this_goal) < 0.01
			if passed:
				reached_goal += 1

			complete_name = name + ' ( variant ' + str(variant) + ' )'

			# TODO : refactor handling of this
			levels_set[grid_size_index][level_index].predictions_of_heuristics[complete_name] = passed

		t1 = time.time()
		accuracy_total.append(round(reached_goal / len(levels_set[grid_size_index]), 4))
		time_taken.append(round((t1 - t0) / len(levels_set[grid_size_index]), 4))

	print('==> Performance : ', accuracy_total, " time taken: ", time_taken)
	return accuracy_total, time_taken

def get_score_of_a_given_level_solved_using_given_heuristic(heuristic_name, variant, level):
	match heuristic_name:
		case 'Greedy':
			solver = GreedySolver(level, variant)
		case 'Advantage Matrix':
			solver = AdvantageMatrixSolver(level, variant)
		case "BackTracking Limited Depth":
			solver = BackTrackingLimitedDepthSolver(level, variant)
		case "BackTracking With Score Check":
			solver = BackTrackingWithScoreCheckSolver(level, variant)
		case _:
			raise ValueError("Invalid heuristic ")

	final_score = solver.solve()

	return final_score

def test_proportion_of_every_variant_every_solver(set_of_levels):
	print('=> Levels quantity', [len(set_of_levels[grid_size_index]) for grid_size_index in range(len(set_of_levels))])

	list_heuristics_to_test = [
		("Greedy", 0),
		("Greedy", 1),
		("BackTracking Limited Depth", 0),
		("BackTracking Limited Depth", 1),
		("BackTracking With Score Check", 0),
		("BackTracking With Score Check", 1),
		("BackTracking With Score Check", 2),
		("Advantage Matrix", 0),
	]

	dict_time = {}
	dict_perf = {}
	list_heuristics_str = []

	for heuristic_setting_index in range(len(list_heuristics_to_test)):
		print("====> Heuristic", heuristic_setting_index, "/", len(list_heuristics_to_test))
		this_heuristic_setting = list_heuristics_to_test[heuristic_setting_index]
		accuracy_total, time_taken = evaluate_heuristic_performance(this_heuristic_setting[0], this_heuristic_setting[1], set_of_levels)
		name_in_dict = this_heuristic_setting[0] + ' ( variant ' + str(this_heuristic_setting[1]) + ' )'

		dict_time[name_in_dict] = time_taken
		dict_perf[name_in_dict] = accuracy_total

		list_heuristics_str.append(name_in_dict)

	print("Time : ", dict_time)
	print("Perf : ", dict_perf)

	print('=====> Display Performance/Time of each heuristic')
	display_performance_time_heuristic(dict_time, dict_perf)

	print('=====> Display evolution of passed levels')
	plot_performance_of_each_solver(set_of_levels, list_heuristics_str)

	print('=====> Display sum of predictors passing levels for each level')
	plot_quantity_predictor_passing_each_levels(set_of_levels, list_heuristics_str)
