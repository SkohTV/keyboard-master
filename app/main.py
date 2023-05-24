"""
Module principal
===============

Ce module sert de point d'entrée pour exécuter l'application tkinter

Utilisation :
-------------
	Pour exécuter l'application, exécutez ce fichier directement à l'aide de l'interpréteur Python

	$ py main.py

"""



from src.app import App



# Ne s'exéctue que si main.py est lancé, pas importé
if __name__ == "__main__":
	app = App()
	app.mainloop()
