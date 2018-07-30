import os
import subprocess
import Converter


class Runner(object):

    def __init__(self, loadFile):

            # Runner - class
            #     Executes commands from files specified in
            #       'files.json' as {"command": "file path"}

            # Variables:
            #     cwd - string, current working directory
            #     conv - instance of Converter class,
            #            used to convert json files to python
            #            dictionary and vice-versa
            #     commands - python dictionary, used to store
            #                the path to the commands of all
            #                operating systems
            #     osFormat - python dictionary, used to store
            #                the necessary formating for the files

            # Methods:
            #     run(operatingSystem)
            #         Executes throught OS calls commands to get the metrics
            #         and stores them in a file named 'metrics.json'

        self.cwd = os.getcwd()  # current working directory
        self.conv = Converter.Converter()

        # dictionary of shortcuts to actual files
        #   {"Operating system" : ["path", "to", "commands"]}
        # access a command:
        #    r = Runner(filePath)
        #    r.commands[operatingSystem][command]
        self.commands = self.conv.fromJSONtoDict(loadFile)

        for operatingSystem in self.commands:
            # for portability, we use os.path.join to join
            #   the path with the correct OS separator
            self.commands[operatingSystem] = os.path.join(
                *self.commands[operatingSystem])

        self.osFormat = {}
        self.osFormat['Windows'] = ['/format:list', '>']
        self.osFormat['Linux'] = ['>']

        self.delimiters = {}
        self.delimiters['Windows'] = ['=', '\n']
        self.delimiters['Linux'] = [':', '\n']

    def run(self, operatingSystem):
        # call: run(operatingSystem)
        # input: operatingSystem - string, name of the host operating system
        # output: -

        # changing directory to commands directory
        os.chdir(os.path.dirname(self.commands[operatingSystem]))
        # loading json file into memory as a dict
        d = self.conv.fromJSONtoDict(
            os.path.basename(self.commands[operatingSystem]))

        if not os.path.isdir('metrics'):
            # making directory to store the metrics to look tidy
            os.mkdir('metrics')

        os.chdir('metrics')

        for cmd in d:
            # formatting the output to match the requirements
            #   for the converter instance to manage converting
            #   and then outputting it to a file with
            #   the same name as the command
            command = d[cmd] + self.osFormat[operatingSystem] + ['%s.txt' % cmd]
            command = ' '.join(command)
            subprocess.call(command, shell=True)
            # converting to .json files
            self.conv.makeJSON(
                '%s.txt' % cmd,
                '%s.json' % cmd,
                *self.delimiters[operatingSystem])

        self.conv.groupJSON('metrics.json', *d.keys())

        # changing the working directory back to the original
        os.chdir(self.cwd)
