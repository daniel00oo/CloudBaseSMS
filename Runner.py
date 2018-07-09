import os
import subprocess
import Converter
import json

class Runner(object):

	def __init__(self, loadFile):
		"""
			Runner - class 
				Executes files from commands specified in 'files.json' as {"command": "file path"}

		"""
		self.cwd = os.getcwd()
		self.conv = Converter.Converter()

		#dictionary of shortcuts to actual files {"Operating system" : ["path", "to", "command"]}
		#access a command: 
		#	r = Runner(filePath)
		#	r.commands[operatingSystem][command]
		self.commands = self.conv.fromJSONtoDict(loadFile)
		
		for operatingSystem in self.commands:
			self.commands[operatingSystem] = os.sep.join(self.commands[operatingSystem])	#for portability, we use os.sep to join the path with the correct OS separator


	def run(self, operatingSystem):
		os.chdir(self.commands[operatingSystem])
		d = self.conv.fromJSONtoDict(os.path.basename(self.commands[operatingSystem]))

		for cmd in d:
			subprocess.call(d[cmd].split(' '))


		for line in l:
			subprocess.call(line.split(' '), shell=True)	#executting the batch file line by line

		os.chdir(self.cwd)									#changing the working directory back to the original
