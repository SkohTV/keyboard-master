import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from _tkinter import TclError
import webbrowser

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, query_sentence as query






class App_Multi(tk.Frame):
	def __init__(self, parent, controller):
		"""Initialisation de l'objet"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2 = ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1)
		self.text_entry = tk.Text(frame2)

		# Changement de certains paramètres de style (police & couleur)

		# Placement des widgets dans la fenêtre
		self.label_hello.pack()
		self.text_entry.pack()


		# On pack les 4 frames
		frame1.pack()
		frame2.pack()