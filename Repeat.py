import threading
import time

class Repeat(object):
	"""
		Repeat - class
		
		Class used to repeat a task after a set interval util manually stopped

		Variables:
			is_running - boolean, True if the task is running or False otherwise
			interval - number, at what intervat of time to run the function
			function - function to be run at given interval
			args - list of arguments for function call
			kwargs - key arguments for function call
			thread - instance of a python Thread. 
				Used to run the task silently in the background

		Methods:
			run()
				Used to run the function with its needed parameters
			start()
				Used to start the whole process. Calls the run method
			stop()
				Used to stop the process

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
		#call: run()
		#input: -
		#output: -
		while self.is_running:
			
			self.function(*self.args, **self.kwargs)
			
			time.sleep(self.interval)

	def start(self):
		#call: start()
		#input: -
		#output: -
		if self.is_running == False:
			self.is_running = True
			self.thread.start()	#starting the thread

	def stop(self):
		#call: stop()
		#input: -
		#output: -
		self.is_running = False