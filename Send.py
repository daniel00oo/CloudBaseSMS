from Sender import Sender
import sys

def main():

	ac = len(sys.argv)
	url = 'localhost'
	queue = 'default' 

	if ac == 1:
		print("""
	send [message, queue, url]

		Used to send messages via RabbitMQ to consumer nodes

		message - the message you want to be sent (default: None)
		queue - the queue for the message to be send to. This will
				influence where the message will be redirected. 
				(default: "default")
		url	- the url that will be used to store info (default: "localhost")

	Examples:
		python send.py "start 10"
		python send.py "stop"
		python send.py "start 100" "default" "localhost"
			""")
		return(ac)

	if ac >= 4:
		url = sys.argv[3]
	if ac >= 3:
		queue = sys.argv[2]
	if ac >= 2:
		s = Sender(url)
		s.send(sys.argv[1], queue)

	return(ac)

if __name__ == '__main__':
	main()