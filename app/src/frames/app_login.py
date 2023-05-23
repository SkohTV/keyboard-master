import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font

from src.connect_server import user_connection as connect



class App_Login(tk.Frame):
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
		frame1, frame2, frame3, frame4 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_status = ttk.Label(frame1, text="Bonjour, merci de vous connecter")
		self.label_username = ttk.Label(frame2, text="Username :")
		self.entry_username = ttk.Entry(frame2)
		self.label_password = ttk.Label(frame3, text="Password :")
		self.entry_password = ttk.Entry(frame3, show="*")
		self.button_login = ttk.Button(frame4, text="Log in", width=10, command=self.interface_login, takefocus=0)
		self.button_register = ttk.Button(frame4, text="Register", width=10, command=self.interface_register, takefocus=0)
  
		# Changement de certains paramètres de style (police & couleur)
		self.label_status["font"] = font.Font(family="Verdana", weight="bold", size=10)
		self.label_status.config(foreground="#89CFF0")
		self.button_login["style"] = "small.TButton"
		self.button_register["style"] = "small.TButton"

		# Placement des widgets dans la fenêtre
		self.label_status.pack(side=tk.TOP)
		self.label_username.pack(side=tk.LEFT, padx=10)
		self.entry_username.pack(side=tk.RIGHT, padx=5)
		self.label_password.pack(side=tk.LEFT, padx=10)
		self.entry_password.pack(side=tk.RIGHT, padx=5)
		self.button_login.pack(side=tk.LEFT, padx=5)
		self.button_register.pack(side=tk.RIGHT, padx=5)

		# On pack les 4 frames
		frame1.pack(pady=10, fill=tk.X)
		frame2.pack(pady=5, padx=5, fill=tk.X)
		frame3.pack(padx=5, fill=tk.X)
		frame4.pack(pady=10)


	def interface_login(self) -> None:
		"""On fait une requête au serveur de connection d'utilisateur"""
		res = connect(False, self.entry_username.get(), self.entry_password.get())
		if not res:
			self.label_status.config(text="Identifiants invalides")
		else:
			self.label_status.config(text="Connection réussie ! Redirection...")
			self.controller.user = res
			self.controller.send_event("UpdateName")
			self.controller.external_show_frame("App_Main")


	def interface_register(self) -> None:
		"""On fait une requête au serveur de création d'utilisateur"""
		res = connect(True, self.entry_username.get(), self.entry_password.get())
		if not res:
			self.label_status.config(text="Ce username est déjà utilisé")
		else:
			self.label_status.config(text="Création réussie ! Redirection...")
			self.controller.user = res
			self.controller.send_event("UpdateName")
			self.controller.external_show_frame("App_Main")
