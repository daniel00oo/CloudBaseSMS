import pika

class Receiver(object):
	def __init__(self, url='localhost', howToProcess=lambda x: x):
		self.url = url

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.url))
		self.channel = self.connection.channel()
		self.howToProcess = howToProcess


	def queueDec(self, que):
		self.channel.queue_declare(queue=que, durable=True)

	def callback(self, ch, method, properties, body):
		print("-----------------------")
		print(" [x] Received %r" % body)
		self.howToProcess(body)
		print(" [x] Done")

		ch.basic_ack(delivery_tag = method.delivery_tag)


	def setReceive(self, que):
		self.channel.basic_consume(
			self.callback,
			queue = que
			)

	def receive(self, que='default'):
		self.queueDec(que)
		self.setReceive(que)
		self.channel.start_consuming()