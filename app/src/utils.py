"""
Utilitaires
===========

Ce module contient des fonctions et une classe utilitaires pour le traitement des données et l'exécution en threading

Contenu :
---------
- export_gamemodes: Transforme une list de gamemodes en string compressé pour l'envoi au serveur distant
- threaded: Permet de passer une fonction en threading via un décorateur
- User: Initialise un objet User

"""



import time
import threading
from typing import Callable

from pynput import keyboard



def export_gamemodes(gamemodes: list) -> str:
	"""Transforme une list de gamemodes en string compressé pour l'envoi au serveur distant\n

	Args:
		gamemodes (list): Liste de gamemodes\n

	Returns:
		str: String des gamemodes séparés par un "-"\n
	"""
	return "-".join(gamemodes)


# https://stackoverflow.com/a/19846691
def threaded(func: Callable) -> Callable:
	"""Permet de passer une fonction en threading via un décorateur\n

	Args:
		func (function): Fonction à passer en thread\n

	Returns:
		function: Fonction en thread\n
	"""
	def wrapper(*args, **kwargs):
		threading.Thread(target=func, args=args, kwargs=kwargs).start()
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



class WrapListener():
	"""Wrapper pour une longue fonction partagée dans AppSolo et AppMulti"""

	def __init__(self) -> None:
		"""Initialise un objet sans rien dedans (on n'initialise jamais cette classe directement)"""
		self.written = []
		self.sentence = ""
		self.label_hello = None
		self.label_you = None
		self.text_entry = None
		self.start_time = None
		self.current_time = None
		self.thread = None
		self.controller = None


	@threaded
	def listen_keypresses(self) -> None:
		"""Ecoute et réagit aux touches pressées pour le jeu"""

		def on_press(key: keyboard.Key) -> None:
			"""Fonction appelée par le listener lorsqu'une touche est pressée\n

			Args:
				key (keyboard.Key): Touche pressée\n
			"""
			if key == keyboard.Key.space: # Touche = espace
				key = " "
			elif key == keyboard.Key.backspace: # Touche = backspace (supprimer)
				key = "backspace"
			else:
				try: # Touche = touche alphanumérique
					key = key.char
				except AttributeError: # Touche = autre truc qu'on s'en fiche
					return

			# Si backspace, alors on remove un item de la liste de trucs écrit
			if key == "backspace":
				if self.written:
					for i in ("good", "wrong", "empty", "wrong-space"):
						self.text_entry.tag_remove(i, f"1.{len(self.written)-1}", f"1.{len(self.written)}")
					self.written.pop()
				return

			# Sinon, on n'as pas fini d'écrire
			if len(self.written) < len(self.sentence):
				if self.start_time is None: # Si c'est la PREMIERE fois qu'on écrit
					self.start_time = time.time()
					self.label_hello.config(text="Écrivez le plus vite possible !")

				# On ajoute la touche alphanumérique (ou espace) à la liste
				self.written.append(key)

			# On remove tous les tags de la lettre qu'on viens d'écrire
			for i in ("good", "wrong", "empty", "wrong-space"):
				self.text_entry.tag_remove(i, f"1.{len(self.written)-1}", f"1.{len(self.written)}")

			if key == self.sentence[len(self.written)-1]: # Si c'est la bonne lettre
				self.text_entry.tag_add("good", f"1.{len(self.written)-1}", f"1.{len(self.written)}")
			else: # Si c'est la mauvaise lettre
				if self.sentence[len(self.written)-1] == " " or not self.sentence[len(self.written)-1].isalnum(): # Si c'est un alphanumérique
					self.text_entry.tag_add("wrong-space", f"1.{len(self.written)-1}", f"1.{len(self.written)}")
				else: # Si c'est un espace
					self.text_entry.tag_add("wrong", f"1.{len(self.written)-1}", f"1.{len(self.written)}")

			# Si tout est écrit, on check si tout est bon
			if len(self.written) >= len(self.sentence):
				wrong = len(self.sentence)
				for index, elem in enumerate(self.sentence):
					if elem == self.written[index]:
						wrong -= 1
				if wrong == 0:
					self.thread = False
					self.label_hello.config(text=f"Votre score est de : {len(self.written) / (self.current_time - self.start_time) : .3f}cps")
					self.label_you.configure(text=f"{self.controller.user.name} : {len(self.written) / (self.current_time - self.start_time) : .3f}cps")

		# On crée un listener, pour écouter les touches
		with keyboard.Listener(on_press=on_press) as listener:
			def stop_event(): # Fonction stop event ici, afin d'être appelable dans la closure du with
				self.thread = True
				while self.thread:
					time.sleep(0.01)
				listener.stop()

			# On démarre un thread, il est stoppé tout seul quand self.thread = False
			threading.Thread(target=stop_event).start()
			listener.join()
