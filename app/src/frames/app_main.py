import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from _tkinter import TclError
import webbrowser

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, query_sentence as query

from src.frames.app_solo import App_Solo
from src.frames.app_matchmaking import App_Matchmaking



class App_Main(tk.Frame):
	def __init__(self, parent, controller):
		"""Initialisation de l'objet"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		#self.label_hello = ttk.Label(frame1, textvariable=self.master.master.username)
		self.label_hello = ttk.Label(frame1, text=f"Bonjour null")
		self.button_solo = tk.Button(frame2, text="Solo", command=self.button_solo)
		self.button_versus = tk.Button(frame3, text="Versus", command=self.button_versus)
		self.github_icon = ttk.Label(self, image=self.master.master.github_icon, cursor="hand2")
		self.reskin = ttk.Label(self, image=self.master.master.reskin, cursor="hand2")
		self.github_icon.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/SkohTV/KeyboardMaster"))
		self.reskin.bind("<Button-1>", lambda _: self.master.master.change_skin())

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
  
		self.master.master.bind("<<UpdateName>>", self.update_name)


	def button_solo(self):
		self.controller.show_frame(App_Solo)


	def button_versus(self):
		self.master.master.start_matchmaking()
		self.controller.show_frame(App_Matchmaking)


	def update_name(self, _):
		self.label_hello.config(text=f"Bonjour {self.master.master.user.name}")