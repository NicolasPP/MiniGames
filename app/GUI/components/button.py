import pygame
from enum import Enum
from config.app_config import *
import config.games_config as gcfg
from GUI.components.lable import Lable
from GUI.components.component import Component


class Button_Type(Enum):
	SWITCH = 1
	PRESS = 2

class Button(Component):
	def __init__(self,\
				parent,
	 			size,\
	 			color,\
	 			pos = (0, 0),\
	 			message = "",\
	 			on_click = False,\
	 			alpha = gcfg.NORMAL_ALPHA,\
	 			show_lable = False,\
	 			font_color = "Black",\
	 			button_type = Button_Type.PRESS):
		super().__init__(parent, pos, size, alpha, color)
		self.surface = get_button_surface(self)
		self.message = message
		self.on_click = on_click
		self.alpha = alpha
		self.show_lable = show_lable
		self.font_color = font_color
		self.type = button_type
		self.active = False
		self.lable = get_lable(self)
		self.switch_button_styles = {
			True : (no_style,()),
			False: (no_style,())
		}

	def set_active_style(self, func, *kwargs):
		self.switch_button_styles[True] = func, kwargs

	def set_inctive_style(self, func, *kwargs):
		self.switch_button_styles[False] = func, kwargs

	def update_style(self):
		self.surface.fill(self.color)
		func, kwargs = self.switch_button_styles[self.active]
		func(*kwargs)

	def render(self, set_alpha = False):
		self.parent.surface.blit(*self.get_surface_blit(set_alpha = set_alpha))

	def update_pos(self, pos_change):
		self.rect.topleft = tuple(pygame.math.Vector2(self.rect.topleft) + pos_change)
	

	def click(self, *kwargs):
		if self.type == Button_Type.SWITCH:
			self.active = not self.active
			self.update_style()
		if self.on_click: self.on_click(*kwargs)


def no_style(): pass

def get_lable(button):
	pos = button.rect.w // 2, button.rect.h // 2
	lable = Lable(button, pos, button.message, LABLE_FONT_SIZE, button.font_color, button.alpha)
	if button.show_lable: lable.render()
	return lable

def get_button_surface(button):
	s = pygame.Surface((button.rect.w, button.rect.h))
	s.fill(button.color)
	s.set_alpha(button.alpha)
	return s
