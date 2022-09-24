import pygame

class Game:
	def __init__(self, app):
		self.app = app
		self.surface = app.get_game_surface()
		self.paused_surface = app.get_game_pause_surface()
		self.current_surface = self.paused_surface
		self.paused = True
		self.bg_color = "White"

	def update(self, dt): pass
	def render(self, parent_surface): parent_surface.blit(self.current_surface, self.app.get_gs_position())
	def parse_event(self, event): pass
	def update_surface_size(self):
		new_s = self.app.get_game_surface()
		new_ps = self.app.get_game_pause_surface()
		new_s.fill(self.bg_color)
		new_ps.fill(self.bg_color)
		self.paused_surface = new_ps
		self.surface =  new_s
		self.set_current_surface()


	def set_current_surface(self):
		if self.paused: self.current_surface = self.paused_surface
		else: self.current_surface = self.surface
