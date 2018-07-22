from pymongo import MongoClient

class StorageMongoDB(object):
	def __init__(self, host='localhost', port=27017):
		self.client = MongoClient(host, port)
		self.db = self.client.client

	def addDict(self, d):
		self.db.metrics.insert_one(d)

	def getDict(self, d={}):
		return self.db.metrics.find_one(d)

	def getAll(self):
		return list(self.db.metrics.find())

