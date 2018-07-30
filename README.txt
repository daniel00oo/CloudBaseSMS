~ Supercalifragilisticexpialidocius Monitoring System (SMS) Project ~

How to install:
	--Windows--

	1. Install RabbitMQ from https://www.rabbitmq.com/install-windows.html
	2. Install MongoDB Community Server from https://www.mongodb.com/download-center
	3. Go to mongo installed folder, open a command line and type "mongod --install"
	2. Run startServices.bat from \tools\Windows\ as Administrator

	--Linux--

	1. Run installDependencies.sh from ./tools/Linux/
	2. Run startServicies.sh from ./tools/Linux

How to run:

	v To receive messages:
		'startListen.bat' help
		'startListen.sh' help 

	^ To send messages:
		send.py help
		python send.py help
