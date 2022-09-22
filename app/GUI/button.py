import pygame
from enum import Enum

class Button_Type(Enum):
	SWITCH = 1
	PRESS = 2

class Button:
	def __init__(self,\
	 			topleft,\
	 			width,\
	 			height,\
	 			color,\
	 			lable = "",\
	 			on_click = False,\
	 			alpha = 1,\
	 			offset = (0,0),\
	 			button_type = Button_Type.PRESS):
		self.topleft = topleft
		self.width, self.height  = width, height
		self.rect = pygame.Rect((topleft[0] + offset[0], topleft[1] + offset[1]), (width, height))
		self.color = color
		self.alpha = alpha
		self.lable = lable
		self.on_click = on_click
		self.type = button_type
		self.active = False

		self.surface = self.get_button_surface()
		
	def render(self, parent_surface):
		parent_surface.blit(self.surface, self.topleft)

	def get_button_surface(self):
		s =  pygame.Surface((self.width, self.height))
		s.fill(self.color)
		return s

	def click(self, *kwargs):
		if self.type == Button_Type.PRESS:
			if self.on_click: self.on_click(*kwargs)
		else: self.active = not self.active