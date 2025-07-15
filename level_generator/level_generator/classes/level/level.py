from level_generator.config.config import *
from level_generator.utils.level_creation_functions import set_operators_and_operand_balanced, set_operations_and_operand
import copy

class Level(object):
	def __init__(self, grid_size_id, operations_grid):
		self.grid_size_id = grid_size_id
		self.grid_size = grid_sizes[grid_size_id]

		if operations_grid:
			self.operations_grid = copy.deepcopy(operations_grid)

		else:
			self.operations_grid = [[None for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
			if balance_operands:
				set_operators_and_operand_balanced(self.grid_size, self.operations_grid)
			else:
				set_operations_and_operand(self.grid_size, self.operations_grid)

	def display_level(self):
		for line_index in range(len(self.operations_grid)):
			for cell_index in range(len(self.operations_grid[line_index])):
				cell = self.operations_grid[line_index][cell_index]
				print(cell, end = " ")
			print()
