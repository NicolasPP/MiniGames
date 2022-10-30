import pygame
from config.games_config import *
from GUI.components.component import Component


class Lable(Component):
	def __init__(self, 
				 parent, 
				 message : str, 
				 font_size : int, 
				 color : tuple[int, int, int], 
				 alpha : int, 
				 pos : tuple[int, int] = (0,0), 
				 r_topleft = False):
		super().__init__(parent, pos, (font_size, font_size), alpha, color)
		self._message = message
		self.font = pygame.font.Font(None, font_size)
		self.r_topleft = r_topleft # default is center
		self.pos = pos
		self.blink_alpha = alpha
		self.blink_speed  : int = ALPHA_CHANGE
		self.blink_change  : int = -1

		self.center()

	@property
	def message(self) -> str: return self._message

	@message.setter
	def message(self, new_message : str) -> None: 
		self._message = new_message
		self.update_message()	

	@message.deleter
	def message(self) -> None: del self._message

	def blink(self, dt : float) -> None:
		self.alpha +=  (self.blink_speed * dt * self.blink_change)

		if self.alpha <= 0:
			self.alpha = 0
			self.blink_change = 1

		if self.alpha >= 255:
			self.alpha = 255
			self.blink_change = -1

	def center(self) -> None:
		self.surface = self.font.render(self.message, True, self.color)
		self.rect = self.surface.get_rect(center = self.rect.topleft)

	def update_message(self) -> None:
		self.surface = self.font.render(self.message, True, self.color)
		self.rect = self.surface.get_rect(center = self.rect.center)
