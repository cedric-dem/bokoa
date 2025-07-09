from level_generator.config.config import grid_sizes
from level_generator.heuristics_solver.backtrack_with_limited_depth import BackTrackingLimitedDepthSolver
from level_generator.heuristics_solver.backtrack_with_score_check import BackTrackingWithScoreCheckSolver
from level_generator.heuristics_solver.greedy import GreedySolver
from level_generator.heuristics_solver.advantage_matrix import AdvantageMatrixSolver
import time

def evaluate_heuristic_performance(name, levels_set):
	print('====> Evaluate heuristic: ', name)

	performance = []
	time_taken = []

	for grid_size_index in range(len(levels_set)):
		t0=time.time()
		reached_goal = 0
		print("==> on grid size ", grid_sizes[grid_size_index], " levels quantity : ", len(levels_set[grid_size_index]))
		for level_index in range(len(levels_set[grid_size_index])):
			reached_score = get_score_of_a_given_level_solved_using_given_heuristic(name, levels_set[grid_size_index][level_index])

			this_goal = levels_set[grid_size_index][level_index].best_score
			# print("=> level", level_index, " goal ", this_goal, "reached : ", reached_score)

			if abs(reached_score - this_goal) < 0.01:
				reached_goal += 1
		performance.append(round(reached_goal / len(levels_set[grid_size_index]), 2))
		t1=time.time()
		time_taken.append(round(t1-t0,2))

	print('==> Performance : ', performance, " time taken: ", time_taken)

def get_score_of_a_given_level_solved_using_given_heuristic(heuristic_name, level):
	match heuristic_name:
		case 'Greedy':
			solver = GreedySolver(level)
		case 'Advantage Matrix':
			solver = AdvantageMatrixSolver(level)
		case "BackTracking Limited Depth":
			solver = BackTrackingLimitedDepthSolver(level)
		case "BackTracking With Score Check":
			solver = BackTrackingWithScoreCheckSolver(level)
		case _:
			print("Not found solver")

	final_score = solver.solve()

	return final_score
