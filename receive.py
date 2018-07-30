import platform
import sys
import os
import time

import Receiver
import Runner
import Repeat
import StorageMongoDB
import Converter


class Receive(Receiver.Receiver):

        # Extention of Receive class made custom to
        #   automatically start a process
        #   to collect and store metrics of host unit

        # r = Receive([url, dbhost])
        #     url - url string, the url in from which to
        #           receive messages via RabbitMQ
        #           (defaults to 'localhost')
        #     dbhost - url string, the url in which to store the metrics
        #         (defaults to 'localhost')

        # Variables:
        #     osys - string, name of the host operating system
        #         (e.g.: 'Windows')
        #     runner - instance of Runner class,
        #              used to run files to get metrics
        #     storage - instance of StorageMongoDB class,
        #               used to store the metrics into a noSQL database
        #               (using pymongo package and MongoDB)
        #     conv - instance of Converter class, used to convert
        #            json files into python dictionaries
        #     t - instance of Repeater class,
        #         used to repeat the '__run' task at given intervals
        #     is_running - boolean value,
        #                  describes if the process is running or not
        #                  (changes with 'start' and 'stop' methods)

        # Methods:
        #     howToProcess(body)
        #       method used to process the received message
        #     __run()
        #       used to run the files and commands that will get and
        #       store the desired metrics into a database
        #     start()
        #       used to start the process, calls the '__run' method.
        #     stop()
        #       used to stop the process called by the 'start' method.

    def __init__(self, url='localhost', dbhost='default'):
        Receiver.Receiver.__init__(self, url)
        self.osys = platform.system()
        self.runner = Runner.Runner('files.json')
        self.storage = StorageMongoDB.StorageMongoDB(dbhost)
        self.conv = Converter.Converter()
        self.is_running = False

    def howToProcess(self, body):
        # call: - (don't call this outside pls)
        # input: body - string, the message received
        # output -
        bodyList = body.split(' ')

        if bodyList[0] == "start":
            self.start(int(bodyList[1]))
        if bodyList[0] == "stop":
            self.stop()
        if bodyList[0] == "update":
            self.update(body)

    def __run(self):
        # call: - (NEVER call this outside pls)
        # input: -
        # output: -
        print("__________________________")
        print("    - Running commands...")
        self.runner.run(self.osys)
        print("    - Commands executed successfully")
        d = {}
        print("    - Getting metrics...")
        d = self.conv.fromJSONtoDict(os.path.join(
            'tools',
            self.osys,
            'metrics',
            'metrics.json'))
        # time tags for easier access and management
        d['time'] = time.strftime("%c")
        d['day'] = time.strftime("%d")
        d['month'] = time.strftime("%m")
        d['year'] = time.strftime("%Y")
        print("    - Storing metrics...")
        self.storage.addDict(d)
        print("   (~) Task completed successfully!")

    def start(self, interval):
        # call: start(interval)
        # input: interval - number, the time between function calls
        # output: -
        if not self.is_running:
            self.is_running = True
            self.t = Repeat.Repeat(interval, self.__run)
            self.t.start()
        else:
            print("    x Already running!")
            print("    x Send 'stop' if you want to stop the process")
            print("    x or <ctr> + <c> to terminate the program!")

    def stop(self):
        # call: stop()
        # input: -
        # output: -
        if not self.is_running:
            self.is_running = False
            print("    - Stopping...")
            self.t.stop()
            print("   (~) Task completed successfully!")
        else:
            print("    x Nothing to stop...")

    def update(self, body):
        pass


# help message
h = """

    receive [queue, url, database]

        Used to receive messages via RabbitMQ from publisher nodes

        queue - the queue for the message to be received from. This will
                influence what messages are processed by a node.
                (default: "default")
        url - the url from which to get info via RabbitMQ
              (default: "localhost")
        database - the url of the database in which to store the metrics
                    (default: "localhost")

    Examples:
        python receive.py
        python receive.py help
        python receive.py "queue1"
        python receive.py "queue1" "url1"
        python receive.py "queue1" "url1" "database1"

"""

if len(sys.argv) == 2 and sys.argv[1].lower() == 'help':
    # print the help message if requested
    print(h)
else:
    # run as usual otherwise
    queue = 'default'
    url = 'localhost'
    database = 'localhost'
    if len(sys.argv) >= 4:
        # the 3rd argument becomes the database url
        database = sys.argv[3]
    if len(sys.argv) >= 3:
        # the 2nd argument becomes the RabbitMQ url
        # (from which messages will be extracted)
        url = sys.argb[2]
    if len(sys.argv) >= 2:
        # the 1st argument becomes the queue name
        # from which to extract messages via RabbitMQ
        queue = sys.argv[1]

    # start listening
    r = Receive(url, database)
    r.receive(queue)
