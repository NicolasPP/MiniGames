import pygame
from enum import Enum
from config.app_config import *
import config.games_config as gcfg
from GUI.components.lable import Lable
from GUI.components.component import Component
from typing import Callable, Any

def nothing() -> None: pass

class Button_Type(Enum):
	SWITCH = 1
	PRESS = 2

class Button(Component):
	def __init__(self,
				parent,
	 			size : tuple[int, int],
	 			color : tuple[int, int, int],
	 			pos : tuple[int, int] = (0, 0),
	 			message : str = "",
	 			on_click : Callable = nothing,
	 			alpha : float = gcfg.NORMAL_ALPHA,
	 			show_lable : bool = False,
	 			font_color : tuple[int, int, int] = (0,0,0),
	 			button_type : Button_Type = Button_Type.PRESS,
	 			active : bool = False):
		super().__init__(parent, pos, size, alpha, color)
		self.surface : pygame.Surface = get_button_surface(self)
		self.message = message
		self.on_click = on_click
		self.alpha = alpha
		self.show_lable = show_lable
		self.font_color = font_color
		self.type = button_type
		self.active = active
		self.lable : Lable = get_lable(self)
		self.switch_button_styles : dict[bool,tuple[Callable, Any]] = {
			True : (nothing,()),
			False: (nothing,())
		}


	def set_active_style(self, func : Callable, *kwargs : Any) -> None:
		self.switch_button_styles[True] = func, kwargs
		self.update_style()

	def set_inactive_style(self, func : Callable, *kwargs : Any) -> None:
		self.switch_button_styles[False] = func, kwargs
		self.update_style()

	def update_style(self) -> None :
		func, kwargs = self.switch_button_styles[self.active]
		func(*kwargs)

	def render(self, set_alpha = False) -> None:
		self.parent.surface.blit(*self.get_surface_blit(set_alpha = set_alpha))
	

	def click(self, *kwargs : Any) -> None:
		if self.type == Button_Type.SWITCH:
			self.active = not self.active
			self.update_style()
		self.on_click(*kwargs)



def get_lable(button : Button) -> Lable:
	pos = button.rect.w // 2, button.rect.h // 2
	lable = Lable(button, button.message, LABLE_FONT_SIZE, button.font_color, button.alpha, pos = pos)
	if button.show_lable: lable.render()
	return lable

def get_button_surface(button : Button) -> pygame.Surface:
	s = pygame.Surface((button.rect.w, button.rect.h))
	s.fill(button.color)
	s.set_alpha(int(round(button.alpha)))
	return s


#### some styles ####

def style_quit(button : Button) -> None:
	pygame.draw.line(button.surface, "Red", (5, 5), (button.rect.width - 5, button.rect.height - 5), 4)
	pygame.draw.line(button.surface, "Red", (button.rect.width - 5, 5), (5, button.rect.height - 5), 4)

def fullscreen_active_style(button : Button) -> None:
	rects = [
		#topleft
		pygame.Rect((FS_RECT_WIDTH - FS_RECT_HEIGHT, 0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((0, FS_RECT_WIDTH - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#topright
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, 0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, FS_RECT_WIDTH - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#bottomleft
		pygame.Rect((0, button.rect.height - FS_RECT_WIDTH), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((FS_RECT_WIDTH - FS_RECT_HEIGHT, button.rect.h - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		#bottomright
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, button.rect.h - FS_RECT_WIDTH), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, button.rect.h - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
	]
	button.surface.fill(button.color)
	for rect in rects: pygame.draw.rect(button.surface, "White", rect)

def fullscreen_inactive_style(button : Button) -> None:
	rects = [
		# topleft
		pygame.Rect((0,0), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((0,0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		#topright
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, 0), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((button.rect.w - FS_RECT_HEIGHT, 0), (FS_RECT_HEIGHT , FS_RECT_WIDTH)),
		#bottomleft
		pygame.Rect((0, button.rect.h-FS_RECT_WIDTH), (FS_RECT_HEIGHT,FS_RECT_WIDTH)),
		pygame.Rect((0, button.rect.h-FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#bottomright
		pygame.Rect((button.rect.w - FS_RECT_HEIGHT, button.rect.h - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, button.rect.h - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
	]
	button.surface.fill(button.color)

	for rect in rects: pygame.draw.rect(button.surface, "White", rect)

def collapsed_menu_style(button : Button):
	print('me')
	button.surface.fill('red')
def expanded_menu_style(button : Button):
	print('you')
	button.surface.fill('green')
