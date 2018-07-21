import Receiver
import Runner
import platform
import subprocess
import sys
import threading
import time
from Repeat import Repeat


class Receive(Receiver.Receiver):
	def __init__(self, url='localhost'):
		Receiver.Receiver.__init__(self, url)
		self.osys = platform.system()
		self.r = Runner.Runner('files.json')


	def howToProcess(self, body):
		bodyList = body.split(' ')

		if bodyList[0] == "start":
			self.start(int(bodyList[1]))
		if bodyList[0] == "stop":
			self.stop()
		if bodyList[0] == "update":
			self.update(body)

	def start(self, interval, *args, **kwargs):
		self.t = Repeat(interval, self.r.run, self.osys)
		self.t.start()
		
	def stop(self):
		self.t.stop()

	def update(self, body):
		pass

queue = 'default'
url = 'localhost'
if len(sys.argv) >= 3:
	url = sys.argb[2]
if len(sys.argv) >= 2:
	queue = sys.argv[1]

r = Receive(url)
r.receive(queue)