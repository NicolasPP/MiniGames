import pygame

from app.GUI.screen import Screen
from games.snake import Snake
from games.wordle import Wordle
from games.tictactoe import Tictactoe
from app.GUI.sidebar import Sidebar

class MiniGameApp:
	def __init__(self, s_width, s_height, full_screen):

		# Selected Game -- if false player hasnt choosen the game yet
		self.current_game = False

		# initialize main pygame surface
		self.screen = Screen(s_width, s_height, full_screen)
		self.screen.display()

		# GUI elements Rect : function
		self.sidebar = Sidebar(s_width, s_height)
		self.in_game = False 

	# Main Game Functions

	def run(self):
		self.update()
		self.render()

	def update(self):
		if self.in_game: pass
		self.sidebar.update(self.in_game)

	def render(self):
		if self.in_game: pass
		self.sidebar.render(self.screen.surface, self.in_game)
    

	# Game events Parser 

	def parse_event(self, event):
		self.sidebar.parse_event(event)
		if self.in_game: pass

