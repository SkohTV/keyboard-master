import os
import json
from time import sleep

from src.lifecycle import set_alive, keep_alive
from src.connect_server import user_connection as connect, join_matchmaking as join, leave_matchmaking as leave, query_sentence as query



def start():
	root = set_alive()

	#user = connect(False, "Skoh", "abcde")
	#print(join(user, ["easy", "insane"]))
	#sleep(2)
	#print(leave(user))
	#res = query(gamemodes=["easy","insane"])
	#print(res)
	
	keep_alive(root)
