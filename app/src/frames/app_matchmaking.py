import sys, time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from _tkinter import TclError
import webbrowser
from pynput import keyboard
import threading

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, retrieve_data as retrieve
from src.utils import threaded




class App_Matchmaking(tk.Frame):
	def __init__(self, parent, controller):
		"""Initialisation de l'objet"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller

		self.thread = False

		# On crée quatre packs pour formatter l'affichage
		frame1, frame2, frame3 = ttk.Frame(self), ttk.Frame(self), ttk.Frame(self)

		# Définition des widgets
		self.label_hello = ttk.Label(frame1, text="Lancez une recherche pour commencer")
		self.query_button = ttk.Button(frame2, text="Rejoindre le matchmaking", command=self.join_or_leave)
		self.github_icon = ttk.Label(self, image=self.master.master.github_icon, cursor="hand2")
		self.back_button = ttk.Label(self, image=self.master.master.back_button, cursor="hand2")
		self.reskin = ttk.Label(self, image=self.master.master.reskin, cursor="hand2")
		self.github_icon.bind("<Button-1>", lambda _: webbrowser.open_new("https://github.com/SkohTV/KeyboardMaster"))
		self.back_button.bind("<Button-1>", lambda _: self.back())
		self.reskin.bind("<Button-1>", lambda _: self.master.master.change_skin())
		self.gamemodes_var = []
		self.gamemodes_array = []

		# On peuple self.gamemodes_var et self.gamemodes_array avec les modes de jeu
		for index, elem in enumerate(("easy", "insane")):
			self.gamemodes_var.append(tk.BooleanVar())
			self.gamemodes_array.append(ttk.Checkbutton(frame3, text=elem, variable=self.gamemodes_var[index], onvalue=True, offvalue=False))

		# Changement de certains paramètres de style (police & couleur)
		self.label_hello["font"] = font.Font(family="Verdana", weight="bold", size=20)

		# Placement des widgets dans la fenêtre
		self.label_hello.pack(pady=20)
		self.query_button.pack()
		[i.pack(side=tk.TOP, anchor=tk.W, pady=8) for i in self.gamemodes_array]
		[i.set(False) for i in self.gamemodes_var]
		self.github_icon.place(x=5, y=360)
		self.back_button.place(x=5, y=20)
		self.reskin.place(x=660, y=360)

		# On pack les 4 frames
		frame1.pack()
		frame2.pack()
		frame3.place(x=600, y=(100 - frame3.winfo_height()/2), anchor=tk.NW)


	@threaded
	def join_matchmaking(self):
		gamemodes = []
		for index, elem in enumerate(self.gamemodes_var):
			if elem.get():
				gamemodes.append(self.gamemodes_array[index].cget("text"))
		res = "Denied"
		while res == "Denied" and self.thread:
			res = join(self.master.master.user, gamemodes)

		if not res == "Denied":
			self.label_hello["text"] = "En attente d'un adversaire"
			self.master.master.match_res = retrieve(self.master.master.user, res)
			self.master.master.external_show_frame("App_Multi")
			self.master.master.send_event("StartMulti")


	def join_or_leave(self):
		if self.thread:
			self.thread = False
			self.query_button["text"] = "Rejoindre le matchmaking"
			leave(self.master.master.user)
		else:
			self.thread = True
			self.query_button["text"] = "Quitter le matchmaking"
			self.join_matchmaking()


	def back(self):
		self.reset()
		self.master.master.external_show_frame("App_Main")


	def reset(self):
		leave(self.master.master.user)
		self.label_hello["text"] = "Lancez une recherche pour commencer"
		self.query_button["text"] = "Rejoindre le matchmaking"
		[i.set(False) for i in self.gamemodes_var]
