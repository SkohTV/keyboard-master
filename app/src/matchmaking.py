import threading as th
from connect_server import join_matchmaking as join, leave_matchmaking as leave
from utils import User, export_gamemodes



class CustomThread(th.Thread):
	def __init__(self, user: User, gamemodes: list) -> None:
		th.Thread.__init__(self)
		self.user = user
		self.gamemodes = export_gamemodes(gamemodes)
		self.state = None
		
	def request(self) -> None:
		while not self.state:
			res = join(self.user, self.gamemodes)
			if res != 'Denied':
				self.state = int(res)