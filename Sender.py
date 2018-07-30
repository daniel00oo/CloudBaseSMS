import pika


class Sender(object):
        # Sender - class

        # Used to send messages via RabbitMQ and pika

        # Variables:
        # 	url - string, url to where to send the messages
        # 	connection - pika.BlockingConnection instance,
        #                used to connect to 'url'
        # 	channel - pika.BlockingConnection.channel variable,
        #             used to send messages to given queues

        # Methods:
        # 	close()
        # 		Used to close the connection
        # 	queueDec(que)
        # 		Declares a queue 'que' to exist.
        #       If it already exists, doesn't do anything
        # 	send(message, que)
        # 		Sends a message on a queue 'que' via RabbitMQ

    def __init__(self, url='localhost'):
        self.url = url

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.url))
        self.channel = self.connection.channel()

    def close(self):
        # call: close()
        # input:-
        # output: -
        self.connection.close()

    def queueDec(self, que):
        # call:queueDec(que)
        # input: que - string, name of the queue to be declared
        # output: -
        self.channel.queue_declare(queue=que, durable=True)

    def send(self, message, que='default1'):
        # call: send(message, que)
        # input: message - string, the message that will be sent
        # 		que - string, the name of the queue in which to put the message
        # output: -
        print("==> Sending mesage %r in queue %r" % (message, que))
        self.queueDec(que)
        self.channel.basic_publish(
            exchange='',
            routing_key=que,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2
                )
            )
