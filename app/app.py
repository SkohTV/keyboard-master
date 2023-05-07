import os
import json

from src.lifecycle import set_alive
from src.connect_server import user_connection as connect



def start():
	set_alive()

	#data = {
	#  "gamemodes": "agbqg"
	#}
	
	data = {
		"name": "Skoh",
		"rawPwd": "abcde"
	}
	
	#user = {
	#	"name": "Skoh",
	#	"hashedPwd": ""
	#}

	#res = send(type="JoinMatchmaking", user=json.dumps(user), data=json.dumps(data))
	#res = send(type="CreateUser", user=None, data=json.dumps(data))
	#res = send(type="LoginUser", user=None, data=json.dumps(data))
	user = connect(False, "Skoh", "abcde")

	#res = join_matchmaking(type="JoinMatchmaking", user=json.dumps(user), data=json.dumps(data))
	#res = send(type="CreateUser", user=None, data=json.dumps(data))
	#res = send(type="LoginUser", user=None, data=json.dumps(data))
	#res = connect(False, "Skoh", "abcde")
	print(user)