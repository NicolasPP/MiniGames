import pygame

class Game:
	def __init__(self, app):
		self.app = app
		self.surface = app.get_game_surface(False)
		self.paused_surface = app.get_game_surface(True)
		self.paused = True
		self.bg_color = "White"
		self.sidebar_offset = self.app.sidebar.get_sidebar_game_offset()

	def update(self, dt): pass
	def render(self, parent_surface):
		parent_surface.blit(self.surface, self.app.get_gs_position())
	def parse_event(self, event): pass
	def update_surface_size(self):
		new_s = self.app.get_game_surface(False)
		new_ps = self.app.get_game_surface(True)
		new_s.fill(self.bg_color)
		new_ps.fill(self.bg_color)
		self.paused_surface = new_ps
		self.surface =  new_s