import pygame
from app.GUI.button import Button, Button_Type
from app.GUI.screen import Screen
from games.snake import Snake
from games.wordle import Wordle
from games.tictactoe import Tictactoe
from app.GUI.sidebar import Sidebar
from app.app_config import *
from enum import Enum

class MiniGameApp:
	def __init__(self, s_width, s_height, full_screen):

		# Selected Game -- if false player hasnt choosen the game yet
		self.current_game = False

		# initialize main pygame surface
		self.screen = Screen(s_width, s_height, full_screen)
		self.screen.display()

		# GUI elements Rect : function
		self.sidebar = Sidebar(s_width, s_height, self)
		#Games

		self.games = {
			"Snake" : Snake(self.get_game_surface()),
			"Tictactoe" : Tictactoe(self.get_game_surface()),
			"Wordle" : Wordle(self.get_game_surface()),
		}

		self.current_game_surface = self.get_game_surface()


	# Main Game Functions

	def run(self):
		self.update()
		self.render()

	def update(self):
		self.sidebar.update()

	def render(self):
		self.screen.surface.blit(self.current_game_surface, self.get_gs_position())
		self.sidebar.render(self.screen.surface)

	def get_game_surface(self):
		gs_x, gs_y = self.get_gs_position()
		gs_width = self.screen.current_width - (gs_x + PADDING)
		gs_height = self.screen.current_height - (gs_y + PADDING)
		game_surface = pygame.Surface((gs_width, gs_height)) 
		game_surface.fill(NO_GAME_COLOR)
		return game_surface

	def get_gs_position(self):
		return self.sidebar.width + (PADDING * 2), PADDING

		
	# Game events Parser 
	def parse_event(self, event):
		self.sidebar.parse_event(event)
	






