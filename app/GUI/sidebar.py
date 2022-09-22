import pygame
from app.app_config import *
from games.games_config import *
from app.GUI.button import Button, Button_Type
class Sidebar:
	def __init__(self, width, height, parent, screen_cover_ratio = .1, alpha = 1, bg_color = BG_COLOR):
		self.width = (width * screen_cover_ratio) - PADDING
		self.height = height - (PADDING * 2)
		self.rect = pygame.Rect((PADDING,PADDING), (width, height))
		self.screen_cover_ratio = screen_cover_ratio
		self.alpha = alpha
		self.bg_color = bg_color
		self.surface = self.get_sidebar_surface()
		self.components = self.add_sidebar_content()
		self.parent = parent

	def render(self, parent_surface):
		for comp in self.components: comp.render(self.surface)
		parent_surface.blit(self.surface, self.rect.topleft)


	def update(self):
		pass

	def parse_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN: self.check_comp_collision()

	def check_comp_collision(self):
		for comp in self.components:
			if comp.rect.collidepoint(pygame.mouse.get_pos()): comp.click(self.parent, comp.lable)

	def get_sidebar_surface(self):
		s = pygame.Surface((self.width, self.height))
		s.fill(self.bg_color)
		return s
	
	def add_sidebar_content(self):
		snake = Button((30 , 30), 50, 20, SNAKE_BG, on_click = set_current_game,lable = "Snake", offset = self.rect.topleft)
		tictactoe = Button((30, 100), 50, 20, TICTACTOE_BG, on_click = set_current_game, lable = "Tictactoe", offset = self.rect.topleft)
		wordle = Button((30, 170), 50, 20, WORDLE_BG, on_click = set_current_game, lable = "Wordle", offset = self.rect.topleft)
		return [snake, tictactoe, wordle]
	
def set_current_game(parent, lable):
	parent.current_game_surface = parent.games[lable].surface

