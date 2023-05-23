import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import webbrowser
from pynput import keyboard
import threading

from src.connect_server import query_sentence as query
from src.utils import threaded



class App_Solo(tk.Frame):
	def __init__(self, parent: tk.Frame, controller) -> None:
		"""Initialisation de l'objet\n

		Args:
			parent (tk.Frame): Objet dont la classe inhérite\n
			controller (src.app.App): Classe tk.Tk principale qui controle la tk.Frame\n
		"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
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
	def listen_keypresses(self) -> None:
		"""Ecoute et réagit aux touches pressées pour le jeu"""

		def on_press(key: keyboard.Key) -> None:
			"""Fonction appelée par le listener lorsqu'une touche est pressée

			Args:
				key (keyboard.Key): Touche pressée
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
			elif len(self.written) < len(self.sentence):
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
					self.label_hello.config(text=f"Votre score est de : {len(self.written) / (self.current_time - self.start_time) : .3f}cps")
					self.thread = False

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
		self.controller.external_show_frame("App_Main")


	def reset(self):
		"""Fonction de reset pour remettre la fenêtre dans un état initial"""
		self.thread = False
		self.written = []
		self.sentence = ""
		self.start_time = None
		self.label_you.config(text="")
		self.label_hello.config(text="Commencez quand vous êtes prêt")
		self.text_update("")
