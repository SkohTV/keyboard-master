import os
from pymongo import MongoClient



class MongoDB:
	def __init__(self, connection_string) -> None:
		self.client = MongoClient(connection_string)
		self.matchmakingDB = self.client["Database"]["Matchmaking"]
		self.sentenceDB = self.client["Database"]["Sentence"]