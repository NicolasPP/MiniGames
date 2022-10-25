import pygame
from GUI.components.component import Component


class Lable(Component):
	def __init__(self, 
				 parent, 
				 message, 
				 font_size, 
				 color, 
				 alpha, 
				 pos = (0,0), 
				 r_topleft = False):
		super().__init__(parent, pos, (font_size, font_size), alpha, color)
		self._message = message
		self.font = pygame.font.Font(None, font_size)
		self.r_topleft = r_topleft # default is center
		self.pos = pos
		self.update_surface()

		

	@property
	def message(self): return self._message

	@message.setter
	def message(self, new_message): 
		self._message = new_message
		self.update_surface()	

	@message.deleter
	def message(self): del self._message


	def update_surface(self):
		self.surface = self.font.render(self.message, True, self.color)
		self.rect = self.surface.get_rect(center = self.pos)
