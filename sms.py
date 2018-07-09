#!/usr/bin/env python2.7

#imports
import os
import sys
import platform
import Runner
from UI import UI
import time

#global variables
osys = platform.system() #type of system (ex.: Windows, Linux)
r = Runner.Runner('files.json')

if (len(sys.argv) == 1):
	if not os.path.exists('metrics.json'):
		open('metrics.json', 'w').write('{\n\n}')

elif (len(sys.argv) == 2):
	if (sys.argv[1] in ['help', '\\h', '/h', '!h', '$h', '/help', '\\help', '$help', '!help']):
		UI.showHelp()
