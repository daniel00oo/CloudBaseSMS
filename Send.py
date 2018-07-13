import pika

class Send(object):
	def __init__(self, url='localhost'):
		self.url = url

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.url))
		self.channel = self.connection.channel()


	def close(self):
		self.connection.close()

	def queueDec(self, que):
		self.channel.queue_declare(queue=que)

	def send(self, que, message):
		self.channel.basic_publish(
			exchange = '',
			routing_key = que,
			body = message
			)

s = Send()

s.queueDec('hello')
s.send('hello', "Hello World!")
s.close()