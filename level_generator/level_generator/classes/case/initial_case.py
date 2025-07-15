from level_generator.classes.case.case_content import CaseContent

class InitialCase(CaseContent):
	def __init__(self):
		super().__init__()

	def __str__(self):
		return "1"

	def is_initial(self):
		return True
