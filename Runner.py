import os
import subprocess
import Converter
import json
import io

class Runner(object):

	def __init__(self, loadFile):
		"""
			Runner - class 
				Executes commands from files specified in 'files.json' as {"command": "file path"}

		"""
		self.cwd = os.getcwd()	#current working directory
		self.conv = Converter.Converter()

		#dictionary of shortcuts to actual files {"Operating system" : ["path", "to", "command"]}
		#access a command: 
		#	r = Runner(filePath)
		#	r.commands[operatingSystem][command]
		self.commands = self.conv.fromJSONtoDict(loadFile)
		
		for operatingSystem in self.commands:
			self.commands[operatingSystem] = os.sep.join(self.commands[operatingSystem])	#for portability, we use os.sep to join the path with the correct OS separator


	def run(self, operatingSystem):
		#call: 
		os.chdir(os.path.dirname(self.commands[operatingSystem]))
		d = self.conv.fromJSONtoDict(os.path.basename(self.commands[operatingSystem]))	#loading json file into memory as a dict

		try:
			os.mkdir('metrics')
		except:
			pass

		os.chdir('metrics')

		for cmd in d:
			subprocess.call(d[cmd] + ['/format:list', '>', '%s.txt' % cmd], shell=True)	
			self.conv.makeJSON('%s.txt' % cmd, '%s.json' % cmd)

		self.conv.groupJSON('metrics.json', *d.keys())

		os.chdir(self.cwd)									#changing the working directory back to the original