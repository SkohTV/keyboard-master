import sys
import tkinter as tk
import tkinter.ttk as ttk
from _tkinter import TclError

from ttkbootstrap import Style

from src.connect_server import user_connection as connect


from src.ttk_windows.app_main import App_Main




class App_Login(tk.Frame):
	def __init__(self, parent, controller):
		"""Initialisation de l'objet"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3, frame4 = tk.Frame(self), tk.Frame(self), tk.Frame(self), tk.Frame(self)

		# Définition des widgets
		self.label_status = tk.Label(frame1, text="Bonjour, merci de vous connecter")
		self.label_username = tk.Label(frame2, text="Username :")
		self.entry_username = tk.Entry(frame2)
		self.label_password = tk.Label(frame3, text="Password :")
		self.entry_password = tk.Entry(frame3)
		self.button_login = ttk.Button(frame4, text="Log in", width=10, command=self.interface_login)
		self.button_register = ttk.Button(frame4, text="Register", width=10, command=self.interface_register)

		# Placement des widgets dans la fenêtre
		self.label_status.pack(side=tk.TOP)
		self.label_username.pack(side=tk.LEFT, padx=5)
		self.entry_username.pack(side=tk.RIGHT, padx=5)
		self.label_password.pack(side=tk.LEFT, padx=5)
		self.entry_password.pack(side=tk.RIGHT, padx=5)
		self.button_login.pack(side=tk.LEFT, padx=5)
		self.button_register.pack(side=tk.RIGHT, padx=5)

		# On pack les 4 frames
		frame1.pack(pady=10, fill=tk.X)
		frame2.pack(pady=5, fill=tk.X)
		frame3.pack(fill=tk.X)
		frame4.pack(pady=20)


	def interface_login(self):
		"""On fait une requête au serveur de connection d'utilisateur"""
		res = connect(False, self.entry_username.get(), self.entry_password.get())
		if not res:
			self.label_status.config(text="Identifiants invalides")
		else:
			self.label_status.config(text="Connection réussie ! Redirection...")
			self.controller.show_frame(App_Main)


	def interface_register(self):
		"""On fait une requête au serveur de création d'utilisateur"""
		res = connect(True, self.entry_username.get(), self.entry_password.get())
		if not res:
			self.label_status.config(text="Ce username est déjà utilisé")
		else:
			self.label_status.config(text="Création réussie ! Redirection...")
			self.controller.show_frame(App_Main)
