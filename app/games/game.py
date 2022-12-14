from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_app import Minigames

from config.games_config import *
import pygame
from dataclasses import dataclass
from GUI.components.containers import Linear_Container, Scrollable_Container, Relative_Container
from GUI.components.button import Button
from GUI.components.lable import Lable
from GUI.components.component import Component
from typing import Any


class Game:
	def __init__(self, 
				app : Minigames, 
				color : tuple[int, int, int] = GAME_BG
				) -> None:
		self.color = color
		self.app = app

		self._surface : pygame.Surface = self.get_game_surface(self.color)
		self.rect : pygame.rect.Rect = self.surface.get_rect(topleft = (0, 0))
				
		self.paused : bool = True

	@property
	def surface(self) -> pygame.Surface: return self._surface

	@surface.setter
	def surface(self, new_surface : pygame.Surface) -> None: 
		self._surface = new_surface
		self.rect = new_surface.get_rect(topleft = (0,0))

	@surface.deleter
	def surface(self) -> None: del self._surface


	def update(self, dt : float) -> None: pass
	def parse_event(self, event : pygame.event.Event) -> None: pass

	def render(self) -> None: 
		self.app.surface.blit(self.surface, (0,0))
	def update_surface_size(self) -> None: self.surface = self.get_game_surface(self.color)

	def get_game_surface(self, 
						color : tuple[int, int, int], 
						alpha : float = NORMAL_ALPHA
		) -> pygame.Surface:
		game_surface = pygame.Surface(self.app.screen.get_current_size())
		game_surface.set_alpha(int(round(alpha)))
		game_surface.fill(color)
		return game_surface




class Game_GUI:
	def __init__(self, game : Any):
		self.game = game
		self.containers : dict[str, Linear_Container | Scrollable_Container | Relative_Container] = {}
		self.lables : dict[str, Lable] = {}
		self.buttons : dict[str, Button] = {}
		self._surface : pygame.Surface =  game.surface

	@property
	def surface(self) -> pygame.Surface: return self.game.surface
	@surface.setter
	def surface(self, new_surface : pygame.Surface) -> None: self._surface = new_surface
	@surface.deleter
	def surface(self) -> None: del self._surface

	def populate_GUI(self) ->None: assert "not implemented"

	def add_component(self, component : Component): pass




