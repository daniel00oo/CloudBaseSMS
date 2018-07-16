from Sender import Sender
import sys

def main():

	ac = len(sys.argv)
	url = 'localhost'
	queue = 'default' 

	if ac == 1:
		print("""
	sender [message, queue, url]

		Used to send messages via RabbitMQ to consumer nodes

		message - the message you want to be sent (e.g.: "run cpu")
		queue - the queue for the message to be send to. This will
				influence where the message will be redirected. 
				(e.g.: "default")
		url	- the url that will be used to store info (e.g.: "localhost")
			""")
		return(ac)

	if ac == 4:
		url = sys.argv[3]
	if ac == 3:
		queue = sys.argv[2]
	if ac == 2:
		s = Sender(url)
		s.send(sys.argv[1], queue)

	return(ac)

if __name__ == '__main__':
	main()