import pygame
from config.app_config import *
from GUI.button import Button, Button_Type
class Sidebar:
	def __init__(self, width, height, parent, alpha = 1, bg_color = BG_COLOR):
		self.parent = parent
		self.width, self.height = self.get_dimensions()
		self.topleft = (PADDING,PADDING)
		self.alpha = alpha
		self.bg_color = bg_color
		self.surface = self.get_sidebar_surface()
		self.components = self.add_sidebar_content()

	def render(self, parent_surface):
		for comp in self.components: comp.render(self.surface)
		parent_surface.blit(self.surface, self.topleft)


	def update(self, dt): pass

	def update_surface_size(self):
		self.width, self.height = self.get_dimensions()
		self.surface = self.get_sidebar_surface()

	def get_dimensions(self):
		return (PADDING * 2) + BUTTON_W, self.parent.screen.current_height - (PADDING * 2)
	
	def parse_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN: self.check_comp_collision()

	def check_comp_collision(self):
		for comp in self.components:
			if comp.is_clicked(pygame.mouse.get_pos()): comp.click(self.parent, comp)

	def get_sidebar_surface(self):
		s = pygame.Surface((self.width, self.height))
		s.fill(self.bg_color)
		return s
	def get_sidebar_game_offset(self):
		return (PADDING * 4) + BUTTON_W, PADDING
	

	def add_settings(self):
		quit_size = ((BUTTON_W - PADDING) // 2, BUTTON_H)
		full_screen_size = ((BUTTON_W - PADDING) // 2, BUTTON_H)
		quit_pos = (PADDING, PADDING)
		full_screen_pos =((PADDING * 2) + (BUTTON_W - PADDING) // 2, PADDING)
		quit = Button(quit_pos, quit_size, BG_COLOR, message = "Quit", offset = self.topleft, on_click = quit_game, show_lable= False)
		full_screen = Button(full_screen_pos, full_screen_size, BG_COLOR, message = "Fullscreen", offset = self.topleft, on_click = fullscreen, show_lable= False, button_type = Button_Type.SWITCH)
		quit.style(style_quit, quit)
		full_screen.set_active_style(fullscreen_active_style, full_screen)
		full_screen.set_inctive_style(fullscreen_inactive_style, full_screen)
		full_screen.update_style()
		return [quit, full_screen]

	def add_scrollable_content(self):
		offset_w, offset_h = self.topleft
		button_size = (BUTTON_W, BUTTON_H)
		back_pos = (PADDING, (PADDING * 2) + BUTTON_H)
		snake_pos = (PADDING, (PADDING * 5) + (BUTTON_H * 2))
		tictactoe_pos = (PADDING, (PADDING * 6) + (BUTTON_H * 3))
		wordle_pos = (PADDING, (PADDING * 7) + (BUTTON_H * 4))
		back = Button(back_pos, button_size, BUTTON_COLOR, message = "Menu", offset = self.topleft, on_click = set_game, show_lable= True, font_color = FONT_COLOR)	
		snake = Button(snake_pos, button_size, BUTTON_COLOR, message = "Snake", offset = self.topleft, on_click = set_game, show_lable = True, font_color = FONT_COLOR)
		tictactoe = Button(tictactoe_pos, button_size, BUTTON_COLOR, message = "Tictactoe", offset = self.topleft, on_click = set_game, show_lable= True, font_color = FONT_COLOR)
		wordle = Button(wordle_pos, button_size, BUTTON_COLOR, message = "Wordle", offset = self.topleft, on_click = set_game, show_lable= True, font_color = FONT_COLOR)
		return [snake, tictactoe, wordle, back]


	def add_sidebar_content(self):
		return self.add_settings() + self.add_scrollable_content()
	

# GUI BUTTON LOGIC

def set_game(parent, comp):
	if parent.current_game == comp.message: return
	parent.current_game = comp.message

def fullscreen(parent, comp):
	parent.toggle_fullscreen()

def quit_game(parent, comp):
	parent.quit_game()

def style_quit(button):
	pygame.draw.line(button.surface, "Red", (5, 5), (button.rect.width - 5, button.rect.height - 5), 4)
	pygame.draw.line(button.surface, "Red", (button.rect.width - 5, 5), (5, button.rect.height - 5), 4)

def fullscreen_active_style(button):
	rects = [
		#topleft
		pygame.Rect((FS_RECT_WIDTH - FS_RECT_HEIGHT, 0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((0, FS_RECT_WIDTH - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#topright
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, 0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, FS_RECT_WIDTH - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#bottomleft
		pygame.Rect((0, button.rect.height - FS_RECT_WIDTH), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((FS_RECT_WIDTH - FS_RECT_HEIGHT, button.rect.h - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		#bottomright
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, button.rect.h - FS_RECT_WIDTH), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, button.rect.h - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
	]
	for rect in rects: pygame.draw.rect(button.surface, "White", rect)

def fullscreen_inactive_style(button):
	rects = [
		# topleft
		pygame.Rect((0,0), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((0,0), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		#topright
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, 0), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		pygame.Rect((button.rect.w - FS_RECT_HEIGHT, 0), (FS_RECT_HEIGHT , FS_RECT_WIDTH)),
		#bottomleft
		pygame.Rect((0, button.rect.h-FS_RECT_WIDTH), (FS_RECT_HEIGHT,FS_RECT_WIDTH)),
		pygame.Rect((0, button.rect.h-FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
		#bottomright
		pygame.Rect((button.rect.w - FS_RECT_HEIGHT, button.rect.h - FS_RECT_WIDTH), (FS_RECT_HEIGHT, FS_RECT_WIDTH)),
		pygame.Rect((button.rect.w - FS_RECT_WIDTH, button.rect.h - FS_RECT_HEIGHT), (FS_RECT_WIDTH, FS_RECT_HEIGHT)),
	]
	for rect in rects: pygame.draw.rect(button.surface, "White", rect)


