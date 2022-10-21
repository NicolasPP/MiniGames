import pygame
from config.app_config import *
from GUI.components.button import Button, Button_Type
from GUI.components.containers import Container, LAYOUT_PLANE


class MOUSECLICK:
	LEFT = 1
	MIDDLE = 2
	RIGHT = 3
	SCROLL_UP = 4
	SCROLL_DOWN = 5

class Sidebar:
	def __init__(self, width, height, parent, alpha = 1, bg_color = BG_COLOR):
		self.parent = parent
		self.rect = pygame.Rect((PADDING, PADDING), self.get_size())
		self.alpha = alpha
		self.bg_color = bg_color
		self.surface = self.get_sidebar_surface()
		self.fixed_components = self.add_settings()
		self.scrollable_components = self.add_scrollable_content()
		self._scroll_offset = pygame.math.Vector2(0,0)
		self.scroll_speed = pygame.math.Vector2(0,10)
		a = Container(self, (0,0), 'black', LAYOUT_PLANE.HORIZONTAL)




	@property
	def scroll_offset(self): return self._scroll_offset

	@scroll_offset.setter
	def scroll_offset(self, new_scroll_offset):
		self.scrollable_components.sort(key = lambda x : x.rect.y)
		self.fixed_components.sort(key = lambda x : x.rect.y)
		last_comp = self.scrollable_components[-1]
		first_comp = self.scrollable_components[0] 
		last_pos = pygame.math.Vector2(last_comp.rect.bottomleft)  + new_scroll_offset
		first_pos = pygame.math.Vector2(first_comp.rect.topleft)  + new_scroll_offset
		if last_pos.y  <= self.rect.height - PADDING and first_pos.y >= self.fixed_components[-1].rect.bottom + (PADDING * 3):
			self._scroll_offset = self._scroll_offset + new_scroll_offset
			for comp in self.scrollable_components: comp.update_pos(new_scroll_offset)

	@scroll_offset.deleter
	def scroll_offset(self): del self._scroll_offset

	def get_components(self): return self.scrollable_components + self.fixed_components

	def render(self, parent_surface):
		self.surface.fill(self.bg_color)
		for comp in self.get_components(): comp.render()
		parent_surface.blit(self.surface, self.rect.topleft)

	def update(self, dt): pass

	def update_surface_size(self):
		self.rect.size = self.get_size()
		self.surface = self.get_sidebar_surface()

	def get_size(self):
		return (PADDING * 2) + BUTTON_W, self.parent.screen.current_height - (PADDING * 2)
	
	def parse_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == MOUSECLICK.LEFT: 	    self.check_comp_collision()
			if event.button == MOUSECLICK.SCROLL_UP :   self.scroll_offset = self.scroll_speed
			if event.button == MOUSECLICK.SCROLL_DOWN : self.scroll_offset = self.scroll_speed * -1
	
	def is_hovering(self):
		return self.surface.get_rect().collidepoint(pygame.mouse.get_pos())

	def check_comp_collision(self):
		for comp in self.get_components():
			if comp.is_clicked(pygame.mouse.get_pos()): comp.click(self.parent, comp)

	def get_sidebar_surface(self):
		surface = pygame.Surface(self.rect.size)
		surface.fill(self.bg_color)
		return surface
	
	def get_sidebar_game_offset(self):
		return (PADDING * 4) + BUTTON_W, PADDING

	def add_settings(self):
		button_size = (BUTTON_W, BUTTON_H)
		menu_pos = (PADDING, (PADDING * 2) + BUTTON_H)
		quit_size = ((BUTTON_W - PADDING) // 2, BUTTON_H)
		full_screen_size = ((BUTTON_W - PADDING) // 2, BUTTON_H)
		quit_pos = (PADDING, PADDING)
		full_screen_pos =((PADDING * 2) + (BUTTON_W - PADDING) // 2, PADDING)
		quit = Button(self, quit_pos, quit_size, BG_COLOR, message = "Quit", on_click = quit_game, show_lable= False)
		full_screen = Button(self, full_screen_pos, full_screen_size, BG_COLOR, message = "Fullscreen", on_click = fullscreen, show_lable= False, button_type = Button_Type.SWITCH)
		menu = Button(self, menu_pos, button_size, BUTTON_COLOR, message = "Menu", on_click = set_game, show_lable= True, font_color = FONT_COLOR)	
		quit.style(style_quit, quit)
		full_screen.set_active_style(fullscreen_active_style, full_screen)
		full_screen.set_inctive_style(fullscreen_inactive_style, full_screen)
		full_screen.update_style()
		return [quit, full_screen, menu]

	def add_scrollable_content(self):
		offset_w, offset_h = self.rect.topleft
		button_size = (BUTTON_W, BUTTON_H)
		
		snake_pos = (PADDING, (PADDING * 5) + (BUTTON_H * 2))
		tictactoe_pos = (PADDING, (PADDING * 6) + (BUTTON_H * 3))
		wordle_pos = (PADDING, (PADDING * 7) + (BUTTON_H * 4))
		
		snake = Button(self, snake_pos, button_size, BUTTON_COLOR, message = "Snake", on_click = set_game, show_lable = True, font_color = FONT_COLOR)
		tictactoe = Button(self, tictactoe_pos, button_size, BUTTON_COLOR, message = "Tictactoe", on_click = set_game, show_lable= True, font_color = FONT_COLOR)
		wordle = Button(self, wordle_pos, button_size, BUTTON_COLOR, message = "Wordle", on_click = set_game, show_lable= True, font_color = FONT_COLOR)
		return [snake, tictactoe, wordle]


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

