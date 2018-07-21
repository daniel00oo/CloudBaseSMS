import pika

class Sender(object):
	def __init__(self, url='localhost'):
		self.url = url

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.url))
		self.channel = self.connection.channel()



	def close(self):
		self.connection.close()

	def queueDec(self, que):
		self.channel.queue_declare(queue=que, durable=True)

	def send(self, message, que='default1'):
		print("==> Sending mesage %r in queue %r" % (message, que))
		self.queueDec(que)
		self.channel.basic_publish(
			exchange = '',
			routing_key = que,
			body = message,
			properties = pika.BasicProperties(
				delivery_mode = 2
				)
			)

