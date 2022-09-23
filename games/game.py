import pygame

class Game:
	def __init__(self, app):
		self.app = app
		self.surface = app.get_game_surface()
		self.paused = True

	def update(self): pass
	def render(self): pass
	def parse_event(self): pass
	def update_surface_size(self): self.surface = self.app.get_game_surface()
