~ Supercalifragilisticexpialidocius Monitoring System (SMS) Project ~

pip install SuperMS

How to use:
	As a consumer node: 
		receive2.py [queue, url, db, port]
			queue - the queue in which to listen for messages
			url - the url in which the queue can be found
			db - the mongodb database in which to store the metrics
			port - database port (recommended to be left to default)
		
	As a publisher node: 
		send.py [file, queue, url]
			file - the file to get the metrics
				THIS FILE MUST HAVE THE FOLLOWING:
					- one class with the same name as the file
					- a method within the class named "get" which returns a python dictionary
			queue - the queue in which to send the file
			url - the url in which the queue can be found
		If no arguments are passed to the send.py command, help text will be displayed.
	
	
