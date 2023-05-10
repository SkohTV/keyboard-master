import tkinter as tk
from _tkinter import TclError

import ttkbootstrap as ttk

from src.connect_server import join_matchmaking as join, leave_matchmaking as leave, query_sentence as query


#user = connect(False, "Skoh", "abcde")
#print(join(user, ["easy", "insane"]))
#sleep(2)
#print(leave(user))
#res = query(gamemodes=["easy","insane"])
#print(res)




class App_Main(tk.Tk):
	def __init__(self) -> None:
		"""Initialisation de l'objet"""
		# On utilise l'init de l'objet Tkinter de base
		tk.Tk.__init__(self)

		# Change les paramètres basiques de la fenêtre
		self.resizable(False, False)
		self.title("Keyboard Master")
		self.geometry("700x400")
  
		# Le chargement de l'icône peut échouer (si l'utilisateur est sous Linux par exemple)
		# On va donc tenter de de set l'icône, et si ça échoue on passe à la suite
		try:
			self.iconbitmap("ico/keyboard.ico")
		except TclError:
			pass

	#def show_frame(self, frame) -> None:
	#	self.show_frame() # Maybe self.hide ?


class Frame_Play(tk.Frame):
	def __init_subclass__(cls) -> None:
		return super().__init_subclass__()
