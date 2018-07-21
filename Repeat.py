import threading
import time

class Repeat(object):
	"""
	Class used to repead a task after a set interval

	"""
	def __init__(self, interval, function, *args, **kwargs):
		self.is_running = False
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs

		self.thread = threading.Thread(target = self.run)
		self.thread.daemon = True


	def run(self):
		while self.is_running:
			
			self.function(*self.args, **self.kwargs)
			
			time.sleep(self.interval)

	def start(self):
		if self.is_running == False:
			self.is_running = True
			self.thread.start()	#starting the thread

	def stop(self):
		self.is_running = False