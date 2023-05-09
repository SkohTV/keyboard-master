import os
import json
import tkinter as tk
from time import sleep

import ttkbootstrap as ttk
from dotenv import load_dotenv

from src.connect_server import user_connection as connect, join_matchmaking as join, leave_matchmaking as leave, query_sentence as query




#user = connect(False, "Skoh", "abcde")
#print(join(user, ["easy", "insane"]))
#sleep(2)
#print(leave(user))
#res = query(gamemodes=["easy","insane"])
#print(res)

		#self.geometry("700x400")


class App_Login(tk.Tk):
	def __init__(self) -> None:
		# On utilise l'init de l'objet Tkinter de base
		tk.Tk.__init__(self)

		# Change les paramètres basiques de la fenêtre
		self.resizable(False, False)
		#self.iconbitmap("./ico/keyboard.ico")
		self.title("Login")

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
		res = connect(False, self.entry_username.get(), self.entry_password.get())
		if not res:
			self.label_status.config(text="Identifiants invalides")
		else:
			self.label_status.config(text="Connection réussie ! Redirection...")


	def interface_register(self):
		res = connect(True, self.entry_username.get(), self.entry_password.get())
		if not res:
			self.label_status.config(text="Ce username est déjà utilisé")
		else:
			self.label_status.config(text="Connection réussie ! Redirection...")




