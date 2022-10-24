import pygame, sys, time

from GUI.screen import Screen
from games.snake import Snake
from games.wordle import Wordle
from games.tictactoe import Tictactoe
from GUI.sidebar import Sidebar
from games.main_menu import Main_menu
from config.app_config import *
import config.games_config as gcfg
from enum import Enum
from typing import Type
from games.game import Game

class RES1610:
    MEDIUM = 960, 600
    LARGE = 1280, 800




class Minigames:
	def __init__(self, s_width : int, s_height : int, full_screen : bool) -> None:
		# initialize main pygame surface
		self.screen : Screen = Screen(*RES1610.MEDIUM, full_screen, color = APP_BG_COLOR)
		self.running : bool = True

		# time
		self.clock : pygame.time.Clock =  pygame.time.Clock()
		self.delta_time : float = 0
		self.prev_time : float = time.time()

		# GUI elements Rect : function
		self.sidebar : Sidebar = Sidebar(self.screen.current_width, self.screen.current_height, self)
		
		#Games
		self.games : dict[str, Game]= {
			"Menu" : Main_menu(self),
			"Snake" : Snake(self),
			"Tictactoe" : Tictactoe(self),
			"Wordle" : Wordle(self),
		}

		self.current_game : str = "Menu"


	# Main Game Functions

	def run(self) -> None:
		while self.running:
			
			self.screen.surface.fill(self.screen.bg_color)
			self.set_delta_time()
			for event in pygame.event.get(): self.parse_event(event)

			self.games[self.current_game].surface.fill(self.games[self.current_game].bg_color)

			self.update(self.delta_time)
			self.render()

			pygame.display.update()
			
	def update(self, dt : float) -> None:
		self.games[self.current_game].update(dt)

	def render(self) -> None:
		self.games[self.current_game].render()
		self.sidebar.render(self.screen.surface)
		self.screen.render()

	def set_delta_time(self) -> None:
		self.delta_time = time.time() - self.prev_time
		self.prev_time = time.time()

	def toggle_fullscreen(self) -> None:
		self.screen.toggle_full_screen()
		self.sidebar.update_surface_size()
		for name, game in self.games.items(): game.update_surface_size()
		
	# Game events Parser 
	def parse_event(self, event : pygame.event.Event) -> None:

		if self.sidebar.is_hovering(): self.sidebar.parse_event(event)
		self.games[self.current_game].parse_event(event)
	
	def quit_game(self) -> None:
		self.running = False
		pygame.quit()
		sys.exit()

	def get_game_pos(self) -> tuple[int, int]:
		return self.sidebar.rect.width + (PADDING * 2), PADDING

	def get_game_size(self) -> tuple[int, int]:
		padding = pygame.math.Vector2(PADDING, PADDING)
		game_pos = pygame.math.Vector2(self.get_game_pos())
		screen_size = pygame.math.Vector2(self.screen.get_current_size())
		size = screen_size - (game_pos + padding) 
		width, height = int(size.x), int(size.y)
		return int(width), int(height)
	








