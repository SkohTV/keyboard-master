import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from _tkinter import TclError
import webbrowser
import keyboard

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, query_sentence as query
from src.utils import threaded

# https://www.tutorialspoint.com/how-to-change-the-color-of-certain-words-in-a-tkinter-text-widget



class App_Matchmaking(tk.Frame):
	def __init__(self, parent, controller):
		"""Initialisation de l'objet"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1, text="Vous affrontez null")
		self.text_entry = ttk.Label(frame2, text="Phrase en cours de chargement...", wrap=600)
		self.label_you = ttk.Label(frame3, text="")
		self.label_advers = ttk.Label(frame3)

		# Changement de certains paramètres de style (police & couleur)
		self.label_hello["font"] = font.Font(family="Verdana", weight="bold", size=20)
		self.text_entry["font"] = font.Font(size=12)

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.text_entry.pack(pady=20, padx=20)

		# On pack les 4 frames
		frame1.pack()
		frame2.pack()

		self.master.master.bind("<<UpdateMulti>>", self.update_multi)


	@threaded
	def listen_keypresses(self):
		pass


	def update_multi(self, _):
		self.label_hello.config(text=f"Vous affrontez {None}")
		self.text_entry.config(text=None)


	def soft_update_multi(self, _):
		self.label_you.config()
		self.label_advers.config()