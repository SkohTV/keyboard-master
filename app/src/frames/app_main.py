import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import webbrowser

from src.frames.app_solo import App_Solo
from src.frames.app_matchmaking import App_Matchmaking



class App_Main(tk.Frame):
	def __init__(self, parent: tk.Frame, controller) -> None:
		"""Initialisation de l'objet

		Args:
			parent (tk.Frame): Objet dont la classe inhérite
			controller (src.app.App): Classe tk.Tk principale qui controle la tk.Frame
		"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		#self.label_hello = ttk.Label(frame1, textvariable=self.controller.username)
		self.label_hello = ttk.Label(frame1, text=f"Bonjour null")
		self.button_solo = tk.Button(frame2, text="Solo", command=self.button_solo)
		self.button_versus = tk.Button(frame3, text="Versus", command=self.button_versus)
		self.github_icon = ttk.Label(self, image=self.controller.github_icon, cursor="hand2")
		self.reskin = ttk.Label(self, image=self.controller.reskin, cursor="hand2")
		self.github_icon.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/SkohTV/KeyboardMaster"))
		self.reskin.bind("<Button-1>", lambda _: self.controller.change_skin())

		# Changement de certains paramètres de style (police & couleur)
		self.label_hello["font"] = font.Font(family="Verdana", weight="bold", size=30)
		self.button_solo.config(font=("Tahoma", 35))
		self.button_versus.config(font=("Tahoma", 35))

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.button_solo.pack(pady=20, ipadx=150, ipady=5)
		self.button_versus.pack(pady=10, ipadx=150, ipady=5)
		self.github_icon.place(x=5, y=360)
		self.reskin.place(x=660, y=360)

		# On pack les 4 frames
		frame1.pack()
		frame2.pack()
		frame3.pack()

		# Lorsqu'on se log, on met à jour le nom
		self.controller.bind("<<UpdateName>>", self.update_name)


	def button_solo(self):
		self.controller.external_show_frame("App_Solo")
		print(self.controller == self.controller, self.controller is self.controller)


	def button_versus(self):
		self.controller.external_show_frame("App_Matchmaking")


	def update_name(self, _):
		self.label_hello.config(text=f"Bonjour {self.controller.user.name}")