import requests
import json

from src.utils import User
from src.utils import export_gamemodes

# La base de donnée est gérée côté serveur, en JS, afin de :
# - Pouvoir gérer les autorisations des utilisateurs ayant accès au code source
#	- Facilité de connection, mongoose (JS) est bien supérieur à pymongo (Python)



def send(req: str, user: User, data: dict) -> requests.models.Response:
	"""Envoi une requête vers le serveur, méthode privée utilisée via des interfaces\n

	Args:
		req (str): Type de requête\n
		user (User): Utilisateur qui exécute la requête\n
		data (dict): Données supplémentaires à envoyer\n

	Returns:
		requests.models.Response: Objet réponse à une requête via le module requests\n
	"""
	url = "http://keyboard-master.vercel.app" + "/api/send"

	if user == None:
		user_pack = "null"
	else:
		user_pack = json.dumps({"name": user.name, "hashedPwd": user.hashed_password})

	if data == None:
		data = "null"
	
	pack = {
		"type": req,
		"user": user_pack,
		"pack": data
	}

	response = requests.post(url, data=pack)
	return response



def user_connection(is_new: bool, name: str, raw_password: str) -> User or None:
	"""Envoi une demande de connection/création d'utilisateur au serveur\n
	
	Args:
		is_new (bool): True si il s'agit d'une création, false si il s'agit d'une connection\n
		name (str): Username de l'utilisateur souhaité\n
		raw_password (str): Mot de passe pour s'y connecté (brute, non encrypté)\n

	Returns:
		User or None: Renvoi un objet User en cas de réussite, renvoi None sinon\n
	"""
	request = "CreateUser" if is_new else "LoginUser"

	data = {"name": name, "rawPwd": raw_password}
	res = send(req=request, user=None, data=json.dumps(data))

	if res.status_code != 201:
		print(f"Erreur: {res.status_code} - {res.text}")
		return None

	if res.text == "Denied":
		print(f"Connection refusée")
		return None
	
	print(f"Vous êtes connecté en tant que {name}")
	return User(name=name, hashed_password=res.text)



def join_matchmaking(user: User, gamemodes: list) -> str:
	"""Envoi une demande pour rejoindre le service de matchmaking au serveur\n

	Args:
		user (User): Utilisateur qui envoi la requête\n
		gamemodes (list): Liste de modes de jeu souhaités\n

	Returns:
		bool: True si demande acceptée par le serveur, sinon False\n
	"""
	data = json.dumps({"gamemodes": export_gamemodes(gamemodes)})
	res = send(req="JoinMatchmaking", user=user, data=data)
	return res.text



def leave_matchmaking(user: User) -> bool:
	"""Envoi une demande pour quitter le service de matchmaking au serveur\n

	Args:
		user (User): Utilisateur qui envoi la requête\n

	Returns:
		bool: True si demande acceptée par le serveur, sinon False\n
	"""
	res = send(req="LeaveMatchmaking", user=user, data=None)
	return res.text == "Allowed"



def query_sentence(gamemodes: list) -> str:
	"""Envoi une demande au serveur pour obtenir une phrase pour le jeu selon la difficulté\n

	Args:
		gamemodes (list): Liste de difficultés acceptées\n

	Returns:
		str: Phrase pour le jeu\n
	"""
	data = json.dumps({"gamemodes": export_gamemodes(gamemodes)})
	res = send(req="QuerySentence", user=None, data=data)
	return res.text



def set_score(user: User, gameID: int, score: int) -> bool:
	"""Envoi une demande de changement de score au serveur\n

	Args:
		user (User): Utilisateur qui envoi la requête\n
		gameID (int): ID de la game en cours\n
		score (int): Score à envoyer\n

	Returns:
		bool: True si demande acceptée par le serveur, sinon False\n
	"""
	data = json.dumps({"gameID": gameID, "score": score})
	res = send(req="SetMyScore", user=user, data=data)
	print(res.text)
	return res.text == "Allowed"



def retrieve_data(user: User, gameID: int) -> dict:
	"""Récupère actuelles les données d'une partie\n

	Args:
		user (User): Utilisateur qui envoi la requête\n
		gameID (int): ID de la game en cours\n

	Returns:
		dict: Données récupérées\n
	"""
	data = json.dumps({"gameID": gameID})
	res = send(req="RetrieveData", user=user, data=data)
	res = json.loads(res.text)
	res["gameID"] = gameID
	return res