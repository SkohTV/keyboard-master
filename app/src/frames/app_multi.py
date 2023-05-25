"""
Frame de match multijoueur
===========

L'application est composée de 5 frames, chacune étant une page de l'application

Contenu :
---------
- AppMulti : Frame de match multijoueur

"""



import time
import tkinter as tk
from tkinter import ttk
from tkinter import font
import webbrowser

from src.connect_server import retrieve_data as retrieve, set_score as score
from src.utils import threaded, WrapListener




class AppMulti(tk.Frame, WrapListener):
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
		label_you (ttk.Label): Label de texte "Vous"\n
		label_advers (ttk.Label): Label de texte "Adversaire"\n
		github_icon (ttk.Label): Label de l'icone GitHub\n
		back_button (ttk.Label): Label de l'icone de retour\n
		reskin (ttk.Label): Label de l'icone de reskin\n

	Methods:
		__init__: Initialise l'objet\n
		send_ms: Envoie les données au serveur\n
		receive_ms: Reçoit les données du serveur\n
		text_update: Met à jour la phrase\n
		back: Retourne à la page précédente\n
		reset: Réinitialise la page\n
		on_arrive: Quand on arrive sur la page\n
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
		frame1, frame2, frame3 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1, text="Commencez quand vous êtes prêt")
		self.text_entry = tk.Text(frame2, wrap=tk.WORD, width=50, height=10)
		self.label_you = ttk.Label(frame3, text="aaa")
		self.label_advers = ttk.Label(frame3, text="aaa")
		self.github_icon = ttk.Label(self, image=self.controller.github_icon, cursor="hand2")
		self.back_button = ttk.Label(self, image=self.controller.back_button, cursor="hand2")
		self.reskin = ttk.Label(self, image=self.controller.reskin, cursor="hand2")
		self.github_icon.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/SkohTV/KeyboardMaster"))
		self.back_button.bind("<Button-1>", lambda _: self.back())
		self.reskin.bind("<Button-1>", lambda _: self.controller.change_skin())

		# Changement de certains paramètres de style (police & couleur)
		self.label_hello["font"] = font.Font(family="Verdana", weight="bold", size=20)
		self.text_entry["font"] = font.Font(size=12)
		self.text_entry.tag_configure("empty", foreground="white")
		self.text_entry.tag_configure("good", foreground="green")
		self.text_entry.tag_configure("wrong", foreground="red")
		self.text_entry.tag_configure("wrong-space", background="red")
		self.text_entry.insert(tk.END, "")
		self.text_entry.configure(state="disabled")

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.text_entry.pack(side=tk.LEFT)
		self.label_you.pack(side=tk.LEFT, padx=20)
		self.label_advers.pack(side=tk.LEFT, padx=20)
		self.github_icon.place(x=5, y=360)
		self.back_button.place(x=5, y=20)
		self.reskin.place(x=660, y=360)

		# On pack les 4 frames
		frame1.pack()
		frame2.pack()
		frame3.pack(side=tk.BOTTOM, pady=30)

		# Lorsqu'un match est trouvé, on charge cette fenêtre
		self.controller.bind("<<StartMulti>>", self.on_arrive)



	@threaded
	def send_ms(self) -> None:
		"""Tous les 0.25s, on update notre score"""
		while self.thread: # On update tant que self.thread = True
			self.current_time = time.time()
			if (not self.start_time is None) and (not self.current_time is None) and (self.written): # On affiche ET envoi notre score SI le temps est calculable
				self.label_you.configure(text=f"{self.controller.user.name} : {len(self.written) / (self.current_time - self.start_time) : .3f}cps") # Affichage du score
				val = 0 if not self.start_time else round(len(self.written) / (time.time() - self.start_time), 3) * 1000 # Valeur à envoyer
				score(self.controller.user, self.controller.match_res["gameID"], val) # On envoi notre score ici
			time.sleep(0.25)
		if (not self.start_time is None) and (not self.current_time is None) and (self.written):
			score(self.controller.user, self.controller.match_res["gameID"], val) # On envoi notre score ici
			self.label_hello.config(text=f"Votre score est de : {len(self.written) / (self.current_time - self.start_time) : .3f}cps")



	@threaded
	def receive_ms(self) -> None:
		"""Toutes les 0.25s, on envoit au serveur une demande d'obtention des données de la game"""
		while self.thread: # On demande tant que self.thread = True
			res = retrieve(self.controller.user, self.controller.match_res["gameID"])
			if "player" in res: # player ne sera pas là si le second joueur ne s'est pas encore add
				self.label_advers.config(text=f"{res['player']} : {int(res['playerms']) / 1000 : .3f}cps")
			time.sleep(0.25)



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



	def on_arrive(self, _: tk.Event) -> None:
		"""On charge la fenêtre lorsqu'un match est accepté\n

		Args:
			_ (tk.Event): Event tkinter (on l'ignore)\n
		"""
		self.thread = True
		self.sentence = self.controller.match_res["sentence"]
		self.text_update(self.sentence)
		self.label_you.config(text=f"{self.controller.user.name} : {0 : .3f}cps")
		self.label_advers.config(text="...")
		self.listen_keypresses() # On commence à écouter les touches
		self.send_ms() # On commence l'envoi de données
		self.receive_ms() # On commence la réception de données
