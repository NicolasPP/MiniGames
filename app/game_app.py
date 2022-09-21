import pygame

from app.screen import Screen
from games.snake import Snake
from games.wordle import Wordle
from games.tictactoe import Tictactoe

class MiniGameApp:
	def __init__(self, s_width, s_height, full_screen):

		# Selected Game -- if false player hasnt choosen the game yet
		self.current_game = False

		# initialize main pygame surface
		self.screen = Screen(s_width, s_height, full_screen)
		self.screen.display()

		# GUI elements Rect : function
		self.buttons = []
		self.gui_add_button((30, 30), 50, 20, "white", Snake.create_game)
		self.gui_add_button((100, 30), 50, 20, "red", Snake.create_game)
		self.in_game = False 

	# Main Game Functions

	def run(self):
		self.update()
		self.render()

	def update(self):
		if self.in_game: pass

	def render(self):
		if self.in_game: pass
		else: self.gui_render()
    

	# Game events Parser 

	def parse_event(self, event):
		if self.in_game:
			pass
		else:
			if event.type == pygame.MOUSEBUTTONDOWN: self.gui_update()
		

	# GUI
	def gui_render(self):
		for b in self.buttons:
			pygame.draw.rect(self.screen.surface, "White", b)

	def gui_update(self):
		for b in self.buttons:
			if b.collidepoint(pygame.mouse.get_pos()):
				print('youve clicked me')

	def gui_add_button(self, topleft, width, height, color, on_click):
		rect = pygame.Rect(topleft, (width, height))
		self.buttons.append(rect)

