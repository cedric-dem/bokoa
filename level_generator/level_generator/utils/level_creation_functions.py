import random
import math

from level_generator.classes.operation import Operation

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
	total_of_each_op = (grid_size[0] * grid_size[1]) // 4

	multiply_factor_addition_operations = math.ceil(total_of_each_op / 5)
	operands_plus = [i for i in range(1, 6)] * multiply_factor_addition_operations
	operands_minus = [i for i in range(1, 6)] * multiply_factor_addition_operations
	random.shuffle(operands_plus)
	random.shuffle(operands_minus)

	multiply_factor_multiplication_operations = math.ceil(total_of_each_op / 4)
	operands_mul = [i for i in range(2, 6)] * multiply_factor_multiplication_operations
	operands_div = [i for i in range(2, 6)] * multiply_factor_multiplication_operations
	random.shuffle(operands_div)
	random.shuffle(operands_mul)

	reserve = get_operations_reserve_balanced(grid_size)

	# print("===> Balanced number of each operands : ", len(operands_plus), len(operands_minus), len(operands_mul), len(operands_div), "(needed : ", total_of_each_op, ") ( factors  ", multiply_factor_addition_operations, multiply_factor_addition_operations, ")")
	# print("Operands : ", operands_plus, operands_minus, operands_mul, operands_div)

	for i in range(grid_size[0]):
		for j in range(grid_size[1]):
			if i == 0 and j == 0:
				operations_grid[0][0] = "1"
			else:
				if reserve[0] == "×":
					new_operation = Operation(reserve[0], operands_mul[0])
					del operands_mul[0]

				elif reserve[0] == "÷":
					new_operation = Operation(reserve[0], operands_div[0])
					del operands_div[0]

				elif reserve[0] == "-":
					new_operation = Operation(reserve[0], operands_plus[0])
					del operands_plus[0]

				elif reserve[0] == "+":
					new_operation = Operation(reserve[0], operands_minus[0])
					del operands_minus[0]

				operations_grid[j][i] = new_operation
				del reserve[0]

	# print("===> Left of each operands : ", len(operands_plus), len(operands_minus), len(operands_mul), len(operands_div))
