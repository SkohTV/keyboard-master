from app import App_Login

# Q/A
# Q: Pourquoi ne pas utiliser une variable globale pour la fenêtre tkinter ?
# A: Afin d'éviter les side effects qui pourraient modifier la fenêtre de manière innatendue




if __name__ == "__main__":
  app = App_Login()
  app.mainloop()