


def export_gamemodes(gamemodes: list) -> str:
	"""Transforme une list de gamemodes en string compressé pour l'envoi au serveur distant

	Args:
		gamemodes (list): Liste de gamemodes

	Returns:
		str: String compressé
	"""
	return "-".join(gamemodes)