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
	 			pos,\
	 			size,\
	 			color,\
	 			message = "",\
	 			offset = (0,0),\
	 			on_click = False,\
	 			alpha = 1,\
	 			show_lable = False,\
	 			font_color = "Black",\
	 			button_type = Button_Type.PRESS):
		self.rect = pygame.Rect(pos, size)
		self.collide_rect = pygame.Rect(apply_offset(pos, offset), size)
		self.color = color
		self.message = message
		self.on_click = on_click
		self.alpha = alpha
		self.show_lable = show_lable
		self.font_color = font_color
		self.type = button_type
		self.active = False
		self.surface = get_button_surface(self)
		self.lable = get_lable(self)
		self.switch_button_styles = {
			True : (no_style,()),
			False: (no_style,())
		}

		
	def is_clicked(self, mouse_pos):
		return self.collide_rect.collidepoint(mouse_pos)

	def render(self, parent_surface):
		parent_surface.blit(self.surface, self.rect.topleft)

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
	pos = button.rect.w // 2, button.rect.h // 2
	lable = Lable(pos, button.message, LABLE_FONT_SIZE, button.font_color, gcfg.NORMAL_ALPHA)
	if button.show_lable: button.surface.blit(*lable.get_lable_blit())
	return lable

def get_button_surface(button):
		s = pygame.Surface((button.rect.w, button.rect.h))
		s.fill(button.color)
		return s

def apply_offset(pos, offset):
	w, h = pos
	off_w, off_h = offset
	return w + off_w, h + off_h
