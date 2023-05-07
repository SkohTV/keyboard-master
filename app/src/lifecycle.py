import os
from dotenv import load_dotenv


def set_alive() -> None:
  """Lance l'UI du jeu, et initialise l'environnement"""
  load_dotenv()