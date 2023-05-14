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
import threading as th
import time
from src.matchmaking import CustomThread

def a():
  print("a started")
  usr = c.user_connection(False, 'Skoh', 'abcde')
  myT = CustomThread(usr, ['easy', 'insane'])
  myT.start()
  time.sleep(2)
  print(myT.state)
  time.sleep(10)
  print(myT.state)


def b():
  print("b started")
  usr = c.user_connection(False, 'Skoh2', 'abcd')
  myT = CustomThread(usr, ['insane'])
  myT.start()

th.Thread(target=a).start()
time.sleep(2)
th.Thread(target=b).start()



