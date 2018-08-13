#!/usr/bin/env python
from Sender import Sender
import sys
import os


def sendFile(file, url='localhost', queue='default'):
    s = Sender(url)
    text = os.path.basename(file) + '?\n'

    with open(file, 'r') as f:
        text += f.read()

    s.send(text, queue)


def main():
    # argument count
    ac = len(sys.argv)
    url = 'localhost'
    queue = 'default'

    if ac == 1:
        h = """
    send [file, queue, url]

        Used to send files via RabbitMQ to consumer nodes

        file - the file you want to be sent
        queue - the queue for the file to be send to. This will
            influence where the file will be redirected.
                (default: "default")
        url	- the url that will be used to store info via RabbitMQ
            (default: "localhost")

    Examples:
        send.py
        send.py file.py
        send.py test_metrics/Cpuinfo.py

            """

        print(h)
        return(ac)

    if ac >= 4:
        url = sys.argv[3]
    if ac >= 3:
        queue = sys.argv[2]
    if ac >= 2:
        print("==> Sending mesage %r in queue %r" % (sys.argv[1], queue))
        try:
            sendFile(sys.argv[1], url, queue)
        except IOError as e:
            print(e)

    return(ac)


if __name__ == '__main__':
    main()
