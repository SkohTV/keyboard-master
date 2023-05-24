"""
Connexion au serveur
===========

Ce module contient les fonctions pour se connecter au serveur distant et envoyer des requêtes

Contenu :
---------
- send: Envoi une requête vers le serveur, méthode privée utilisée via des interfaces
- user_connection: Envoi une demande de connection/création d'utilisateur au serveur
- join_matchmaking: Envoi une demande pour rejoindre le service de matchmaking au serveur
- leave_matchmaking: Envoi une demande pour quitter le service de matchmaking au serveur
- query_sentence: Envoi une demande au serveur pour obtenir une phrase pour le jeu selon la difficulté
- set_score: Envoi une demande de changement de score au serveur
- retrieve_data: Récupère actuelles les données d'une partie

"""



import json
import requests

from src.utils import User
from src.utils import export_gamemodes



# La base de donnée est gérée côté serveur, en JS, afin de :
# - Pouvoir gérer les autorisations des utilisateurs ayant accès au code source
#	- Facilité de connection, mongoose (JS) est bien supérieur à pymongo (Python)


#? Méthode d'encapsulation, uniquement utilisable via les interfaces de ce fichier
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

	# Si pas d'utilisateur, on envoi "null"
	if user is None:
		user_pack = "null"
	else:
		user_pack = json.dumps({"name": user.name, "hashedPwd": user.hashed_password})

	# Si pas de données, on envoi "null"
	if data is None:
		data = "null"

	# On met tout dans un paquet pour l'envoi
	pack = {
		"type": req,
		"user": user_pack,
		"pack": data
	}

	# On envoi la requête et la retourne
	response = requests.post(url, data=pack, timeout=10)
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
	# Selon la requête, soit on envoi une demande de création, soit une demande de connection
	request = "CreateUser" if is_new else "LoginUser"

	# On envoi la requête
	data = {"name": name, "rawPwd": raw_password}
	res = send(req=request, user=None, data=json.dumps(data))

	# Si le serveur renvoi "Denied", ou qu'il y a une erreur, on renvoi None
	if res.text == "Denied" or res.status_code != 201:
		return None

	# Sinon, on renvoi un objet User
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
	return res.text # Renvoi "denied" ou l'ID de la game



def leave_matchmaking(user: User) -> bool:
	"""Envoi une demande pour quitter le service de matchmaking au serveur\n

	Args:
		user (User): Utilisateur qui envoi la requête\n

	Returns:
		bool: True si demande acceptée par le serveur, sinon False\n
	"""
	res = send(req="LeaveMatchmaking", user=user, data=None)
	return res.text == "Allowed" # Renvoi true ou false selon si la demande a été acceptée



def query_sentence(gamemodes: list) -> str:
	"""Envoi une demande au serveur pour obtenir une phrase pour le jeu selon la difficulté\n

	Args:
		gamemodes (list): Liste de difficultés acceptées\n

	Returns:
		str: Phrase pour le jeu\n
	"""
	data = json.dumps({"gamemodes": export_gamemodes(gamemodes)})
	res = send(req="QuerySentence", user=None, data=data)
	return res.text # Renvoi la phrase



def set_score(user: User, game_id: int, score: int) -> bool:
	"""Envoi une demande de changement de score au serveur\n

	Args:
		user (User): Utilisateur qui envoi la requête\n
		gameID (int): ID de la game en cours\n
		score (int): Score à envoyer\n

	Returns:
		bool: True si demande acceptée par le serveur, sinon False\n
	"""
	data = json.dumps({"gameID": game_id, "score": score})
	res = send(req="SetMyScore", user=user, data=data)
	return res.text == "Allowed" # Renvoi true ou false selon si la demande a été acceptée



def retrieve_data(user: User, game_id: int) -> dict:
	"""Récupère actuelles les données d'une partie\n

	Args:
		user (User): Utilisateur qui envoi la requête\n
		gameID (int): ID de la game en cours\n

	Returns:
		dict: Données récupérées\n
	"""
	data = json.dumps({"gameID": game_id})
	res = send(req="RetrieveData", user=user, data=data)
	res = json.loads(res.text)
	res["gameID"] = game_id
	return res # Renvoi les données récupérées
