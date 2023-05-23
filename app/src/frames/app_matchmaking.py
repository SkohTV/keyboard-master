import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import webbrowser

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, retrieve_data as retrieve
from src.utils import threaded



class App_Matchmaking(tk.Frame):
	def __init__(self, parent: tk.Frame, controller) -> None:
		"""Initialisation de l'objet\n

		Args:
			parent (tk.Frame): Objet dont la classe inhérite\n
			controller (src.app.App): Classe tk.Tk principale qui controle la tk.Frame\n
		"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# On garde en mémoire si un thread est actif ou non
		self.thread = False

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1, text="Lancez une recherche pour commencer")
		self.query_button = ttk.Button(frame2, text="Rejoindre le matchmaking", command=self.join_or_leave, takefocus=0)
		self.github_icon = ttk.Label(self, image=self.controller.github_icon, cursor="hand2")
		self.back_button = ttk.Label(self, image=self.controller.back_button, cursor="hand2")
		self.reskin = ttk.Label(self, image=self.controller.reskin, cursor="hand2")
		self.github_icon.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/SkohTV/KeyboardMaster"))
		self.back_button.bind("<Button-1>", lambda _: self.back())
		self.reskin.bind("<Button-1>", lambda _: self.controller.change_skin())
		self.gamemodes_var = []
		self.gamemodes_array = []

		# On peuple self.gamemodes_var et self.gamemodes_array avec les modes de jeu
		for index, elem in enumerate(("easy", "insane")):
			self.gamemodes_var.append(tk.BooleanVar())
			self.gamemodes_array.append(ttk.Checkbutton(frame3, text=elem, variable=self.gamemodes_var[index], onvalue=True, offvalue=False))

		# Changement de certains paramètres de style (police & couleur)
		self.label_hello["font"] = font.Font(family="Verdana", weight="bold", size=20)
		self.query_button["style"] = "big.TButton"

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.query_button.pack(pady=90, ipadx=50, ipady=10)
		[i.pack(side=tk.TOP, anchor=tk.W, pady=8) for i in self.gamemodes_array]
		[i.set(False) for i in self.gamemodes_var]
		self.github_icon.place(x=5, y=360)
		self.back_button.place(x=5, y=20)
		self.reskin.place(x=660, y=360)

		# On pack les 4 frames
		frame1.pack()
		frame2.pack()
		frame3.place(x=600, y=(100 - frame3.winfo_height()/2), anchor=tk.NW)


	@threaded
	def join_matchmaking(self) -> None:
		"""On rejoint le matchmaking, utilisée dans un thread pour plus de contrôle"""
		# On crée une liste de gamemodes avec ceux sélectionnés
		gamemodes = []
		for index, elem in enumerate(self.gamemodes_var):
			if elem.get():
				gamemodes.append(self.gamemodes_array[index].cget("text"))

		# Tant que les demandes sont refusées, on fait une demande de rejoindre le matchmaking
		res = "Denied"
		while res == "Denied" and self.thread:
			res = join(self.controller.user, gamemodes)

		# Si la demande est acceptée, on passe en mode multijoueur
		if not res == "Denied":
			self.label_hello["text"] = "En attente d'un adversaire"
			self.controller.match_res = retrieve(self.controller.user, res) # Récupération des données de la game
			self.reset()
			self.controller.external_show_frame("App_Multi") # Affichage de la frame multijoueur
			self.controller.send_event("StartMulti")


	def join_or_leave(self) -> None:
		"""Gère le bouton de join/leave matchmaking"""
		if self.thread: # Si bouton cliqué, et thread actif
			self.thread = False # On quite le matchmaking
			self.query_button["text"] = "Rejoindre le matchmaking"
			leave(self.controller.user)
		else: # Sinon
			self.thread = True # On le rejoint
			self.query_button["text"] = "Quitter le matchmaking"
			self.join_matchmaking()


	def back(self) -> None:
		"""Bouton de retour arrière"""
		self.reset()
		self.controller.external_show_frame("App_Main")


	def reset(self) -> None:
		"""Fonction de reset pour remettre la fenêtre dans un état initial"""
		leave(self.controller.user)
		self.label_hello["text"] = "Lancez une recherche pour commencer"
		self.query_button["text"] = "Rejoindre le matchmaking"
		[i.set(False) for i in self.gamemodes_var]
