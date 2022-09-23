import pygame

from app.GUI.screen import Screen
from games.snake import Snake
from games.wordle import Wordle
from games.tictactoe import Tictactoe
from app.GUI.sidebar import Sidebar
from app.GUI.main_menu import Main_menu
from app.app_config import *
from enum import Enum

class MiniGameApp:
	def __init__(self, s_width, s_height, full_screen):

		self.running = True
		# initialize main pygame surface
		self.screen = Screen(s_width, s_height, full_screen)
		self.screen.display()

		# GUI elements Rect : function
		self.sidebar = Sidebar(self.screen.current_width, self.screen.current_height, self)
		#Games

		self.games = {
			"Menu" : Main_menu(self),
			"Snake" : Snake(self),
			"Tictactoe" : Tictactoe(self),
			"Wordle" : Wordle(self),
		}
		self.current_game = "Menu"


	# Main Game Functions

	def run(self):
		self.update()
		self.render()

	def update(self):
		self.sidebar.update()

	def render(self):
		self.screen.surface.blit(self.games[self.current_game].surface, self.get_gs_position())
		self.sidebar.render(self.screen.surface)

	def get_game_surface(self):
		gs_x, gs_y = self.get_gs_position()
		gs_width = self.screen.current_width - (gs_x + PADDING)
		gs_height = self.screen.current_height - (gs_y + PADDING)
		game_surface = pygame.Surface((gs_width, gs_height)) 
		return game_surface

	def get_gs_position(self):
		return self.sidebar.width + (PADDING * 2), PADDING

	def toggle_fullscreen(self):
		self.screen.toggle_full_screen()
		for name, game in self.games.items(): game.update_surface_size()
		self.sidebar.update_surface_size()
	# Game events Parser 
	def parse_event(self, event):
		self.sidebar.parse_event(event)
	






