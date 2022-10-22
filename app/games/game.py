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

		self._surface = app.get_game_surface(self.bg_color)
		self.rect = self.surface.get_rect(topleft = app.get_gs_position())
				
		self.paused = True
		self._user_input = pygame.key.get_pressed()



	@property
	def user_input(self): return pygame.key.get_pressed()
	@property
	def surface(self): return self._surface

	@user_input.setter
	def user_input(self, new_user_input): self._user_input = new_user_input
	@surface.setter
	def surface(self, new_surface): 
		self._surface = new_surface
		self.rect = new_surface.get_rect(topleft = self.app.get_gs_position())


	@user_input.deleter
	def user_input(self, ): del self._user_input
	@surface.deleter
	def surface(self): del self._surface


	def update(self, dt): pass
	def parse_event(self, event): pass

	def render(self): self.app.screen.surface.blit(self.surface, self.app.get_gs_position())
	def update_surface_size(self): self.surface = self.app.get_game_surface(self.bg_color)
	def render_message(self, *lable_ids):
		for l_id in lable_ids:
			lable = self.lables[l_id]['lable']
			lable_surface  = self.lables[l_id]['surface']
			if lable_surface : self.surface.blit(lable_surface, (0,0))  	
			lable.render(set_alpha = True)