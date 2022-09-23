from games.games_config import *
from games.game import Game

class Snake(Game):
	def __init__(self, app):
		super().__init__(app)
		self.bg_color = SNAKE_BG
		self.surface.fill(self.bg_color)

	def update(self):
		if self.paused: return

	def render(self):
		if self.paused: self.display_paused()

	def display_paused():
		pass

	def parse_event(self):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: self.pause = not self.paused
