import sys
import tkinter as tk
import tkinter.ttk as ttk
from _tkinter import TclError

from ttkbootstrap import Style

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, query_sentence as query




class App_Main(tk.Frame):
	def __init__(self, parent, controller):
		"""Initialisation de l'objet"""
		# On crée une frame Tkinter
		tk.Frame.__init__(self, parent)
		self.controller = controller
  
  