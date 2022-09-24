from games.games_config import *
from games.game import Game
class Wordle(Game):
	def __init__(self, app):
		super().__init__(app)
		self.bg_color = WORDLE_BG
		self.surface.fill(self.bg_color)
		self.paused_surface.fill(self.bg_color)