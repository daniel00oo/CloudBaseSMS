import pika
import time


class Receiver(object):

        # Receiver - class

        # Used to listen for messages and process them via RabbitMQ

        # Variables:
        #   url - string, used to store the url from which to
        #         listen to for messages
        #   connection - pika.BlockingConnection instance,
        #                used to connect to 'url'
        #   channel - pika.BlockingConnection.channel variable,
        #             used to listen to given queues

        # Methods:
        #   queueDec(que)
        #       Declares a queue 'que' to exist. If it already exists,
        #       doesn't do anything
        #   howToProcess(body)
        #       Does nothing. Needs implemetation in a subclass
        #       This dictates how the message received will be processed
        #   callback(ch, method, properties, body)
        #       Method required by pika. Dictates how the
        #       message received will be processed
        #   setReceive(que)
        #       Sets which queue to be listened when expecting messages
        #   receive(que)
        #       Starts listening for messages of queue of name 'que'

    def __init__(self, url='localhost'):
        self.url = url

        self.connection = pika.BlockingConnection(
                            pika.ConnectionParameters(self.url))
        self.channel = self.connection.channel()

    def queueDec(self, que):
        # call: queueDec(que)
        # input: que - string, the name of the queue
        # output: -
        self.channel.queue_declare(queue=que, durable=True)

    def howToProcess(self, body):
        # overrite this function to process the body/message
        pass

    def callback(self, ch, method, properties, body):
        # method required by pika.BlockingConnection.channel.basic_consume()
        print("-----------------------")
        print(" [x] Received %r at %r" % (body, time.strftime("%c")))
        self.howToProcess(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def setReceive(self, que):
        # call: setReceive(que)
        # input: que - string, the name of the queue
        # output: -
        self.channel.basic_consume(
            self.callback,
            queue=que
            )

    def receive(self, que='default'):
        # call: receive([que])
        # input: que - string, the name of the queue
        # output: -
        self.queueDec(que)
        self.setReceive(que)
        self.channel.start_consuming()

    def cancel(self, que='default'):
        self.channel.basic_cancel(consumer_tag=que)
