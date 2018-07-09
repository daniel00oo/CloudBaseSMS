import Converter
import json

class UI(object):
	def __init__(self):

		self.commands['cpu'] = """
		cpu - Displays information about CPU

			Attributes: %s
		""".format()

	@staticmethod
	def showHelp():

		h = """
		
	PLACEHOLDER

		"""

		print(h)

	def getCommandAttributes(self, command):
		pass
