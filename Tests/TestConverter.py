import sys
sys.path.insert(0, "../")

import Converter

class TestConverter(object):
	def __init__(self):
		self.c = Converter.Converter()
		self.testfromDictToJson()
		self.testfromTextToDict()
		self.testmakeJSON()

	def testfromDictToJson(self):
		d = {'something1' : 'something2', 'else': 35}

		try:
			self.c.fromDictToJson(d)
		except:
			print("Error: 'fromDictToJson' is not working properly!")

	def testfromTextToDict(self):
		text = 	"""

			key1=value1
			key2=value2
			key3=value3

				"""
		try:
			self.c.fromTextToDict(text)
		except:
			print("Error: fromTextToDict is not working properly!")

		
	def testmakeJSON(self):
		inFile = "cpuinfo.txt"
		outFile = "cpuinfo.json"

		try:
			self.c.makeJSON(inFile, outFile)
		except:
			print("Error: makeJSON is not working properly!")

t = TestConverter()