import pygame

class Game:
	def __init__(self, app):
		self.app = app
		self.surface = app.get_game_surface()
		self.paused = True
		self.bg_color = "Black"

	def update(self): pass
	def render(self): pass
	def parse_event(self): pass
	def update_surface_size(self):
		new_s = self.app.get_game_surface()
		new_s.fill(self.bg_color)
		self.surface =  new_s
