from pymongo import MongoClient

class StorageMongoDB(object):
	def __init__(self, name, port=27017):
		self.client = MongoClient(name, port)
		self.db = self.client.examples

	def addDict(self, d):
		self.db.autos.insert(d)

	def getDict(self, d={}):
		return self.db.autos.find(d)

