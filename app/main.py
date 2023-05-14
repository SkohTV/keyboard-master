from src.app_login import App_Login
from src.app_main import App_Main

# Q/A
# Q: Pourquoi ne pas utiliser une variable globale pour la fenêtre tkinter ?
# A: Afin d'éviter les side effects qui pourraient modifier la fenêtre de manière innatendue




# Ne s'exéctue que si main.py est lancé, pas importé
#if __name__ == "__main__":
#  # On lance la fenêtre de login
#  app_login = App_Login()
#  app_login.mainloop()
#  # Lorsqu'elle se ferme SANS faire un sys.exit, on lance la fenêtre de jeu
#  app_main = App_Main()
#  app_main.mainloop()


# TESTS

import src.connect_server as c

#usr = c.user_connection(False, 'Skoh', 'abcde')
usr = c.user_connection(False, 'Skoh2', 'abcd')
c.join_matchmaking(usr, ['insane'])