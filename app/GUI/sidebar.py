import pygame
from config.app_config import *
from GUI.components.button import Button, Button_Type
from GUI.components.containers import Container, Scrollable_Container, LAYOUT_PLANE, Padding

class Sidebar:
	def __init__(self, width, height, parent, alpha = 1, bg_color = BG_COLOR):
		self.parent = parent
		self.rect = pygame.Rect((PADDING, PADDING), self.get_size())
		self.alpha = alpha
		self.bg_color = bg_color
		self.root_container = get_root_container(self)
		self.surface = self.get_sidebar_surface()
		self._mouse_pos = pygame.mouse.get_pos()

	@property
	def mouse_pos(self):
		mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
		sidebar_offset = pygame.math.Vector2(self.rect.topleft)
		return tuple(mouse_pos - sidebar_offset)
	
	@mouse_pos.setter
	def mouse_pos(self, new_mouse_pos): self._mouse_pos = new_mouse_pos

	@mouse_pos.deleter
	def mouse_pos(self): del self._mouse_pos

	def render(self, parent_surface):
		self.surface.fill(self.bg_color)
		self.root_container.render()
		parent_surface.blit(self.surface, self.rect.topleft)

	def update(self, dt): pass

	def update_surface_size(self):
		self.rect.size = self.get_size()
		self.surface = self.get_sidebar_surface()
		self.root_container = get_root_container(self)

	def get_size(self):
		return (PADDING * 2) + BUTTON_W, self.parent.screen.current_height - (PADDING * 2)
	
	def parse_event(self, event):
		self.root_container.parse_event(event, self)

	def is_hovering(self):
		return self.surface.get_rect().collidepoint(self.mouse_pos)

	def get_sidebar_surface(self):
		surface = pygame.Surface(self.rect.size)
		surface.fill(self.bg_color)
		return surface

def get_root_container(sidebar):
	root = Container(sidebar, BG_COLOR, LAYOUT_PLANE.VERTICAL, root = True, padding = Padding(spacing = PADDING * 2) )
	game_menu = settings = Container(root, BG_COLOR, LAYOUT_PLANE.VERTICAL, padding = Padding(0,0,0,0,PADDING))
	settings = Container(game_menu, BG_COLOR, LAYOUT_PLANE.HORIZONTAL, padding = Padding(0,0,0,0,PADDING))
	game_selection = get_game_selection_container(sidebar, root)
	
	half_button_size = ((BUTTON_W - PADDING) // 2, BUTTON_H)
	button_size = BUTTON_W, BUTTON_H

	quit = Button(settings, half_button_size, BG_COLOR, message = "Quit", on_click = quit_game, show_lable= False)
	full_screen = Button(settings, half_button_size, BG_COLOR, message = "Fullscreen", on_click = fullscreen, show_lable= False, button_type = Button_Type.SWITCH, active = sidebar.parent.screen.full_screen)
	menu = Button(game_menu, button_size, BUTTON_COLOR, message = "Menu", on_click = set_game, show_lable= True, font_color = FONT_COLOR)
	
	style_quit(quit)

	full_screen.set_active_style(fullscreen_active_style, full_screen)
	full_screen.set_inctive_style(fullscreen_inactive_style, full_screen)

	settings.add_component(quit)
	settings.add_component(full_screen)

	game_menu.add_component(settings)
	game_menu.add_component(menu)


	root.add_component(game_menu)
	root.add_component(game_selection)

	return root

def get_game_selection_container(sidebar, parent):
	game_selection = Scrollable_Container(parent, BG_COLOR, LAYOUT_PLANE.VERTICAL, padding = Padding(top = 0), size = sidebar.get_size())
		
	button_size = (BUTTON_W, BUTTON_H)
	
	snake = Button(game_selection, button_size, BUTTON_COLOR, message = "Snake", on_click = set_game, show_lable = True, font_color = FONT_COLOR)
	tictactoe = Button(game_selection, button_size, BUTTON_COLOR, message = "Tictactoe", on_click = set_game, show_lable= True, font_color = FONT_COLOR)
	wordle = Button(game_selection, button_size, BUTTON_COLOR, message = "Wordle", on_click = set_game, show_lable= True, font_color = FONT_COLOR)

	game_selection.add_component(snake)
	game_selection.add_component(wordle)
	game_selection.add_component(tictactoe)

	return game_selection


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
	button.surface.fill(button.color)
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
	button.surface.fill(button.color)

	for rect in rects: pygame.draw.rect(button.surface, "White", rect)

