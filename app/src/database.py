import os
import requests

# La base de donnée est gérée côté serveur, en JS, afin de :
# - Pouvoir gérer les autorisations d'écriture/lecture des utilisateurs ayant accès au code source
#	- Facilité de connection, mongoose (JS) est bien supérieur à pymongo (Python)




def send(type, user, data):
	url = os.getenv("SERVER_URL") + "/send"

	if user == None:
		user = "null"
	if data == None:
		data = "null"
	
	pack = {
		"type": type,
		"user": user,
		"pack": data
	}

	response = requests.post(url, data=pack)
	return response

def receive():
	pass