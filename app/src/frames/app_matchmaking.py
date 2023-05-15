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
		frame1, frame2 = ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1, textvariable=self.master.master.versusname)
		self.text_entry = ttk.Label(frame2, textvariable=self.master.master.sentence, wrap=600)

		# Changement de certains paramètres de style (police & couleur)
		self.label_hello["font"] = font.Font(family="Verdana", weight="bold", size=20)
		self.text_entry["font"] = font.Font(size=12)

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.text_entry.pack(pady=20, padx=20)


		# On pack les 4 frames
		frame1.pack()
		frame2.pack()


		@threaded
		def listen_keypresses(self):
			pass