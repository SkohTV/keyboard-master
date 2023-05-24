"""
Frame de choix du mode de jeu
===========

L'application est composée de 5 frames, chacune étant une page de l'application

Contenu :
---------
- AppMain : Frame de choix du mode de jeu

"""



import tkinter as tk
from tkinter import ttk
from tkinter import font
import webbrowser



class AppMain(tk.Frame):
	"""
	Frame de choix du mode de jeu\n

	Attributes:
		controller (src.app.App): Classe tk.Tk principale qui controle la tk.Frame\n
		label_hello (ttk.Label): Label de bienvenue\n
		button_solo (ttk.Button): Bouton de jeu solo\n
		button_versus (ttk.Button): Bouton de jeu versus\n
		github_icon (ttk.Label): Label de l'icône GitHub\n
		reskin (ttk.Label): Label de l'icône de reskin\n
		github_icon (ttk.Label): Label de l'icône GitHub\n
		reskin (ttk.Label): Label de l'icône de reskin\n

	Methods:
		__init__: Initialise l'objet\n
		button_solo: Bouton de jeu solo\n
		button_versus: Bouton de jeu versus\n
		update_name: Met à jour le nom de l'utilisateur\n
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
		frame1, frame2, frame3 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1, text="Bonjour null")
		self.button_solo = ttk.Button(frame2, text="Solo", command=self.button_solo, takefocus=0)
		self.button_versus = ttk.Button(frame3, text="Versus", command=self.button_versus, takefocus=0)
		self.github_icon = ttk.Label(self, image=self.controller.github_icon, cursor="hand2")
		self.reskin = ttk.Label(self, image=self.controller.reskin, cursor="hand2")
		self.github_icon.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/SkohTV/KeyboardMaster"))
		self.reskin.bind("<Button-1>", lambda _: self.controller.change_skin())

		# Changement de certains paramètres de style (police & couleur)
		self.label_hello["font"] = font.Font(family="Verdana", weight="bold", size=30)
		self.button_solo["style"] = "giga.TButton"
		self.button_versus["style"] = "giga.TButton"

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.button_solo.pack(pady=15, padx=50, fill=tk.X, expand=True, ipady=15)
		self.button_versus.pack(pady=10, padx=50, fill=tk.X, expand=True, ipady=15)
		self.github_icon.place(x=5, y=360)
		self.reskin.place(x=660, y=360)

		# On pack les 4 frames
		frame1.pack()
		frame2.pack(fill=tk.X)
		frame3.pack(fill=tk.X)

		# Lorsqu'on se log, on met à jour le nom
		self.controller.bind("<<UpdateName>>", self.update_name)



	def button_solo(self) -> None:
		"""Affiche la frame de jeu solo"""
		self.controller.external_show_frame("AppSolo")



	def button_versus(self) -> None:
		"""Affiche la frame de matchmaking"""
		self.controller.external_show_frame("AppMatchmaking")



	def update_name(self, _: tk.Event) -> None:
		"""Update le nom de l'utilisateur avec qui on vient de se connecter (appelée via event & bind)\n

		Args:
			_ (tk.Event): Event tkinter (on l'ignore)
		"""
		self.label_hello.config(text=f"Bonjour {self.controller.user.name}")
