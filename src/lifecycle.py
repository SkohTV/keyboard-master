import os

from dotenv import load_dotenv

from src.database import MongoDB









def set_alive():
	load_dotenv()
	#print(os.getenv("MongoAdmin"))
	#print(os.getenv("MongoUser"))