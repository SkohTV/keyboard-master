import sys
import tkinter as tk
import tkinter.ttk as ttk
from _tkinter import TclError

from ttkbootstrap import Style

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, query_sentence as query

from src.frames.app_login import App_Login
from src.frames.app_main import App_Main
from src.frames.app_solo import App_Solo
from src.frames.app_matchmaking import App_Matchmaking
from src.frames.app_multi import App_Multi

from src.utils import User



class App(tk.Tk):
	def __init__(self) -> str:
		"""Initialisation de l'objet"""
		# On utilise l'init de l'objet Tkinter de base
		tk.Tk.__init__(self)

		# On gardera l'utilisateur dans la classe, pour y accéder plus facilement (global == mauvaise pratique)
		self.user = User()
  
		# Valeurs réutilisées dans des frames, nécessaires ici pour y accéder
		self.username = tk.StringVar()
		self.versusname = tk.StringVar()
		self.sentence = tk.StringVar()
		self.username.set("null")
		self.github_icon = tk.PhotoImage(file="ico/github.png")

		# On attrape l'event de fermeture de la fenêtre, pour pouvoir clore le script
		self.protocol("WM_DELETE_WINDOW", self.on_close)

		# Change les paramètres basiques de la fenêtre
		self.resizable(False, False)

		# On gère le style via ttkbootstrap (juste un thème par défaut)
		self.style = Style()
		self.style.theme_use("darkly")

		# Le chargement de l'icône peut échouer (si l'utilisateur est sous Linux par exemple)
		# On va donc tenter de de set l'icône, et si ça échoue on passe à la suite
		try:
			self.iconbitmap("ico/keyboard.ico")
		except TclError:
			pass

		# On crée un pack pour englober la frame
		container = tk.Frame(self, height=400, width=700)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# On ajoute les frames à un dictionnaire
		self.frames = {}
		for F in (App_Login, App_Main, App_Solo, App_Matchmaking, App_Multi):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		# On affiche la frame de login
		self.show_frame(App_Login)


	def show_frame(self, cont) -> None:
		frame = self.frames[cont]
		if cont == App_Login:
			self.title("Login")
			self.geometry("285x155")
		else:
			self.title("Keyboard Master")
			self.geometry("700x400")
		frame.tkraise()


	def on_close(self):
		"""Shutdown le programme Python lorsqu'on ferme la fenêtre, pour éviter d'ouvrir la fenêtre de jeu"""
		self.destroy()
		sys.exit()


	def start_matchmaking(self):
		pass


	def send_event(self, event: str) -> None:
		self.event_generate(f"<<{event}>>")