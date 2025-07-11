import random
import math

from level_generator.classes.case.initial_case import InitialCase
from level_generator.classes.case.operation import Operation

random.seed(12345)

def get_operators_reserve_balanced(grid_size):
	quantity_of_each_operator = (grid_size[0] * grid_size[1]) // 4
	operators_reserve = (
			['+' for _ in range(quantity_of_each_operator)] +
			['-' for _ in range(quantity_of_each_operator)] +
			['×' for _ in range(quantity_of_each_operator)] +
			['÷' for _ in range(quantity_of_each_operator)])

	random.shuffle(operators_reserve)
	return operators_reserve

def initialize_operations_grid_unbalanced_operands(grid_size, operations_grid):
	operators_reserve = get_operators_reserve_balanced(grid_size)
	for line_index in range(grid_size[0]):
		for column_index in range(grid_size[1]):
			if line_index == 0 and column_index == 0:
				operations_grid[0][0] = InitialCase()
			else:
				operations_grid[column_index][line_index] = get_operation_with_random_operand(operators_reserve[0])
				del operators_reserve[0]

def get_operation_with_random_operand(new_operator):
	if new_operator == "×" or new_operator == "÷":
		new_operand = random.randint(2, 5)
	else:
		new_operand = random.randint(1, 5)
	return Operation(new_operator, new_operand)

def get_operand_reserve_balanced(quantity_of_each_operator, min_value, max_value):
	multiply_factor_addition_operations = math.ceil(quantity_of_each_operator / (max_value - min_value))
	operands_list = [i for i in range(min_value, max_value)] * multiply_factor_addition_operations
	random.shuffle(operands_list)
	return operands_list

def initialize_operations_grid_balanced_operands(grid_size, operations_grid):
	quantity_of_each_operator = (grid_size[0] * grid_size[1]) // 4

	operands_plus = get_operand_reserve_balanced(quantity_of_each_operator, 1, 6)
	operands_minus = get_operand_reserve_balanced(quantity_of_each_operator, 1, 6)
	operands_div = get_operand_reserve_balanced(quantity_of_each_operator, 2, 6)
	operands_mul = get_operand_reserve_balanced(quantity_of_each_operator, 2, 6)

	operators_reserve = get_operators_reserve_balanced(grid_size)

	for line_index in range(grid_size[0]):
		for column_index in range(grid_size[1]):
			if line_index == 0 and column_index == 0:
				new_case = InitialCase()
			else:
				new_case = get_operation_with_operand_balanced(operators_reserve[0], operands_mul, operands_div, operands_plus, operands_minus)

				del operators_reserve[0]

			operations_grid[column_index][line_index] = new_case

	# print("===> Left of each operands : ", len(operands_plus), len(operands_minus), len(operands_mul), len(operands_div))

def get_operation_with_operand_balanced(new_operator, operands_mul, operands_div, operands_plus, operands_minus):
	match new_operator:
		case "×":
			new_operand = operands_mul.pop(0)
		case "÷":
			new_operand = operands_div.pop(0)
		case "-":
			new_operand = operands_plus.pop(0)
		case "+":
			new_operand = operands_minus.pop(0)
		case _:
			raise ValueError("Invalid  operation ", new_operator)

	return Operation(new_operator, new_operand)
