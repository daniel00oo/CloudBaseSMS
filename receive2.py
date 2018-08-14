#!/usr/bin/env python
import sys
import os
import time
import json
import Receiver
import tools.getmetrics
from Repeat import Repeat
from StorageMongoDB import StorageMongoDB
try:
    # for Python3.5+
    from importlib import reload
except ImportError:
    pass


class Receive(Receiver.Receiver):
    # Extention of class Receiver
    # Used to receive files via RabbitMQ

    # Variables:
    #   _storage - MongoDB client
    #   _repeater - Class used to run a function every interval

    # Methods:
    #   howToProcess(body)
    #       implementation of how to process the received file

    #       body - string, should be 'NameOfFile?\nFileContents'
    #   getmetrics()
    #       manages the files needed to get the metrics: getmetrics.py
    #       and imports.py, and stores the metrics in a database
    def __init__(self, url='localhost', db='localhost', port=27017):
        # init the Receiver
        Receiver.Receiver.__init__(self, url)
        # init the storage unit
        self._storage = StorageMongoDB(db, port)
        # init the repeater
        self._repeater = Repeat(-1, self.getmetrics)
        try:
            # a 'timer' file should always be present
            with open('./tools/timer', 'r') as f:
                # the file should contain a number and a number only
                # which will represent the intervat between getmetrics call
                i = float(f.read())
            self._repeater = Repeat(i, self.getmetrics)
            self._repeater.start()
        except IOError:
            print('    Could not find "timer" file!')

        if not os.path.exists('tools'):
            # if the whole tool directory is missing
            # the necessary files will be made
            os.mkdir('tools')
            with open('./tools/__init__.py', 'w') as f:
                pass
            with open('./tools/imports.py', 'w') as f:
                pass
            with open('./tools/getmetrics.py', 'w') as f:
                f.write('from imports import *\n\n\n')
                f.write('_d = {}\n')
                f.write('def update():\n')
                f.write('    _d.update({})\n')
            with open('./tools/timer', 'w') as f:
                f.write('-1')

    def howToProcess(self, body):
        # call: -
        # input: body - string
        # output: -
        filename, contents = body.split('?\n')
        print("-----------------------")
        print(" [x] Received %r at %r" % (filename, time.strftime("%c")))

        if filename == 'timer':
            # if a timer file was sent, the interval is set accordingly
            with open('./tools/timer', 'w') as f:
                f.write(contents)
            if float(contents) == -1:
                # -1 to stop
                self._repeater.stop()
            elif float(contents) > 0:
                # any positive number to start
                self._repeater.stop()
                self._repeater = Repeat(float(contents), self.getmetrics)
                self._repeater.start()
        else:
            with open(os.path.join('tools', filename), 'w') as f:
                f.write(contents)

            imp = ''
            with open('./tools/imports.py', 'r') as f:
                imp = f.read()
            s = filename.split('.')[0]
            if s not in imp:
                with open('./tools/imports.py', 'a') as f:
                    f.write('import ' + s + '\n')
                with open('./tools/getmetrics.py', 'a') as f:
                    f.write('    _d.update(imports.{0}.{0}.get())\n'.format(s))
                reload(tools.getmetrics)

    def getmetrics(self):
        # call: getmetrics()
        # input: -
        # output: -
        try:
            # update the metrics from within tools.getmetrics._d
            tools.getmetrics.update()
            d = tools.getmetrics._d.copy()
            # add time category
            d['time'] = time.strftime('%c')

            if not os.path.exists('./tools/metrics'):
                os.mkdir('./tools/metrics')

            with open('./tools/metrics/metrics.json', 'w') as f:
                dump = json.dumps(d, indent=4)
                f.write(dump)
            self._storage.addDict(d)

        except IndentationError as e:
            print(e)
            print('--No metrics! Check the getmetrics.py file!--')


def main():
    queue = 'default'
    url = 'localhost'
    db = 'localhost'
    port = 27017

    if len(sys.argv) >= 2:
        if sys.argv[1].lower() in '"help"':
            print("""
        receive2.py [queue, url, db, port]

            Used to receive files for metrics collection

            queue - the queue in which to listen for messages
                    (default: 'default')
            url - the url at which the queue is
                    (default: 'localhost')
            db - the url where the database is located
                    (default: 'localhost')
            port - the port of the database
                    (default: '27017')

        Examples:
            receive2.py
            receive2.py default localhost localhost 27017

            """)
            return len(sys.argv)
        else:
            queue = sys.argv[1]
    if len(sys.argv) >= 3:
        url = sys.argv[2]
    if len(sys.argv) >= 4:
        db = sys.argv[3]
    if len(sys.argv) >= 5:
        port = sys.argv[4]

    r = Receive(url, db, port)
    print('Started listening')
    r.receive(queue)


if __name__ == '__main__':
    main()
