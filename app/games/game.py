from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_app import Minigames

from config.games_config import *
import pygame
from dataclasses import dataclass
from GUI.containers import Relative_Container

class Game:
	def __init__(self, 
				app : Minigames, 
				bg_color : tuple[int, int, int] = GAME_BG
				) -> None:
	
		self.bg_color = bg_color
		self.app = app

		self._surface : pygame.Surface = self.get_game_surface(self.bg_color)
		self.rect : pygame.rect.Rect = self.surface.get_rect(topleft = app.get_game_pos())
				
		self.paused : bool = True
		# self.root_container = Relative_Container(self, (0,0), app.get_game_size(), alpha, color)

	@property
	def surface(self) -> pygame.Surface: return self._surface

	@surface.setter
	def surface(self, new_surface : pygame.Surface) -> None: 
		self._surface = new_surface
		self.rect = new_surface.get_rect(topleft = self.app.get_game_pos())

	@surface.deleter
	def surface(self) -> None: del self._surface


	def update(self, dt : float) -> None: pass
	def parse_event(self, event : pygame.event.Event) -> None: pass

	def render(self) -> None: 
		self.app.screen.surface.blit(self.surface, self.app.get_game_pos())
	def update_surface_size(self) -> None: self.surface = self.get_game_surface(self.bg_color)
	def render_message(self, *lable_ids : tuple[str]):
		for l_id in lable_ids:
			lable = self.lables[l_id]['lable']
			lable_surface  = self.lables[l_id]['surface']
			if lable_surface : self.surface.blit(lable_surface, (0,0))  	
			lable.render(set_alpha = True)

	def get_game_surface(self, 
						color : tuple[int, int, int], 
						alpha : int = NORMAL_ALPHA
		) -> pygame.Surface:
		game_surface = pygame.Surface(self.app.get_game_size())
		game_surface.set_alpha(alpha)
		game_surface.fill(color)
		return game_surface



