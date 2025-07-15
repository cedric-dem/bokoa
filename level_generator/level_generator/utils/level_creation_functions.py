import random
import math

from level_generator.classes.operation import Operation

random.seed(12345)

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

def get_operand_reserve_balanced(total_of_each_op, low, high):
	multiply_factor_addition_operations = math.ceil(total_of_each_op / (high - low))
	operands_list = [i for i in range(low, high)] * multiply_factor_addition_operations
	random.shuffle(operands_list)
	return operands_list

def set_operations_and_operand_balanced(grid_size, operations_grid):
	total_of_each_op = (grid_size[0] * grid_size[1]) // 4

	operands_plus = get_operand_reserve_balanced(total_of_each_op, 1, 6)
	operands_minus = get_operand_reserve_balanced(total_of_each_op, 1, 6)
	operands_div = get_operand_reserve_balanced(total_of_each_op, 2, 6)
	operands_mul = get_operand_reserve_balanced(total_of_each_op, 2, 6)

	reserve = get_operations_reserve_balanced(grid_size)

	for line_index in range(grid_size[0]):
		for column_index in range(grid_size[1]):
			if line_index == 0 and column_index == 0:
				new_operation = "1"
			else:
				match reserve[0]:
					case "×":
						new_operation = Operation(reserve[0], operands_mul.pop(0))

					case "÷":
						new_operation = Operation(reserve[0], operands_div.pop(0))

					case "-":
						new_operation = Operation(reserve[0], operands_plus.pop(0))

					case "+":
						new_operation = Operation(reserve[0], operands_minus.pop(0))
					case _:
						raise ValueError("Invalid  operation ", reserve[0])

				del reserve[0]

			operations_grid[column_index][line_index] = new_operation

# print("===> Left of each operands : ", len(operands_plus), len(operands_minus), len(operands_mul), len(operands_div))
