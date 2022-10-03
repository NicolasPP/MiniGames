import pygame
from games.games_config import *

class Game:
	def __init__(self, app, bg_color = GAME_BG):
	
		self.bg_color = bg_color
		self.app = app

		self.surface = app.get_game_surface(self.bg_color)
		self.sidebar_offset = self.app.sidebar.get_sidebar_game_offset()
		
		self.paused = True

	def update(self, dt): pass
	def parse_event(self, event): pass

	def render(self): self.app.screen.surface.blit(self.surface, self.app.get_gs_position())
	def update_surface_size(self): self.surface = self.app.get_game_surface(self.bg_color)