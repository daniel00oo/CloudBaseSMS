from pymongo import MongoClient

class StorageMongoDB(object):
	"""
		StorageMongoDB - class

		Used to store info in a given MongoDB database

		Variables:
			client - instance of MongoClient
			db - instance of a MongoDB collection, used to store info

		Methods:
			addDict(d)
				Adds a dictionary to the database
			getDict(d)
				Gets a single entry from the database that matches the given dictionary d
			getAll()
				Gets ALL entries from the database


	"""
	def __init__(self, host='localhost', port=27017):
		self.client = MongoClient(host, port)
		self.db = self.client.client

	def addDict(self, d):
		#call: addDict(d)
		#input: d - python dictionary, what you want to be inserted in the database
		#output: -
		self.db.metrics.insert_one(d)

	def getDict(self, d):
		#call: getDict(d)
		#input: d - python dictionary, used to match wanted output
		#			empty dictionary for the first entry
		#output: a python dictionary that matches the input;
		#		or None if nothing matches the input
		return self.db.metrics.find_one(d)

	def getAll(self):
		#call: getAll()
		#input: -
		#output: a list of all the entries in the database
		return list(self.db.metrics.find())