import random

def get_operations_reserve(grid_size):
	total_of_each_op = (grid_size[0] * grid_size[1]) // 4
	operations_reserve = (
			['+' for _ in range(total_of_each_op)] +
			['-' for _ in range(total_of_each_op)] +
			['×' for _ in range(total_of_each_op)] +
			['÷' for _ in range(total_of_each_op)])

	random.shuffle(operations_reserve)
	return operations_reserve
