import pygame
from enum import Enum
from config.app_config import *
import config.games_config as gcfg
from GUI.lable import Lable

class Button_Type(Enum):
	SWITCH = 1
	PRESS = 2

class Button:
	def __init__(self,\
	 			topleft,\
	 			width,\
	 			height,\
	 			color,\
	 			message = "",\
	 			on_click = False,\
	 			alpha = 1,\
	 			offset = (0,0),\
	 			show_lable = False,\
	 			font_color = "Black",\
	 			button_type = Button_Type.PRESS):
		self.show_lable = show_lable
		self.topleft = topleft
		self.width, self.height  = width, height
		self.rect = pygame.Rect((topleft[0] + offset[0], topleft[1] + offset[1]), (width, height))
		self.color = color
		self.alpha = alpha
		self.message = message
		self.on_click = on_click
		self.type = button_type
		self.active = False
		self.font_color = font_color
		self.surface = get_button_surface(self)
		self.lable = get_lable(self)
		

		self.switch_button_styles = {
			True : (no_style,()),
			False: (no_style,())
		}

		


	def render(self, parent_surface):
		parent_surface.blit(self.surface, self.topleft)

	def style(self, func, *kwargs):
		func(*kwargs)

	def set_active_style(self, func, *kwargs):
		self.switch_button_styles[True] = func, kwargs

	def set_inctive_style(self, func, *kwargs):
		self.switch_button_styles[False] = func, kwargs

	def update_style(self):
		self.surface.fill(self.color)
		func = self.switch_button_styles[self.active][0]
		kwargs = self.switch_button_styles[self.active][1]
		func(*kwargs)


	

	def click(self, *kwargs):
		if self.type == Button_Type.SWITCH:
			self.active = not self.active
			self.update_style()
		if self.on_click: self.on_click(*kwargs)


def no_style(): pass

def get_lable(button):
	pos = button.width // 2, button.height // 2
	lable = Lable(pos, button.message, LABLE_FONT_SIZE, button.font_color, gcfg.NORMAL_ALPHA)
	if button.show_lable: button.surface.blit(*lable.get_lable_blit())
	return lable

def get_button_surface(button):
		s = pygame.Surface((button.width, button.height))
		s.fill(button.color)
		return s
