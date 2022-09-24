import pygame, sys, time

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
		pygame.init()
		self.delta_time = 0
		self.prev_time = time.time()
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
		while self.running:
			pygame.display.update()
			self.set_delta_time()
			for event in pygame.event.get(): self.parse_event(event)
			self.update(self.delta_time)
			self.render()
			pygame.display.update()
			
	def update(self, dt): self.games[self.current_game].update(dt)

	def render(self):
		self.games[self.current_game].render(self.screen.surface)
		self.sidebar.render(self.screen.surface)


	def get_game_surface(self, is_paused_surface):
		gs_width, gs_height = self.get_gs_dimension()
		if is_paused_surface: return pygame.Surface((gs_width, gs_height), pygame.SRCALPHA)
		return pygame.Surface((gs_width, gs_height))
	
	def get_gs_dimension(self):
		gs_x, gs_y = self.get_gs_position()
		gs_width = self.screen.current_width - (gs_x + PADDING)
		gs_height = self.screen.current_height - (gs_y + PADDING)
		return gs_width, gs_height

	def get_gs_position(self):
		return self.sidebar.width + (PADDING * 2), PADDING

	def set_delta_time(self):
		self.delta_time = time.time() - self.prev_time
		self.prev_time = time.time()

	def toggle_fullscreen(self):
		self.screen.toggle_full_screen()
		self.sidebar.update_surface_size()
		for name, game in self.games.items(): game.update_surface_size()
		
	# Game events Parser 
	def parse_event(self, event):
		self.sidebar.parse_event(event)
		self.games[self.current_game].parse_event(event)
	
	def quit_game(self):
		self.running = False
		pygame.quit()
		sys.exit()





