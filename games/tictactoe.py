from games.games_config import *
class Tictactoe:
	def __init__(self, app):
		self.app = app
		self.surface = self.get_surface()
		

	def update(self):
		pass

	def render(self):
		pass

	def update_surface_size(self):
		self.surface = self.get_surface()

	def get_surface(self):
		s = self.app.get_game_surface()
		s.fill(TICTACTOE_BG)
		return s