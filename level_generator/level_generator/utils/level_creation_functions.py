import random
import math

from level_generator.classes.case.initial_case import InitialCase
from level_generator.classes.case.operation import Operation

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
				operations_grid[0][0] = InitialCase()
			else:
				operations_grid[j][i] = get_operation_with_random_operand(operations_reserve[0])
				del operations_reserve[0]

def get_operation_with_random_operand(new_operation):
	if new_operation == "×" or new_operation == "÷":
		new_operation = Operation(new_operation, random.randint(2, 5))
	else:
		new_operation = Operation(new_operation, random.randint(1, 5))
	return new_operation

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
				new_operation = InitialCase()
			else:
				new_operation = get_operation_with_operand_balanced(reserve[0], operands_mul, operands_div, operands_plus, operands_minus)

				del reserve[0]

			operations_grid[column_index][line_index] = new_operation

	# print("===> Left of each operands : ", len(operands_plus), len(operands_minus), len(operands_mul), len(operands_div))

def get_operation_with_operand_balanced(new_op, operands_mul, operands_div, operands_plus, operands_minus):
	match new_op:
		case "×":
			new_operation = Operation(new_op, operands_mul.pop(0))
		case "÷":
			new_operation = Operation(new_op, operands_div.pop(0))
		case "-":
			new_operation = Operation(new_op, operands_plus.pop(0))
		case "+":
			new_operation = Operation(new_op, operands_minus.pop(0))
		case _:
			raise ValueError("Invalid  operation ", new_op)

	return new_operation
