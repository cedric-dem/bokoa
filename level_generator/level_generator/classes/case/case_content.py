from abc import ABC, abstractmethod

class CaseContent(object):
	def __init__(self):
		pass

	@abstractmethod
	def is_initial(self):
		pass

