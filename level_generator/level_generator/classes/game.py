class Game(object):
	def __init__(self, level):
		self.level = level
		self.score = 1
		self.grid_size = level.grid_size

		self.moves_history = []
		self.position_history = [[0, 0]]

	def apply_move(self, direction):
		new_pos = [self.position_history[-1][0] + direction[0], self.position_history[-1][1] + direction[1]]

		self.moves_history.append(direction)

		new_operation = self.level.operations_grid[new_pos[0]][new_pos[1]]

		self.apply_operation(new_operation)

		self.position_history.append(new_pos)

	def apply_operation(self, operation):
		match operation[0]:
			case "+":
				self.score += int(operation[1])
			case '-':
				self.score -= int(operation[1])
			case '×':
				self.score *= int(operation[1])
			case '÷':
				self.score /= int(operation[1])
			case _:
				raise ValueError("Invalid Value  (in Apply Operation) : ", operation[0])

	def is_move_in_bound(self, new_pos):
		return new_pos[0] >= 0 and new_pos[1] >= 0 and new_pos[0] < self.grid_size[1] and new_pos[1] < self.grid_size[0]

	def is_move_in_history(self, new_pos):
		return new_pos in self.position_history
