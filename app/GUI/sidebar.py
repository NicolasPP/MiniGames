import pygame
from app.app_config import *
from games.games_config import *
from app.GUI.button import Button, Button_Type
class Sidebar:
	def __init__(self, width, height, parent, alpha = 1, bg_color = BG_COLOR):
		self.parent = parent
		self.width, self.height = self.set_dimensions()
		self.topleft = (PADDING,PADDING)
		self.alpha = alpha
		self.bg_color = bg_color
		self.surface = self.get_sidebar_surface()
		self.components = self.add_sidebar_content()

	def render(self, parent_surface):
		for comp in self.components: comp.render(self.surface)
		parent_surface.blit(self.surface, self.topleft)


	def update(self):
		pass

	def update_surface_size(self):
		self.width, self.height = self.set_dimensions()
		self.surface = self.get_sidebar_surface()
		self.components = self.add_sidebar_content()

	def set_dimensions(self):
		return (PADDING * 2) + BUTTON_W, self.parent.screen.current_height - (PADDING * 2)
	def parse_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN: self.check_comp_collision()

	def check_comp_collision(self):
		for comp in self.components:
			if comp.rect.collidepoint(pygame.mouse.get_pos()): comp.click(self.parent, comp)

	def get_sidebar_surface(self):
		s = pygame.Surface((self.width, self.height))
		s.fill(self.bg_color)
		return s
	
	def add_sidebar_content(self):
		snake = Button((PADDING , PADDING), BUTTON_W, BUTTON_H, SNAKE_BG, on_click = set_game,lable = "Snake", offset = self.topleft, show_lable = True)
		tictactoe = Button((PADDING, (PADDING * 3) + BUTTON_H), BUTTON_W, BUTTON_H, TICTACTOE_BG, on_click = set_game, lable = "Tictactoe", offset = self.topleft, show_lable= True)
		wordle = Button((PADDING, (PADDING * 5) + (BUTTON_H * 2)), BUTTON_W, BUTTON_H, WORDLE_BG, on_click = set_game, lable = "Wordle", offset = self.topleft, show_lable= True)
		back = Button((PADDING, self.height - (PADDING * 2) - (BUTTON_H * 2)), BUTTON_W, BUTTON_H, BACK_BUTTON_COLOR, on_click = set_game, lable = "Menu", offset = self.topleft, show_lable= True)
		quit = Button((PADDING, self.height - PADDING - BUTTON_H), (BUTTON_W - PADDING) // 2, BUTTON_H, "Red", on_click = quit_game, lable = "Quit", offset = self.topleft, show_lable= False)
		full_screen = Button(((PADDING * 2) + (BUTTON_W - PADDING) // 2, self.height - PADDING - BUTTON_H), (BUTTON_W - PADDING) // 2, BUTTON_H, "Green", on_click = fullscreen, lable = "Fullscreen", offset = self.topleft, show_lable= False)
		return [snake, tictactoe, wordle, quit, back, full_screen]


# GUI BUTTON LOGIC

def set_game(parent, comp):
	if parent.current_game == comp.lable: return
	parent.current_game = comp.lable

def fullscreen(parent, comp):
	parent.toggle_fullscreen()

def quit_game(parent, comp):
	parent.running = False

