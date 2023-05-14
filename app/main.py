from src.app import App

# Q/A
# Q: Pourquoi ne pas utiliser une variable globale pour la fenêtre tkinter ?
# A: Afin d'éviter les side effects qui pourraient modifier la fenêtre de manière innatendue


import time

# Ne s'exéctue que si main.py est lancé, pas importé
if __name__ == "__main__":
  # On lance la fenêtre de login
  #app_login = App_Login()
  #app_login.mainloop()
  ## Lorsqu'elle se ferme SANS faire un sys.exit, on lance la fenêtre de jeu
  #time.sleep(1)
  #app_main = App_Main()
  #app_main.mainloop()
  
  app = App()
  app.mainloop()


# TESTS

#import src.connect_server as c
#import threading as th
#import time
#from src.matchmaking import CustomThread


#def a():
#  print("a started")
#  usr = c.user_connection(False, 'Skoh', 'abcde')
#  myT = CustomThread(usr, ['easy', 'insane'])
#  myT.start()
#  time.sleep(2)
#  print(myT.state)
#  time.sleep(10)
#  print(myT.state)
#  res = c.set_score(usr, myT.state, 300)
#  print(res)
#  time.sleep(2)
#  res = c.set_score(usr, myT.state, 150)
#  print(res)
#  time.sleep(2)
#  res = c.retrieve_data(usr, myT.state)
#  print(res["sentence"])


#def b():
#  print("b started")
#  usr = c.user_connection(False, 'Skoh2', 'abcd')
#  myT = CustomThread(usr, ['easy'])
#  myT.start()

#th.Thread(target=a).start()
#time.sleep(2)
#th.Thread(target=b).start()



