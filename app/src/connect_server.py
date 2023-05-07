import os
import requests
import json

from src.structs import User

# La base de donnée est gérée côté serveur, en JS, afin de :
# - Pouvoir gérer les autorisations d'écriture/lecture des utilisateurs ayant accès au code source
#	- Facilité de connection, mongoose (JS) est bien supérieur à pymongo (Python)



def send(type: str, user: User, data: dict):
	url = os.getenv("SERVER_URL") + "/api/send"

	user_pack = {"name": user.name, "hashedPwd": user.hashed_password} if user else "none"
	data_pack = data if data else "none"

	pack = {
		"type": type,
		"user": user,
		"pack": data
	}

	print(json.dumps(pack))

	response = requests.post(url, data=json.dumps(pack))
	return response



def user_connection(is_new: bool, name: str, raw_password: str) -> User or None:
	"""Envoi une demande de connection/création d'utilisateur au serveur\n
	
	Args:
		is_new (bool): True si il s'agit d'une création, false si il s'agit d'une connection\n
		name (str): Username de l'utilisateur souhaité\n
		raw_password (str): Mot de passe pour s'y connecté (brute, non encrypté)\n

	Returns:
		User or None: Renvoi un objet User en cas de réussite, renvoi None sinon
	"""
	request = "CreateUser" if is_new else "LoginUser"

	data = {"name": name, "rawPwd": raw_password}
	res = send(type=request, user=None, data=data)

	if res.status_code != 201:
		print(f"Erreur: {res.status_code} - {res.text}")
		return None

	if res.text == "Denied":
		print(f"Connection refusée")
		return None
	
	print(f"Vous êtes connecté en tant que {name}")
	return User(name=name, hashed_password=res.text)



def join_matchmaking(user: User, gamemodes: str) -> bool:
	res = send(type="JoinMatchmaking", user=user, data={"gamemodes": gamemodes})
	return res == "Allowed"



def leave_matchmaking():
  pass



def query_sentence():
  pass