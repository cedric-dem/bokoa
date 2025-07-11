class Operation(object):
	def __init__(self, operator, operand):
		self.operator = operator
		self.operand = operand

	def __str__(self):
		return self.operator + str(self.operand)
