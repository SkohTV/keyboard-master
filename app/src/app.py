"""
Application principale
===========

L'application est composée de 5 frames, chacune étant une page de l'application

Contenu :
---------
- App : Classe principale de l'application

"""



import sys
import tkinter as tk

from ttkbootstrap import Style as ttkStyle

from src.frames.app_login import AppLogin
from src.frames.app_main import AppMain
from src.frames.app_solo import AppSolo
from src.frames.app_matchmaking import AppMatchmaking
from src.frames.app_multi import AppMulti

from src.utils import User



class App(tk.Tk):
	"""
	Classe principale de l'application\n

	Attributes:
		user (User): Objet utilisateur connecté\n
		match_res (dict): Données de la partie en cours\n
		github_icon (PhotoImage): Icône de GitHub\n
		back_button (PhotoImage): Icône de retour\n
		reskin (PhotoImage): Icône de changement de skin\n
		style (ttkStyle): Style de l'application\n
		skin_cursor (int): Curseur pour la sélection du skin\n
		skins (list): Liste des skins disponibles\n

	Methods:
		__init__: Initialise l'objet\n
		show_frame: Affiche une frame\n
		external_show_frame: Affiche une frame depuis une autre frame\n
		on_close: Ferme l'application\n
		send_event: Envoie un event à une frame\n
		change_skin: Change le skin de l'application\n
	"""

	def __init__(self) -> None:
		"""Initialisation de l'objet"""
		# On utilise l'init de l'objet Tkinter de base
		tk.Tk.__init__(self)

		# On gardera l'utilisateur dans la classe, pour y accéder plus facilement (global == mauvaise pratique)
		self.user = User()
		self.match_res = None

		# Valeurs réutilisées dans des frames, nécessaires ici pour y accéder
		self.github_icon = tk.PhotoImage(file="ico/github.png")
		self.back_button = tk.PhotoImage(file="ico/back.png")
		self.reskin = tk.PhotoImage(file="ico/change_skin.png")

		# On attrape l'event de fermeture de la fenêtre, pour pouvoir clore le script
		self.protocol("WM_DELETE_WINDOW", self.on_close)

		# Change les paramètres basiques de la fenêtre
		self.resizable(False, False)

		# On gère le style via ttkbootstrap (juste un thème par défaut)
		self.style = ttkStyle()
		self.style.theme_use("darkly")
		self.skin_cursor = -1
		self.skins = ["darkly", "solar", "superhero", "cyborg", "vapor"]
		self.change_skin()

		# Le chargement de l'icône peut échouer (si l'utilisateur est sous Linux par exemple)
		# On va donc tenter de de set l'icône, et si ça échoue on passe à la suite
		try:
			self.iconbitmap("ico/keyboard.ico")
		except tk.TclError:
			pass

		# On crée un pack pour englober la frame
		container = tk.Frame(self, height=400, width=700)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# On ajoute les frames à un dictionnaire
		self.frames = {}
		for item in (AppLogin, AppMain, AppSolo, AppMatchmaking, AppMulti):
			frame = item(container, self)
			self.frames[item] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		# On affiche la frame de login
		self.show_frame(AppLogin)


	def show_frame(self, cont: tk.Frame) -> None:
		"""Affiche une frame de la fenêtre Tkinter (voir fichiers dans frames)\n

		Args:
			cont (tk.Frame): Frame à afficher\n
		"""
		# On récupère la frame dans le dictionnaire
		frame = self.frames[cont]

		# Si c'est le login, on met la fenêtre en petit
		if cont == AppLogin:
			self.title("Login")
			self.geometry("285x155")
		else: # Sinon on la met en grand
			self.title("Keyboard Master")
			self.geometry("700x400")

		# Et on l'affiche
		frame.tkraise()


	def external_show_frame(self, text_frame: str) -> None:
		"""Afficher une frame depuis une autre frame\n

		Args:
			text_frame (str): Nom en string de la fenêtre à afficher\n
		"""
		# Selon le str, on affiche une frame différente
		match text_frame:
			case "AppMain":
				self.show_frame(AppMain)
			case "AppSolo":
				self.show_frame(AppSolo)
			case "AppMatchmaking":
				self.show_frame(AppMatchmaking)
			case "AppMulti":
				self.show_frame(AppMulti)


	def on_close(self) -> None:
		"""Ferme la fenêtre ET LES THREADS quand on ferme la fenêtre"""
		self.destroy()
		sys.exit()


	def send_event(self, event: str) -> None:
		"""Envoi un event au niveau de la fenêtre (utilisée à partir d'une Frame)\n

		Args:
			event (str): Nom de l'event à envoyer\n
		"""
		self.event_generate(f"<<{event}>>")


	def change_skin(self) -> None:
		"""Passe au skin suivant dans la liste"""
		# On passe au thème suivant dans la liste
		self.skin_cursor = (self.skin_cursor + 1) % len(self.skins)
		self.style.theme_use(self.skins[self.skin_cursor])

		# Et on update le style des boutons pour correspondre
		self.style.configure("small.TButton", foreground=self.style.colors.fg, background=self.style.colors.dark)
		self.style.configure("big.TButton", font="Verdana 15 bold", foreground=self.style.colors.fg, background=self.style.colors.dark)
		self.style.configure("giga.TButton", font="Tahoma 35 bold", foreground=self.style.colors.fg, background=self.style.colors.dark)
