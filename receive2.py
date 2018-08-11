#!/usr/bin/env python
import platform
import sys
import os
import time
import json
import Receiver
import tools.getmetrics
from Repeat import Repeat
from StorageMongoDB import StorageMongoDB


class Receive(Receiver.Receiver):
    def __init__(self, url='localhost', db='localhost', port=27017):
        Receiver.Receiver.__init__(self, url)
        self._storage = StorageMongoDB(db, port)
        self._repeater = Repeat(-1, self.getmetrics)
        try:
            with open('./tools/timer', 'r') as f:
                i = float(f.read())
            self._repeater = Repeat(i, self.getmetrics)
            self._repeater.start()
        except IOError:
            print('    Could not find "timer" file!')

        if not os.path.exists('tools'):
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
        filename, contents = body.split('?\n')
        print("-----------------------")
        print(" [x] Received %r at %r" % (filename, time.strftime("%c")))

        if filename == 'timer':
            with open('./tools/timer', 'w') as f:
                f.write(contents)
            if float(contents) == -1:
                self._repeater.stop()
            elif float(contents) > 0:
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
            if not s in imp:
                with open('./tools/imports.py', 'a') as f:
                    f.write('import ' + s + '\n')
                with open('./tools/getmetrics.py', 'a') as f:
                    f.write('    _d.update(imports.{0}.{0}.get())\n'.format(s))
                reload(tools.getmetrics)
        
    def getmetrics(self):
        try:
            tools.getmetrics.update()
            d = tools.getmetrics._d.copy()
            d['time'] = time.strftime('%c')

            if not os.path.exists('./tools/metrics'):
                os.mkdir('./tools/metrics')

            with open('./tools/metrics/metrics.json', 'w') as f:
                dump = json.dumps(d, indent=4)
                f.write(dump)
            self._storage.addDict(d)

        except IndentationError:
            print('--No metrics--')


queue = 'default'
url = 'localhost'
db = 'localhost'
port = 27017

if len(sys.argv) >= 2:
    queue = sys.argv[1]
if len(sys.argv) >= 3:
    url = sys.argv[2]
if len(sys.argv) >= 4:
    db = sys.argv[3]
if len(sys.argv) >= 5:
    port = sys.argv[4]

r = Receive()
print('Started listening')
r.receive()
