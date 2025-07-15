class Operation(object):
	def __init__(self, operation, operand):
		super().__init__()
		self.operation = operation
		self.operand = operand

	def __str__(self):
		return self.operation + str(self.operand)
