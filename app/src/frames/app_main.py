import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from _tkinter import TclError
import webbrowser

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, query_sentence as query

from src.frames.app_solo import App_Solo



class App_Main(tk.Frame):
	def __init__(self, parent, controller):
		"""Initialisation de l'objet"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1, textvariable=self.master.master.username)
		self.button_solo = tk.Button(frame2, text="Solo")
		self.button_versus = tk.Button(frame3, text="Versus")
		self.github_icon = ttk.Label(self, image=self.master.master.github_icon, cursor="hand2")
		self.github_icon.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/SkohTV/KeyboardMaster"))

		# Changement de certains paramètres de style (police & couleur)
		self.label_hello["font"] = font.Font(family="Impact", weight="normal", size=30)
		self.button_solo.config(font=("Tahoma", 35))
		self.button_versus.config(font=("Tahoma", 35))

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.button_solo.pack(pady=20, ipadx=150, ipady=5)
		self.button_versus.pack(pady=10, ipadx=150, ipady=5)
		self.github_icon.place(x=5, y=360)

		# On pack les 4 frames
		frame1.pack()
		frame2.pack()
		frame3.pack()


	def button_solo(self):
		self.controller.show_frame(App_)


	def button_versus(self):
		self.controller.show_frame(App_Main)