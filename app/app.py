import os
import json

from src.lifecycle import set_alive
from src.database import send, receive



def start():
  set_alive()

  #data = {
  #  "gamemodes": "agbqg"
  #}
  
  data = {
    "name": "Skoh",
    "rawPwd": "abcde"
  }
  
  user = {
    "name": "Skoh",
    "hashedPwd": ""
  }

  #res = send(type="JoinMatchmaking", user=json.dumps(user), data=json.dumps(data))
  res = send(type="CreateUser", user=None, data=json.dumps(data))
  print(res)