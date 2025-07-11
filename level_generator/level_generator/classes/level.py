from level_generator.classes.operation import Operation
from level_generator.config.config import *
from level_generator.utils.level_creation_functions import set_operations_and_operand_balanced, set_operations_and_operand

class Level(object):
	def __init__(self, grid_size_id, operations_grid):
		self.grid_size_id = grid_size_id
		self.grid_size = grid_sizes[grid_size_id]

		if operations_grid:
			self.operations_grid = [[None for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
			for i in range(self.grid_size[1]):
				for j in range(self.grid_size[0]):
					if i == 0 and j == 0:
						self.operations_grid[i][j] = "1"
					else:
						self.operations_grid[i][j] = Operation(operations_grid[i][j][0], int(operations_grid[i][j][1]))
		else:
			self.operations_grid = [[None for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
			self.create_level()

	def create_level(self):
		if balance_operand:
			set_operations_and_operand_balanced(self.grid_size, self.operations_grid)
		else:
			set_operations_and_operand(self.grid_size, self.operations_grid)

	def display_level(self):
		for line in self.operations_grid:
			print(line)
