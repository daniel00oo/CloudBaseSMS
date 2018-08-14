import sys
from StringIO import StringIO
import mock
import unittest
from Receiver import Receiver
from Sender import Sender
from receive2 import Receive


class Testing(unittest.TestCase):
    @mock.patch('Receiver.pika')
    def testReceiver(self, mock_pika):
        mock_pika.ConnectionParameters.return_value = "some"
        r = Receiver()

        mock_pika.BlockingConnection.assert_called_with("some")

    @mock.patch('Receiver.pika')
    def testReceiverQueueDec(self, mock_pika):
        r = Receiver()
        r.queueDec("queueDec")

        mock_pika.BlockingConnection.return_value.channel.return_value.queue_declare.assert_called_with(durable=True, queue='queueDec')

    @mock.patch.object(Receiver, 'callback')
    @mock.patch('Receiver.pika')
    def testReceiverSetReceive(self, mock_pika, mock_callback):
        r = Receiver()
        r.callback = "some method"
        r.setReceive("queueRec")

        mock_pika.BlockingConnection.return_value.channel.return_value.basic_consume.assert_called_with('some method', queue='queueRec')

    @mock.patch('Receiver.pika')
    def testReceiverReceive(self, mock_pika):
        r = Receiver()
        r.receive('queue')

        mock_pika.BlockingConnection.return_value.channel.return_value.start_consuming.assert_called_with()

    @mock.patch('Receiver.pika')
    def testReceiverCancel(self, mock_pika):
        r = Receiver()
        r.cancel('consumer')

        mock_pika.BlockingConnection.return_value.channel.return_value.basic_cancel.assert_called_with(consumer_tag='consumer')

    @mock.patch('Sender.pika')
    def testSender(self, mock_pika):
        mock_pika.ConnectionParameters.return_value = "some"
        s = Sender()

        mock_pika.BlockingConnection.assert_called_with("some")

    @mock.patch('Sender.pika')
    def testSenderClose(self, mock_pika):
        s = Sender()
        s.close()

        mock_pika.BlockingConnection.return_value.close.assert_called_with()

    @mock.patch('Sender.pika')
    def testSenderQueueDec(self, mock_pika):
        s = Sender()
        s.queueDec('queueDec')

        mock_pika.BlockingConnection.return_value.channel.return_value.queue_declare.assert_called_with(durable=True, queue='queueDec')

    # mock the print
    @mock.patch('sys.stdout', new_callable=StringIO)
    # mock the queueDec method from Sender
    @mock.patch.object(Sender, 'queueDec')
    @mock.patch('Sender.pika')
    def testSenderSend(self, mock_pika, mock_dec, mock_print):
        s = Sender()
        mock_pika.BasicProperties.return_value = ''
        s.send("some message")

        mock_pika.BlockingConnection.return_value.channel.return_value.basic_publish.assert_called_with(body="some message", exchange='', properties= '', routing_key='default')

    @mock.patch('receive2.Receive.getmetrics')
    @mock.patch('receive2.StorageMongoDB')
    @mock.patch('receive2.Receiver.pika')
    @mock.patch('receive2.Repeat')
    @mock.patch('receive2.os')
    @mock.patch('__builtin__.open')
    def testreceive2(self, mock_open, mock_os, mock_repeat, mock_pika, mock_storage, mock_getmetrics):
        mock_os.path.exists.return_value = False
        mock_open.return_value.read.return_value = 1

        r = Receive()

        mock_os.mkdir.assert_called_with('tools')
        # the second argument is a mock object representing a function
        assert mock_repeat.call_args[0][0] == 1

    @mock.patch('receive2.reload')
    @mock.patch('receive2.Repeat')
    @mock.patch('__builtin__.open')
    @mock.patch('sys.stdout', new_callable=StringIO)
    def testreceive2HowToProcess(self, mock_print, mock_open, mock_repeat, mock_reload):
        body = "timer?\n1"
        r = Receive()
        r.howToProcess(body)

        mock_open.assert_called_with('./tools/timer', 'w')
        mock_repeat.return_value.start.assert_called_with()
        mock_repeat.return_value.stop.assert_called_with()

        body = "Cpuinfo.py?\nclass Someclass():\n    pass"
        r.howToProcess(body)

        mock_open.assert_called_with('./tools/getmetrics.py', 'a')

    @mock.patch('receive2.tools.getmetrics')
    @mock.patch('receive2.StorageMongoDB')
    @mock.patch('receive2.os')
    @mock.patch('receive2.reload')
    @mock.patch('__builtin__.open')
    @mock.patch('receive2.json')
    @mock.patch('receive2.time')
    def testreceive2Getmetrics(self, mock_time, mock_json, mock_open, mock_reload, mock_os, mock_storage, mock_getmetrics):
        mock_getmetrics._d.copy.return_value = {1:1}
        mock_time.strftime.return_value = 'time'

        d = {1: 1, 'time': 'time'}

        r = Receive()
        r.getmetrics()

        mock_getmetrics.update.assert_called_with()
        mock_json.dumps.assert_called_with(d, indent=4)
        mock_storage.return_value.addDict.assert_called_with(d)


unittest.main()
