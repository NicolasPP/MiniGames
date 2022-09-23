import pygame
from app.app_config import *
import games.games_config as gcfg
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
		# self.components = self.add_sidebar_content()

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
		quit = Button((PADDING, PADDING), (BUTTON_W - PADDING) // 2, BUTTON_H, BG_COLOR, on_click = quit_game, lable = "Quit", offset = self.topleft, show_lable= False,)
		full_screen = Button(((PADDING * 2) + (BUTTON_W - PADDING) // 2, PADDING), (BUTTON_W - PADDING) // 2, BUTTON_H, BG_COLOR, on_click = fullscreen, lable = "Fullscreen", offset = self.topleft, show_lable= False, button_type = Button_Type.SWITCH)
		back = Button((PADDING, (PADDING * 2) + BUTTON_H), BUTTON_W, BUTTON_H, BUTTON_COLOR, on_click = set_game, lable = "Menu", offset = self.topleft, show_lable= True, font_color = FONT_COLOR)	
		snake = Button((PADDING , (PADDING * 5) + (BUTTON_H * 2)), BUTTON_W, BUTTON_H, BUTTON_COLOR, on_click = set_game,lable = "Snake", offset = self.topleft, show_lable = True, font_color = FONT_COLOR)
		tictactoe = Button((PADDING , (PADDING * 6) + (BUTTON_H * 3)), BUTTON_W, BUTTON_H, BUTTON_COLOR, on_click = set_game, lable = "Tictactoe", offset = self.topleft, show_lable= True, font_color = FONT_COLOR)
		wordle = Button((PADDING , (PADDING * 7) + (BUTTON_H * 4)), BUTTON_W, BUTTON_H, BUTTON_COLOR, on_click = set_game, lable = "Wordle", offset = self.topleft, show_lable= True, font_color = FONT_COLOR)
		quit.style(style_quit, quit)
		full_screen.set_active_style(fullscreen_active_style, full_screen)
		full_screen.set_inctive_style(fullscreen_inactive_style, full_screen)
		full_screen.update_style()
		return [snake, tictactoe, wordle, quit, back, full_screen]


# GUI BUTTON LOGIC

def set_game(parent, comp):
	if parent.current_game == comp.lable: return
	parent.current_game = comp.lable

def fullscreen(parent, comp):
	parent.toggle_fullscreen()

def quit_game(parent, comp):
	parent.running = False

def style_quit(button):
	pygame.draw.line(button.surface, "Red", (5, 5), (button.width - 5, button.height - 5), 4)
	pygame.draw.line(button.surface, "Red", (button.width - 5, 5), (5, button.height - 5), 4)

def fullscreen_active_style(button):
	rects = [
		#topleft
		pygame.Rect((FS_RECT_WIDTH - FS_RECT_HEIGHT, 0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((0, FS_RECT_WIDTH - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#topright
		pygame.Rect((button.width - FS_RECT_WIDTH, 0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((button.width - FS_RECT_WIDTH, FS_RECT_WIDTH - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#bottomleft
		pygame.Rect((0, button.height - FS_RECT_WIDTH), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((FS_RECT_WIDTH - FS_RECT_HEIGHT, button.height - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		#bottomright
		pygame.Rect((button.width - FS_RECT_WIDTH, button.height - FS_RECT_WIDTH), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((button.width - FS_RECT_WIDTH, button.height - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
	]
	for rect in rects: pygame.draw.rect(button.surface, "White", rect)

def fullscreen_inactive_style(button):
	rects = [
		# topleft
		pygame.Rect((0,0), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((0,0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		#topright
		pygame.Rect((button.width - FS_RECT_WIDTH, 0), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((button.width - FS_RECT_HEIGHT, 0), (FS_RECT_HEIGHT , FS_RECT_WIDTH)),
		#bottomleft
		pygame.Rect((0, button.height-FS_RECT_WIDTH), (FS_RECT_HEIGHT,FS_RECT_WIDTH)),
		pygame.Rect((0, button.height-FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#bottomright
		pygame.Rect((button.width - FS_RECT_HEIGHT, button.height - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((button.width - FS_RECT_WIDTH, button.height - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
	]
	for rect in rects: pygame.draw.rect(button.surface, "White", rect)


