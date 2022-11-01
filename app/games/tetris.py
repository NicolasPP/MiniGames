from config.games_config import *
from games.game import Game


class Tetris(Game):
	def __init__(self, app):
		super().__init__(app)

