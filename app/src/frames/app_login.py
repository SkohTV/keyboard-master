"""
Frame de connexion
===========

L'application est composée de 5 frames, chacune étant une page de l'application

Contenu :
---------
- AppLogin : Frame de connexion

"""



import tkinter as tk
from tkinter import ttk
from tkinter import font

from src.connect_server import user_connection as connect



class AppLogin(tk.Frame):
	"""
	Frame de connexion\n

	Attributes:
		controller (src.app.App): Classe tk.Tk principale qui controle la tk.Frame\n
		label_status (ttk.Label): Label d'état de connexion\n
		label_username (ttk.Label): Label de texte username\n
		entry_username (ttk.Entry): Entrée de l'username\n
		label_password (ttk.Label): Label de texte mot de passe\n
		entry_password (ttk.Entry): Entrée du mot de passe\n
		button_login (ttk.Button): Bouton de connexion\n
		button_register (ttk.Button): Bouton d'inscription\n

	Methods:
		__init__: Initialise l'objet\n
		interface_login: Interface de connexion\n
		interface_register: Interface d'inscription\n
	"""

	def __init__(self, parent: tk.Frame, controller) -> None:
		"""Initialisation de l'objet\n

		Args:
			parent (tk.Frame): Objet dont la classe inhérite\n
			controller (src.app.App): Classe tk.Tk principale qui controle la tk.Frame\n
		"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3, frame4 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_status = ttk.Label(frame1, text="Bonjour, merci de vous connecter")
		self.label_username = ttk.Label(frame2, text="Username :")
		self.entry_username = ttk.Entry(frame2)
		self.label_password = ttk.Label(frame3, text="Password :")
		self.entry_password = ttk.Entry(frame3, show="*")
		self.button_login = ttk.Button(frame4, text="Log in", width=10, command=self.interface_login, takefocus=0)
		self.button_register = ttk.Button(frame4, text="Register", width=10, command=self.interface_register, takefocus=0)

		# Changement de certains paramètres de style (police & couleur)
		self.label_status["font"] = font.Font(family="Verdana", weight="bold", size=10)
		self.label_status.config(foreground="#89CFF0")
		self.button_login["style"] = "small.TButton"
		self.button_register["style"] = "small.TButton"

		# Placement des widgets dans la fenêtre
		self.label_status.pack(side=tk.TOP)
		self.label_username.pack(side=tk.LEFT, padx=10)
		self.entry_username.pack(side=tk.RIGHT, padx=5)
		self.label_password.pack(side=tk.LEFT, padx=10)
		self.entry_password.pack(side=tk.RIGHT, padx=5)
		self.button_login.pack(side=tk.LEFT, padx=5)
		self.button_register.pack(side=tk.RIGHT, padx=5)

		# On pack les 4 frames
		frame1.pack(pady=10, fill=tk.X)
		frame2.pack(pady=5, padx=5, fill=tk.X)
		frame3.pack(padx=5, fill=tk.X)
		frame4.pack(pady=10)



	def interface_login(self) -> None:
		"""On fait une requête au serveur de connection d'utilisateur"""
		# Envoi de la requête
		res = connect(False, self.entry_username.get(), self.entry_password.get())
		if not res: # Refusé
			self.label_status.config(text="Identifiants invalides")
		else: # Accepté
			self.label_status.config(text="Connection réussie ! Redirection...")
			self.controller.user = res
			self.controller.send_event("UpdateName")
			self.controller.external_show_frame("AppMain")



	def interface_register(self) -> None:
		"""On fait une requête au serveur de création d'utilisateur"""
		# Envoi de la requête
		res = connect(True, self.entry_username.get(), self.entry_password.get())
		if not res: # Refusé
			self.label_status.config(text="Ce username est déjà utilisé")
		else: # Accepté
			self.label_status.config(text="Création réussie ! Redirection...")
			self.controller.user = res
			self.controller.send_event("UpdateName")
			self.controller.external_show_frame("AppMain")
