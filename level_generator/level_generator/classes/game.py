class Game(object):
	def __init__(self, level):
		self.level = level
		self.score = 1
		self.grid_size = level.grid_size
		self.grid_size_id = level.grid_size_id

		self.moves_history = []

		self.current_position_head = [0, 0]

		self.occupation_matrix = [[False for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
		self.occupation_matrix[0][0] = True

	def apply_move_given_direction(self, direction):
		new_pos = [self.current_position_head[0] + direction[0], self.current_position_head[1] + direction[1]]

		self.apply_move_given_direction_and_new_pos(direction, new_pos)

	def apply_move_given_direction_and_new_pos(self, direction, new_pos):
		# For optimization purposes, back_track can call directly this function given new pos, saves like 5% of time not to recompute new_pos

		self.moves_history.append(direction)

		new_operation = self.level.operations_grid[new_pos[0]][new_pos[1]]

		self.apply_operation(new_operation)

		self.occupation_matrix[new_pos[0]][new_pos[1]] = True
		self.current_position_head = new_pos

	def apply_operation(self, operation):
		match operation.operation:
			case "+":
				self.score += operation.operand
			case '-':
				self.score -= operation.operand
			case '×':
				self.score *= operation.operand
			case '÷':
				self.score /= operation.operand
			case _:
				raise ValueError("Invalid Value  (in Apply Operation) : ", operation[0])

	def is_move_in_bound_and_not_in_history(self, new_pos):
		return 0 <= new_pos[0] < self.grid_size[1] and 0 <= new_pos[1] < self.grid_size[0] and (not self.occupation_matrix[new_pos[0]][new_pos[1]])
