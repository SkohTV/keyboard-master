import sys
import tkinter as tk
from _tkinter import TclError

import ttkbootstrap as ttk

from src.connect_server import user_connection as connect



class App_Login(tk.Tk):
	def __init__(self) -> None:
		"""Initialisation de l'objet"""
		# On utilise l'init de l'objet Tkinter de base
		tk.Tk.__init__(self)

		# On attrape l'event de fermeture de la fenêtre, pour pouvoir clore le script
		self.protocol("WM_DELETE_WINDOW", self.on_close)

		# Change les paramètres basiques de la fenêtre
		self.resizable(False, False)
		self.title("Login")

		# Le chargement de l'icône peut échouer (si l'utilisateur est sous Linux par exemple)
		# On va donc tenter de de set l'icône, et si ça échoue on passe à la suite
		try:
			self.iconbitmap("ico/keyboard.ico")
		except TclError:
			pass

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3, frame4 = tk.Frame(self), tk.Frame(self), tk.Frame(self), tk.Frame(self)

		# Définition des widgets
		self.label_status = tk.Label(frame1, text="Bonjour, merci de vous connecter")
		self.label_username = tk.Label(frame2, text="Username")
		self.entry_username = tk.Entry(frame2)
		self.label_password = tk.Label(frame3, text="Password")
		self.entry_password = tk.Entry(frame3)
		self.button_login = tk.Button(frame4, text="Log in", width=10, command=self.interface_login)
		self.button_register = tk.Button(frame4, text="Register", width=10, command=self.interface_register)

		# Placement des widgets dans la fenêtre
		self.label_status.pack(side=tk.TOP)
		self.label_username.pack(side=tk.LEFT)
		self.entry_username.pack(side=tk.RIGHT)
		self.label_password.pack(side=tk.LEFT)
		self.entry_password.pack(side=tk.RIGHT)
		self.button_login.pack(side=tk.LEFT, padx=5)
		self.button_register.pack(side=tk.RIGHT, padx=5)

		# On pack les 4 frames
		frame1.pack(pady=5)
		frame2.pack(pady=5)
		frame3.pack()
		frame4.pack(pady=10)

		# On calcul une taille dynamique pour la fenêtre
		widget_width = self.label_username.winfo_reqwidth() + self.entry_username.winfo_reqwidth() + 40
		widget_height = self.label_status.winfo_reqheight() + self.label_username.winfo_reqheight() + self.label_password.winfo_reqheight() + self.button_login.winfo_reqheight() + 40

		# On change la taille de la fenêtre
		self.geometry('{}x{}'.format(widget_width, widget_height))


	def interface_login(self):
		"""On fait une requête au serveur de connection"""
		res = connect(False, self.entry_username.get(), self.entry_password.get())
		if not res:
			self.label_status.config(text="Identifiants invalides")
		else:
			self.label_status.config(text="Connection réussie ! Redirection...")
			self.destroy()


	def interface_register(self):
		"""On fait une requête au serveur de création d'utilisateur"""
		res = connect(True, self.entry_username.get(), self.entry_password.get())
		if not res:
			self.label_status.config(text="Ce username est déjà utilisé")
		else:
			self.label_status.config(text="Connection réussie ! Redirection...")
			self.destroy()


	def on_close(self):
		"""Shutdown le programme Python lorsqu'on ferme la fenêtre, pour éviter d'ouvrir la fenêtre de jeu"""
		self.destroy()
		sys.exit()
