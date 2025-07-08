import random

from level_generator.classes.operation import Operation
from level_generator.config.config import *
from level_generator.utils.level_creation_functions import get_operations_reserve

class Level(object):
	def __init__(self, grid_size_id, operations_grid):
		self.grid_size_id = grid_size_id
		self.grid_size = grid_sizes[grid_size_id]

		if operations_grid:
			self.operations_grid = operations_grid
		else:
			self.operations_grid = [[None for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
			self.create_level()

	def create_level(self):

		operations_reserve = get_operations_reserve(self.grid_size)

		for i in range(self.grid_size[0]):
			for j in range(self.grid_size[1]):
				if i == 0 and j == 0:
					self.operations_grid[0][0] = "1"
				else:
					if operations_reserve[0] == "×" or operations_reserve[0] == "÷":
						new_operation = Operation(operations_reserve[0], random.randint(2, 5))

					else:
						new_operation = Operation(operations_reserve[0], random.randint(1, 5))

					self.operations_grid[j][i] = new_operation
					del operations_reserve[0]

	def display_level(self):
		for line in self.operations_grid:
			print(line)
