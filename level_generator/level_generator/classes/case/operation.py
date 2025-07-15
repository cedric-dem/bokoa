from level_generator.classes.case.case_content import CaseContent

class Operation(CaseContent):
	def __init__(self, operation, operand):
		super().__init__()
		self.operation = operation
		self.operand = operand

	def __str__(self):
		return self.operation + str(self.operand)

	def is_initial(self):
		return False
