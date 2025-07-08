import random

from level_generator.classes.operation import Operation

random.seed(123456789)

def get_operations_reserve_balanced(grid_size):
	total_of_each_op = (grid_size[0] * grid_size[1]) // 4
	operations_reserve = (
			['+' for _ in range(total_of_each_op)] +
			['-' for _ in range(total_of_each_op)] +
			['×' for _ in range(total_of_each_op)] +
			['÷' for _ in range(total_of_each_op)])

	random.shuffle(operations_reserve)
	return operations_reserve

def set_operations_and_operand(grid_size, operations_grid):
	operations_reserve = get_operations_reserve_balanced(grid_size)
	for i in range(grid_size[0]):
		for j in range(grid_size[1]):
			if i == 0 and j == 0:
				operations_grid[0][0] = "1"
			else:
				if operations_reserve[0] == "×" or operations_reserve[0] == "÷":
					new_operation = Operation(operations_reserve[0], random.randint(2, 5))

				else:
					new_operation = Operation(operations_reserve[0], random.randint(1, 5))

				operations_grid[j][i] = new_operation
				del operations_reserve[0]

def set_operations_and_operand_balanced(grid_size, operations_grid):
	# TODO
	pass
