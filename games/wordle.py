from games.games_config import *
from games.game import Game
class Wordle(Game):
	def __init__(self, app):
		super().__init__(app)
		self.surface.fill(WORDLE_BG)