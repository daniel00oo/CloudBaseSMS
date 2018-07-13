from uuid import uuid4

class Message(object):
	def __init__(self):
		self.id = uuid4()