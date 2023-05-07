import os
import tkinter as tk
from dotenv import load_dotenv



def set_alive() -> tk.Tk:
	"""Lance l'UI du jeu, et initialise l'environnement

	Returns:
		tk.Tk: Retourne la fenêtre de jeu
	"""
	load_dotenv()
	root = tk.Tk()
	root.geometry("700x400")
	root.resizable(False, False)
	root.iconbitmap("ico/keyboard.ico")
	login_screen(root)
	return root



def keep_alive(root: tk.Tk) -> None:
	"""Prend une fenêtre de jeu, la maintient en vie et l'update

	Args:
		root (tk.Tk): Objet fenêtre de jeu tkinter
	"""
	root.mainloop()



def login_screen(root: tk.Tk):
	"""Affiche l'écran de log in

	Args:
		root (tk.Tk): Objet fenêtre de jeu tkinter
	"""
	# Change le nom de la fenêtre
	root.title("Login")

	# On crée quatre packs pour formatter l'affichage
	frame1, frame2, frame3, frame4 = tk.Frame(root), tk.Frame(root), tk.Frame(root), tk.Frame(root)

	# Définition des widgets
	label_status = tk.Label(frame1, text="Bonjour, merci de vous connecter")
	label_username = tk.Label(frame2, text="Username")
	entry_username = tk.Entry(frame2)
	label_password = tk.Label(frame3, text="Password")
	entry_password = tk.Entry(frame3)
	button_login = tk.Button(frame4, text="Log in", width=10)
	button_register = tk.Button(frame4, text="Register", width=10)

	# Placement des widgets dans la fenêtre
	label_status.pack(side=tk.TOP)
	label_username.pack(side=tk.LEFT)
	entry_username.pack(side=tk.RIGHT)
	label_password.pack(side=tk.LEFT)
	entry_password.pack(side=tk.RIGHT)
	button_login.pack(side=tk.LEFT, padx=5)
	button_register.pack(side=tk.RIGHT, padx=5)

	# On pack les 4 frames
	frame1.pack(pady=5)
	frame2.pack(pady=5)
	frame3.pack()
	frame4.pack(pady=10)

	# On calcul une taille dynamique pour la fenêtre
	widget_width = label_username.winfo_reqwidth() + entry_username.winfo_reqwidth() + 40
	widget_height = label_status.winfo_reqheight() + label_username.winfo_reqheight() + label_password.winfo_reqheight() + button_login.winfo_reqheight() + 40

	# On change la taille de la fenêtre
	root.geometry('{}x{}'.format(widget_width, widget_height))
