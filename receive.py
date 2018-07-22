import platform
import sys
import threading
import os
import time

import Receiver
import Runner
import Repeat
import StorageMongoDB
import Converter


class Receive(Receiver.Receiver):
	def __init__(self, url='localhost', dbname='default'):
		Receiver.Receiver.__init__(self, url)
		self.osys = platform.system()
		self.runner = Runner.Runner('files.json')
		self.storage = StorageMongoDB.StorageMongoDB(dbname)
		self.conv = Converter.Converter()
		self.t = Repeat.Repeat(100, self.run)


	def howToProcess(self, body):
		bodyList = body.split(' ')

		if bodyList[0] == "start":
			self.start(int(bodyList[1]))
		if bodyList[0] == "stop":
			self.stop()
		if bodyList[0] == "update":
			self.update(body)
	def run(self):
		print("__________________________")
		print("    - Running commands...")
		self.runner.run(self.osys)
		print("    - Commands executed successfully")
		d = {}
		print("    - Getting metrics...")
		d = self.conv.fromJSONtoDict(os.path.join(
			'tools', 
			self.osys, 
			'metrics', 
			'metrics.json'
			))
		d['time'] = time.strftime("%c")
		d['day'] = time.strftime("%d")
		d['month'] = time.strftime("%m")
		d['year'] = time.strftime("%Y")
		print("    - Storing metrics...")
		self.storage.addDict(d)
		print("   (~) Task completed successfully!")

	def start(self, interval, *args, **kwargs):
		self.t = Repeat.Repeat(interval, self.run)
		self.t.start()
		
	def stop(self):
		print("    - Closing...")
		self.t.stop()
		print("   (~) Task completed successfully!")

	def update(self, body):
		pass







h = """

	receive [queue, url, database]

		Used to receive messages via RabbitMQ from publishers

		queue - the queue for the message to be received from. This will
				influence what messages are processed by a node. 
				(default: "default")
		url	- the url from which to get info via RabbitMQ (default: "localhost")
		database - the url of the database in which to store the metrics
					(default: "localhost")

	Examples:
		python receive.py 
		python receive.py "help"
		python receive.py "queue1"
		python receive.py "queue1" "url1"
		python receive.py "queue1" "url1" "database1"

"""

if len(sys.argv) == 2 and sys.argv[1].lower() == 'help':
	print(h)
else:


	queue = 'default'
	url = 'localhost'
	database = 'localhost'
	if len(sys.argv) >= 4:
		database = sys.argv[3]
	if len(sys.argv) >= 3:
		url = sys.argb[2]
	if len(sys.argv) >= 2:
		if sys.argv[1] == "help":
			print(h)
		else:
			queue = sys.argv[1]

	r = Receive(url, database)
	r.receive(queue)