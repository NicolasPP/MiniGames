import pygame
from app.GUI.button import Button
from app.app_config import *

class Sidebar:
	def __init__(self, topleft, width, height, screen_cover_ratio = .2, alpha = 1, bg_color = BG_COLOR):
		self.topleft = topleft
		self.width, self.height  = width, height
		self.rect = pygame.Rect(topleft, (width, height))
		self.screen_cover_ratio = screen_cover_ratio
		self.alpha = alpha
		self.bg_color = bg_color
		self.surface = self.get_sidebar_surface()
		self.components = self.add_sidebar_content()

	def render(self, parent_surface, in_game):
		if in_game: return
		for comp in self.components: comp.render(self.surface)
		parent_surface.blit(self.surface, self.topleft)


	def update(self, in_game):
		if in_game: return

	def parse_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN: self.check_comp_collision()

	def check_comp_collision(self):
		for comp in self.components:
			if comp.rect.collidepoint(pygame.mouse.get_pos()): comp.click()

	def get_sidebar_surface(self):
		s = pygame.Surface((self.width * self.screen_cover_ratio, self.height))
		s.fill(self.bg_color)
		return s
	
	def add_sidebar_content(self):
		snake = Button((30 , 30), 50, 20, "orange", on_click = create_snake, offset = self.topleft)
		tictactoe = Button((30, 100), 50, 20, "red", on_click = create_tictactoe, offset = self.topleft)
		wordle = Button((30, 170), 50, 20, "Yellow", on_click = create_wordle, offset = self.topleft)
		return [snake, tictactoe, wordle]


# GUI Logic
def create_snake():
	print( "snake" )

def create_tictactoe():
	print("tictactoe")

def create_wordle():
	print("wordle")

