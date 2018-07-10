import json
import io
import os
import ast

class Converter(object):
	def __init__(self):
		pass

	def fromTextToDict(self, text, key_value__delimiter = '=', entry_demiliter = '\n'):
		#call: fromTextToDict(text[, key_value__delimiter, entry_demiliter])
		#input: text - string with the format key=value \n key2=value2
		#output: d - dictionary containing all the keys and values from 'text'

		text = text.strip()
		d = {}

		for line in text.split('\n'):
			tmp = line.split('=')
			if tmp != ['']:
				d[tmp[0]] = tmp[1]

		return d

	def fromDictToJson(self, d):
		#call: fromTextToJson(d)
		#input: d - dictionary with info to be converted
		#output: s - string contaning info for a json file

		s = json.dumps(d, sort_keys = True, indent = 4, separators = (',', ': '))
		return s

	def printToFile(self, what, where):
		#call: printToFile(what, where)
		#input: what - string to be printed
		#		where - name of the file where 'what' should be printed in
		#output: -

		f = open('%s' % (where), 'w')
		f.write(what)
		f.close()

	def makeJSON(self, inFile, outFile):
		#call: makeJSON(inFile, outFile)
		#input: inFile - string name of the input file
		#		outFile - string name of the output file
		#output: -
		f = io.open(inFile, 'r', encoding='utf16')	#output of batch commands to a file is encoded with utf16
		s = f.read()
		d = self.fromTextToDict(s)
		j = self.fromDictToJson(d)

		self.printToFile(j, outFile)

		f.close()

	def fromJSONtoDict(self, filePath):
		#call: fromJSONtoKeys(filePath)
		#input: filePath - string; path of the .json file
		#output: d - dictionary of items
		f = open(filePath)

		return ast.literal_eval(json.dumps(json.loads(open(filePath).read())))

	def groupJSON(self, outFile, inFiles):
		#call: groupJSON(outFile, file1, file2, file3, ...)
		#input: outFile - string; name of the file where all the JSONs will be grouped into
		#		*inFiles - list of names of source files from which the text will be grouped into a single file
		#output: -
		s = ""
		for file in inFiles:
			if file[:-5] == ".json":
				s += '\n\t"' + file[:-5] + '":\n'
				with open(file, 'r') as f:
					for line in f:
						s += '\t' + line
			else:
				s += '\n\t"' + file + '":\n'
				with open(file + ".json", 'r') as f:
					for line in f:
						s += '\t' + line

		s = "{" + s + "\n}"

		#s = json.dumps(s, sort_keys = True, indent = 4, separators = (',', ': '))

		open(outFile, 'w').write(s)
