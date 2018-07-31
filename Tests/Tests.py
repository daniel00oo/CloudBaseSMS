import sys
sys.path.insert(0, "../")
from StringIO import StringIO
import mock
import unittest
from Runner import Runner
from Converter import Converter
from Receiver import Receiver
from Sender import Sender


class Testing(unittest.TestCase):
    # nothing will be executed
    @mock.patch('Runner.subprocess.call')
    # mocking os
    @mock.patch('Runner.os')
    # the converter shall return fake dictionaries
    @mock.patch('Converter.Converter')
    def testRunRun(self, mock_conv, mock_os, mock_subprocess):
        d2 = {'Windows': [1, 2, 3]}

        # make the path return a list which we need to format the output file
        mock_os.path.join.return_value = ['some',  'path']
        mock_os.path.basename.return_value = "some"
        mock_os.path.dirname.return_value = "some"
        mock_os.getcwd.return_value = "some"
        # injects a fake dictonary to search the files
        mock_conv.return_value.fromJSONtoDict.return_value = d2

        # loading a file
        r = Runner('some file')
        # running on an operating system
        r.run("Windows")

        mock_conv.return_value.fromJSONtoDict.assert_called_with("some")
        mock_os.chdir.assert_called_with("some")
        mock_subprocess.assert_called_with('some path /format:list > Windows.txt', shell=True)

    def testConverterFromTextToDict(self):
        c = Converter()

        # example input
        t = """
            text1=text2

        """
        # desired output
        d = {'text1': 'text2'}

        assert c.fromTextToDict(t, '=', '\n') == d

    def testConverterFromDictToJson(self):
        c = Converter()

        # example input
        d = {'text1': 'text2'}
        # desired output
        t = """{
    "text1": "text2"
}"""
        assert c.fromDictToJson(d) == t

    # mocking out the built in open method
    @mock.patch('__builtin__.open')
    # mocking out the io open method
    @mock.patch('io.open')
    def testConverterMakeJSON(self, mock_io_open, mock_open):
        t = """
    text1=text2
        """

        # simulating a file that contains the text from t
        mock_io_open.return_value.read.return_value = t

        c = Converter()
        c.makeJSON("in", "out")

        mock_io_open.assert_called_with('in', 'r', encoding='utf16')
        mock_open.assert_called_with('out', 'w')

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


unittest.main()
