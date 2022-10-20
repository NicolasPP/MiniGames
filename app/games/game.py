import pygame
from config.games_config import *

'''
TODO : add mouse_position as a @property, this way the offset can be calculated here and 
	   sent to all children. rather than each children calculating it.
	   
'''

class Game:
	def __init__(self, app, bg_color = GAME_BG):
	
		self.bg_color = bg_color
		self.app = app

		self.surface = app.get_game_surface(self.bg_color)
		self.sidebar_offset = self.app.sidebar.get_sidebar_game_offset()
		
		self.paused = True
		self._user_input = pygame.key.get_pressed()

	@property
	def user_input(self): return pygame.key.get_pressed()

	@user_input.setter
	def user_input(self, new_user_input): self._user_input = new_user_input

	@user_input.deleter
	def user_input(self, ): del self._user_input

	def update(self, dt): pass
	def parse_event(self, event): pass

	def render(self): self.app.screen.surface.blit(self.surface, self.app.get_gs_position())
	def update_surface_size(self): self.surface = self.app.get_game_surface(self.bg_color)