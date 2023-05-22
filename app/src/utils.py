from typing import Callable
import threading


def export_gamemodes(gamemodes: list) -> str:
	"""Transforme une list de gamemodes en string compressé pour l'envoi au serveur distant\n

	Args:
		gamemodes (list): Liste de gamemodes\n

	Returns:
		str: String des gamemodes séparés par un "-"\n
	"""
	return "-".join(gamemodes)


# https://stackoverflow.com/a/19846691
def threaded(fn: Callable) -> Callable:
	"""Permet de passer une fonction en threading via un décorateur\n

	Args:
		fn (function): Fonction à passer en thread\n

	Returns:
		function: Fonction en thread\n
	"""
	def wrapper(*args, **kwargs):
		threading.Thread(target=fn, args=args, kwargs=kwargs).start()
	return wrapper



class User:
	"""Class utilisateur utilisée pour garder les informations de connection en mémoire"""
	def __init__(self, name: str = None, hashed_password: str = None) -> None:
		"""Initialise un objet User\n

		Args:
			name (str, optional): Username de l'utilisateur\n
			hashed_password (str, optional): Password encrypté de l'utilisateur\n
		"""
		self.name = name
		self.hashed_password = hashed_password
