import json
import io
import ast


class Converter(object):

        # Converter - class, extention of 'object'

        # Used mainly to convert from a type to another; work with .json files

        # Variables: -

        # Methods:
        #     fromTextToDict(
        #         text,
        #         key_value__delimiter='=',
        #         entry_demiliter='\n')

        #         converts a string into a dictonary
        #         the string must follow the structure:
        #             key=value\n
        #             key2=value2\n
        #             ...
        #             keyN=valueN\n
        #                 NOTE: this can be customisable

        #     fromDictToJson(d)
        #         converts a python dictionary to a json string and returns it

        #     printToFile(what, where)
        #         prints 'what' into a file 'where'.
        #         Mostly implemented for convenience

        #     makeJSON(inFile, outFile)
        #         converts a text file to a json file
        #         the file must be of structure
        #             key=value\n
        #             key2=value2\n
        #             ...
        #             keyN=valueN\n

        #     fromJSONtoDict(filePath)
        #         converts a json file into a python dictionary

        #     groupJSON(outFile, *inFiles)
        #         makes a new file with the name "outFile" and stores into it
        #         all the info from inFiles. inFiles MUST be .json

    def __init__(self):
        pass

    def fromTextToDict(
            self,
            text,
            key_value__delimiter='=',
            entry_demiliter='\n'):
        # call: fromTextToDict(text[, key_value__delimiter, entry_demiliter])
        # input: text - string with the format key=value \n key2=value2
        # output: d - dictionary containing all the keys and values from 'text'

        text = text.strip()
        d = {}

        for line in text.split(entry_demiliter):
            tmp = line.split(key_value__delimiter)
            if tmp != ['']:  # if we don't have weird lines like "=\n"
                d[tmp[0].strip()] = tmp[1].strip()  # begone, white spaces!

        return d

    def fromDictToJson(self, d):
        # call: fromTextToJson(d)
        # input: d - dictionary with info to be converted
        # output: s - string contaning info for a json file

        s = json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
        return s

    def printToFile(self, what, where):
        # call: printToFile(what, where)
        # input: what - string to be printed
        #       where - name of the file where 'what' should be printed in
        # output: -

        f = open('%s' % (where), 'w')
        f.write(what)
        f.close()

    def makeJSON(
            self,
            inFile,
            outFile,
            key_value__delimiter='=',
            entry_demiliter='\n'):
        # call: makeJSON(inFile, outFile)
        # input: inFile - string name of the input file
        #       outFile - string name of the output file
        # output: -
        try:
            # output of batch commands to a file may be encoded with utf16
            f = io.open(inFile, 'r', encoding='utf16')
            s = f.read()
        except UnicodeError:
            f = open(inFile, 'r')
            s = f.read()

        d = self.fromTextToDict(s, key_value__delimiter, entry_demiliter)
        j = self.fromDictToJson(d)

        self.printToFile(j, outFile)

        f.close()

    def fromJSONtoDict(self, filePath):
        # call: fromJSONtoKeys(filePath)
        # input: filePath - string; path of the .json file
        # output: d - dictionary of items

        with open(filePath) as f:
            return json.load(f)

    def groupJSON(self, outFile, *inFiles):
        # call: groupJSON(outFile, file1[, file2, file3, ...])
        # input: outFile - string; name of the file where all the
        #                  JSONs will be grouped into
        #       *inFiles - list of names of source files from which
        #                  the text will be grouped into a single file
        # output: -

        # basically adds the name of the file for each file, adds the contents
        #   of the file in the final JSON and indents it to look pretty
        s = ""
        for file in inFiles:
            if file[:-5] == ".json":
                # adds the ": " after each file name added
                s += '\n\t"' + file[:-5] + '":\n'
                with open(file, 'r') as f:
                    for line in f:
                        s += '\t' + line    # adds tabs
            else:
                s += '\n\t"' + file + '":\n'
                with open(file + ".json", 'r') as f:
                    for line in f:
                        s += '\t' + line
            s += ','
        s = s[:-1]  # removing a final comma to keep the file compatible

        s = "{" + s + "\n}"

        open(outFile, 'w').write(s)
