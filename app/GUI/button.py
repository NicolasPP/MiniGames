import pygame
from enum import Enum
from app.app_config import *

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
	 			show_lable = False,\
	 			button_type = Button_Type.PRESS):
		self.show_lable = show_lable
		self.topleft = topleft
		self.width, self.height  = width, height
		self.rect = pygame.Rect((topleft[0] + offset[0], topleft[1] + offset[1]), (width, height))
		self.color = color
		self.alpha = alpha
		self.lable = lable
		self.on_click = on_click
		self.type = button_type
		self.active = False
		self.font = pygame.font.Font(None, LABLE_FONT_SIZE)

		self.surface = self.get_button_surface()
		
	def render(self, parent_surface):
		parent_surface.blit(self.surface, self.topleft)

	def render_lable(self, surface):
		lable_render = self.font.render(self.lable, True, "Black")
		lable_rect = lable_render.get_rect(topleft = (0, 0))
		width_diff = self.width - lable_rect.width
		height_diff = self.height - lable_rect.height
		lable_rect = lable_render.get_rect(topleft = (width_diff // 2, height_diff // 2))
		surface.blit(lable_render, lable_rect)

	def get_button_surface(self):
		s =  pygame.Surface((self.width, self.height))
		s.fill(self.color)
		if self.show_lable: self.render_lable(s)
		return s

	def click(self, *kwargs):
		if self.type == Button_Type.PRESS:
			if self.on_click: self.on_click(*kwargs)
		else: self.active = not self.active