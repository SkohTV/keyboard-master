import tkinter as tk

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