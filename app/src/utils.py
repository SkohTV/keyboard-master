from typing import Callable
import tkinter as tk
import threading

class User:
	def __init__(self, name: str = None, hashed_password: str = None) -> None:
		self.name = name
		self.hashed_password = hashed_password


def export_gamemodes(gamemodes: list) -> str:
	"""Transforme une list de gamemodes en string compressé pour l'envoi au serveur distant

	Args:
		gamemodes (list): Liste de gamemodes

	Returns:
		str: String compressé
	"""
	return "-".join(gamemodes)


# https://stackoverflow.com/questions/19846332/python-threading-inside-a-class
def threaded(fn: Callable) -> Callable:
	"""Permet de passer une fonction en threading via un décorateur

	Args:
		fn (function): Fonction à passer ne thread

	Returns:
		function: Fonction en thread
	"""
	def wrapper(*args, **kwargs):
		threading.Thread(target=fn, args=args, kwargs=kwargs).start()
	return wrapper