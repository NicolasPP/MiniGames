import pygame
from GUI.components.component import Component



class Lable(Component):
	def __init__(self, pos, message, font_size, color, alpha, font = False, r_topleft = False ):
		super().__init__()
		self.pos = pos
		self._message = message
		self.font = font if font else pygame.font.Font(None, font_size)
		self.color = color
		self.r_topleft = r_topleft # default is center
		self.alpha = alpha

		self.message_render = self.font.render(self.message, True, self.color)
		self.message_rect = self.message_render.get_rect(center = self.pos)

	@property
	def message(self): return self._message

	@message.setter
	def message(self, new_message): 
		self._message = new_message
		self.message_render = self.font.render(self.message, True, self.color)
		self.message_rect = self.message_render.get_rect(center = self.pos)		

	@message.deleter
	def message(self): del self._message


	def get_lable_blit(self):
		if self.r_topleft: self.message_rect = self.message_render.get_rect(topleft = self.pos)
		self.message_render.set_alpha(self.alpha)
		return self.message_render, self.message_rect

	def get_lable_rect(self):
		message_render = self.font.render(self.message, True, self.color)
		message_render_rect = message_render.get_rect(topleft = (0, 0))
		return message_render_rect