"""
Frame de match solo
===========

L'application est composée de 5 frames, chacune étant une page de l'application

Contenu :
---------
- AppSolo : Frame de match solo

"""



import time
import tkinter as tk
from tkinter import ttk
from tkinter import font
import webbrowser

from src.connect_server import query_sentence as query
from src.utils import threaded, WrapListener



class AppSolo(tk.Frame, WrapListener):
	"""
	Frame de match multijoueur\n

	Attributes:
		controller (src.app.App): Classe tk.Tk principale qui controle la tk.Frame\n
		written (list): Liste des caractères écrits\n
		sentence (str): Phrase à écrire\n
		start_time (float): Temps de début de la partie\n
		thread (bool): Si un thread est actif ou non\n
		current_time (float): Temps actuel\n
		label_hello (ttk.Label): Label de texte de bienvenue\n
		text_entry (tk.Text): Zone de texte pour écrire\n
		query_button (ttk.Button): Bouton de recherche de phrase\n
		label_you (ttk.Label): Label de texte "Vous"\n
		github_icon (ttk.Label): Label de l'icone GitHub\n
		back_button (ttk.Label): Label de l'icone de retour\n
		reskin (ttk.Label): Label de l'icone de reskin\n

	Methods:
		__init__: Initialise l'objet\n
		listen_keypresses: Ecoute les touches pressées\n
		update_score: Met à jour le score\n
		query_sentence: Recherche une phrase\n
		text_update: Met à jour la phrase\n
		back: Retourne à la page précédente\n
		reset: Réinitialise la page\n
	"""

	def __init__(self, parent: tk.Frame, controller) -> None:
		"""Initialisation de l'objet\n

		Args:
			parent (tk.Frame): Objet dont la classe inhérite\n
			controller (src.app.App): Classe tk.Tk principale qui controle la tk.Frame\n
		"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		WrapListener.__init__(self)
		self.controller = controller

		# On garde en mémoire quelques states
		self.written = []
		self.sentence = ""
		self.start_time = None
		self.thread = False
		self.current_time = None

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3, frame4, frame5 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1, text="Lancez une recherche pour commencer")
		self.text_entry = tk.Text(frame2, wrap=tk.WORD, width=50, height=10)
		self.query_button = ttk.Button(frame5, text="Rechercher une phrase", command=self.query_sentence, takefocus=0)
		self.label_you = ttk.Label(frame4, text="")
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
		self.text_entry["font"] = font.Font(size=12)
		self.text_entry.tag_configure("empty", foreground="white")
		self.text_entry.tag_configure("good", foreground="green")
		self.text_entry.tag_configure("wrong", foreground="red")
		self.text_entry.tag_configure("wrong-space", background="red")
		self.text_entry.insert(tk.END, "")
		self.text_entry.configure(state="disabled")
		self.query_button["style"] = "small.TButton"

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.text_entry.pack(side=tk.LEFT)
		self.label_you.pack(side=tk.LEFT, padx=20)
		self.query_button.pack()
		[i.pack(side=tk.TOP, anchor=tk.W, pady=8) for i in self.gamemodes_array]
		[i.set(False) for i in self.gamemodes_var]
		self.github_icon.place(x=5, y=360)
		self.back_button.place(x=5, y=20)
		self.reskin.place(x=660, y=360)

		# On pack les 4 frames
		frame1.pack()
		frame2.pack()
		frame4.pack(side=tk.BOTTOM, pady=30)
		frame5.pack(side=tk.BOTTOM)
		frame3.place(x=600, y=(100 - frame3.winfo_height()/2), anchor=tk.NW)



	@threaded
	def update_score(self) -> None:
		"""Tous les 0.25s, on update notre score"""
		while self.thread: # On update tant que self.thread = True
			self.current_time = time.time()
			if (not self.start_time is None) and (not self.current_time is None) and (self.written): # On affiche le texte que si le temps est calculable
				self.label_you.configure(text=f"{self.controller.user.name} : {len(self.written) / (self.current_time - self.start_time) : .3f}cps")
			time.sleep(0.25)



	def query_sentence(self) -> None:
		"""Envoy une requête pour récupérer une phrase au serveur"""
		# On crée une liste des gamemodes séléctionnés
		gamemodes = []
		for index, elem in enumerate(self.gamemodes_var):
			if elem.get():
				gamemodes.append(self.gamemodes_array[index].cget("text"))

		if not gamemodes: # Si il n'y a pas de gamemodes, on affiche un msg d'erreur
			self.text_update("Veuillez sélectionner au moins un mode de jeu")
		else: # Sinon on setup le jeu
			self.thread = False
			self.written = []
			self.sentence = ""
			self.start_time = None
			self.label_you.config(text="")
			self.label_hello.config(text="Commencez quand vous êtes prêt")
			self.text_update("Recherche d'une phrase...")
			self.sentence = query(gamemodes)
			self.text_update(self.sentence)
			self.thread = True
			self.listen_keypresses()
			self.update_score()



	def text_update(self, text: str) -> None:
		"""Update la widget text avec un nouveau texte\n

		Args:
			text (str): Nouveau texte à afficher\n
		"""
		self.text_entry.configure(state="normal")
		self.text_entry.delete("1.0", tk.END)
		self.text_entry.insert(tk.END, text)
		self.text_entry.configure(state="disabled")



	def back(self) -> None:
		"""Bouton de retour arrière"""
		self.reset()
		self.controller.external_show_frame("AppMain")



	def reset(self):
		"""Fonction de reset pour remettre la fenêtre dans un état initial"""
		self.thread = False
		self.written = []
		self.sentence = ""
		self.start_time = None
		self.label_you.config(text="")
		self.label_hello.config(text="Commencez quand vous êtes prêt")
		self.text_update("")
