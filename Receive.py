import pika

class Receive(object):
	def __init__(self, url='localhost'):
		self.url = url

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.url))
		self.channel = self.connection.channel()


	def queueDec(self, que):
		self.channel.queue_declare(queue=que)

	def callback(self, ch, method, properties, body):
		print(" [x] Received %r" % body)

	def receive(self, que):
		self.channel.basic_consume(
			callback,
			queue = que,
			no_ack = True
			)

	def start(self):
		self.channel.start_consuming()

r = Receive()
r.queueDec('hello')
r.start()