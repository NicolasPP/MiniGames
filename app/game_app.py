import pygame, sys, time
from enum import Enum
from typing import Type


import GUI.size as SIZE
import GUI.components.button as btn
import GUI.components.containers as ctn
from GUI.screen import Screen
from games.game import Game, Game_GUI
from games.snake import Snake
from games.wordle import Wordle
from games.tetris import Tetris
from games.main_menu import Main_menu
from config import *


class MG_CONFIG:
	def __init__(self):
		self.SIDEBAR_SPEED = 600
		self.FONT_COLOR : tuple[int, int, int] 		= COLORS['palette2']['on_secondary'] #rgb(220, 215, 201)
		self.BUTTON_COLOR : tuple[int, int, int] 	= COLORS['palette2']['on_primary'] #rgb(63, 78, 79)
		self.BG_COLOR : tuple[int, int, int] 		= COLORS['palette1']['primary'] #rgb(27, 36, 48)
		self.APP_BG_COLOR : tuple[int, int, int] 	= COLORS['palette2']['primary'] #rgb(44, 54, 57)
		self.MEDIUM_SCREEN : tuple[int, int] 		= 960, 600
		self.LARGE_SCREEN : tuple[int, int]			= 1280, 800

	def BUTTON_SIZE(self):
		return SIZE.get(SIZE.Modifier(
				parent_size = SIZE.current_screen_size(),
				modifier_type = SIZE.MODIFIER.PERCENTAGE,
				width_ratio = 8,
				height_ratio = 4 
			))

	def HALF_BUTTON_SIZE(self):
		size = SIZE.get_width(SIZE.Modifier(
				parent_size = pygame.math.Vector2(self.BUTTON_SIZE()) - pygame.math.Vector2(PADDING, 0),
				modifier_type = SIZE.MODIFIER.RATIO,
				ratio = 0.5
			))
		return size, size

	def GAME_SELECT_HEIGHT(self):
		return SIZE.get_height(SIZE.Modifier(
				parent_size = SIZE.current_screen_size(),
				modifier_type = SIZE.MODIFIER.PERCENTAGE,
				ratio = 15
			))

	def COLLAPSE_BUTTON_SIZE(self, sidebar):
		return SIZE.get(SIZE.Modifier(
				parent_size = pygame.math.Vector2(sidebar.rect.size),
				modifier_type = SIZE.MODIFIER.PERCENTAGE,
				width_ratio = 10,
				height_ratio = 50
			))
CONFIG = MG_CONFIG()


class Minigame_GUI(Game_GUI):
	def __init__(self, minigames) -> None:
		super().__init__(minigames)
		self.show_sidebar : bool = True
		self.sidebar_move_distance : int = 0
		self.sidebar_move_direction : int = 1
		self.sidebar_speed = CONFIG.SIDEBAR_SPEED
		self.populate_GUI()
	
	def populate_GUI(self) -> None:
		self.create_containers()
		self.create_buttons()
		self.populate_containers()
		self.center_sidebar()
		self.center_collapse_menu()

	def create_buttons(self) -> None:
		game_menu  		= self.containers['game_menu'] 		
		settings  		= self.containers['settings'] 		
		game_selection  = self.containers['game_selection']

		
		quit 			= btn.Button(settings, CONFIG.HALF_BUTTON_SIZE(), CONFIG.BG_COLOR, message = "Quit", on_click = quit_game, show_lable= False)
		full_screen 	= btn.Button(settings, CONFIG.HALF_BUTTON_SIZE(), CONFIG.BG_COLOR, message = "Fullscreen", on_click = fullscreen, show_lable= False, button_type = btn.Button_Type.SWITCH, active = self.game.screen.full_screen)
		menu 			= btn.Button(game_menu, CONFIG.BUTTON_SIZE(), CONFIG.BUTTON_COLOR, message = "Menu", on_click = set_game, show_lable= True, font_color = CONFIG.FONT_COLOR)
		snake 			= btn.Button(game_selection, CONFIG.BUTTON_SIZE(), CONFIG.BUTTON_COLOR, message = "Snake", on_click = set_game, show_lable = True, font_color = CONFIG.FONT_COLOR)
		tetris 			= btn.Button(game_selection, CONFIG.BUTTON_SIZE(), CONFIG.BUTTON_COLOR, message = "Tetris", on_click = set_game, show_lable= True, font_color = CONFIG.FONT_COLOR)
		wordle 			= btn.Button(game_selection, CONFIG.BUTTON_SIZE(), CONFIG.BUTTON_COLOR, message = "Wordle", on_click = set_game, show_lable= True, font_color = CONFIG.FONT_COLOR)
		life_game 		= btn.Button(game_selection, CONFIG.BUTTON_SIZE(), CONFIG.BUTTON_COLOR, message = "Life Game", show_lable = True, font_color = CONFIG.FONT_COLOR)



		btn.style_quit(quit)
		full_screen.set_active_style(btn.fullscreen_active_style, full_screen)
		full_screen.set_inactive_style(btn.fullscreen_inactive_style, full_screen)
		self.buttons['quit'] 			= quit
		self.buttons['full_screen'] 	= full_screen
		self.buttons['menu'] 			= menu
		self.buttons['snake'] 			= snake
		self.buttons['tetris'] 			= tetris
		self.buttons['wordle'] 			= wordle
		self.buttons['life_game']		= life_game


	def create_containers(self) -> None:
		sidebar 			= ctn.Linear_Container(self, ctn.LAYOUT_PLANE.VERTICAL, color = CONFIG.BG_COLOR, padding = ctn.Padding(spacing = PADDING * 2), root = True)
		game_menu 			= ctn.Linear_Container(sidebar, ctn.LAYOUT_PLANE.VERTICAL, color = CONFIG.BG_COLOR, padding = ctn.Padding(0,0,0,0,PADDING))
		settings 			= ctn.Linear_Container(game_menu, ctn.LAYOUT_PLANE.HORIZONTAL, color = CONFIG.BG_COLOR, padding = ctn.Padding(0,0,0,0,PADDING))
		game_selection 		= ctn.Scrollable_Container(sidebar, ctn.LAYOUT_PLANE.VERTICAL, color = CONFIG.BG_COLOR, padding = ctn.Padding(0,0,0,0))


		sidebar.conpensate_padding = False
		self.containers['sidebar'] 			= sidebar
		self.containers['game_menu'] 		= game_menu
		self.containers['settings'] 		= settings
		self.containers['game_selection']	= game_selection


	def populate_containers(self) -> None:
		quit  			= self.buttons['quit'] 				
		full_screen  	= self.buttons['full_screen'] 		
		menu  			= self.buttons['menu'] 				
		snake  			= self.buttons['snake'] 				
		tetris  		= self.buttons['tetris'] 			
		wordle  		= self.buttons['wordle']
		life_game		= self.buttons['life_game']
		sidebar  		= self.containers['sidebar'] 			
		game_menu  		= self.containers['game_menu'] 		
		settings  		= self.containers['settings'] 		
		game_selection  = self.containers['game_selection']	

		game_selection.add_component(snake)
		game_selection.add_component(wordle)
		game_selection.add_component(life_game)
		game_selection.add_component(tetris)
		settings.add_component(quit)
		settings.add_component(full_screen)
		game_menu.add_component(settings)
		game_menu.add_component(menu)
		

		game_selection.set_size((game_menu.rect.width, CONFIG.GAME_SELECT_HEIGHT()))
		game_selection.fixed_size = True

		sidebar.add_component(game_menu)
		sidebar.add_component(game_selection)

		collapsed_menu  = btn.Button(self.game, CONFIG.COLLAPSE_BUTTON_SIZE(sidebar), CONFIG.FONT_COLOR , message = "collapsed_menu", on_click =toggle_sidebar, alpha = 20, show_lable = False, button_type = btn.Button_Type.SWITCH, active = self.show_sidebar)
		collapsed_menu.set_active_style(btn.expanded_menu_style, collapsed_menu)
		collapsed_menu.set_inactive_style(btn.collapsed_menu_style, collapsed_menu)
		self.buttons['collapsed_menu']  = collapsed_menu


	def center_collapse_menu(self) -> None:
		self.buttons['collapsed_menu'].rect.left = self.containers['sidebar'].rect.right
		self.buttons['collapsed_menu'].rect.centery = self.containers['sidebar'].rect.centery

	def center_sidebar(self) -> None:
		self.containers['sidebar'].rect.centery = pygame.display.get_surface().get_rect().centery

	def toggle_sidebar(self) -> None:
		self.show_sidebar = not self.show_sidebar
		self.sidebar_move_direction = self.sidebar_move_direction * -1
		self.sidebar_move_distance = self.containers['sidebar'].rect.width

	def render_sidebar(self) -> None:
		self.containers['sidebar'].render(True)
		self.buttons['collapsed_menu'].render(True)

	def update_sidebar(self, dt : float) -> None:
		if self.sidebar_move_distance <= 0: return

		dist = dt * self.sidebar_speed

		self.sidebar_move_distance = round(self.sidebar_move_distance - dist)
		new_xpos = self.containers['sidebar'].rect.left + dist * self.sidebar_move_direction


		if new_xpos < self.containers['sidebar'].rect.w * -1: new_xpos = self.containers['sidebar'].rect.w * -1
		if new_xpos > 0: new_xpos = 0

		self.containers['sidebar'].rect.left = round(new_xpos)
		self.center_collapse_menu()


class Minigames:
	def __init__(self) -> None:
		# initialize main pygame surface
		self.screen : Screen = Screen(*CONFIG.MEDIUM_SCREEN, color = CONFIG.APP_BG_COLOR)
		self.running : bool = True

		# time
		self.clock : pygame.time.Clock =  pygame.time.Clock()
		self.delta_time : float = 0
		self.prev_time : float = time.time()
		
		#Games

		self.current_game : str = 'Menu'


		self.games : dict[str, Game]= {
			"Menu" : Main_menu(self),
			"Snake" : Snake(self),
			"Tetris" : Tetris(self),
			"Wordle" : Wordle(self),
		}

		self.GUI : Minigame_GUI = Minigame_GUI(self)

	@property
	def surface(self) -> pygame.Surface: return self.screen.surface
	@surface.setter
	def surface(self, new_surface : pygame.Surface) -> None: self._surface = new_surface
	@surface.deleter
	def surface(self) -> None: del self._surface



	# Main Game Functions

	def run(self) -> None:
		while self.running:
			
			self.get_current_game().surface.fill(self.get_current_game().color)

			self.set_delta_time()
			for event in pygame.event.get(): self.parse_event(event)


			self.update(self.delta_time)
			self.render()

			pygame.display.update()
		pygame.quit()
		sys.exit()
			
	def update(self, dt : float) -> None:
		self.get_current_game().update(dt)
		self.GUI.update_sidebar(dt)

	def render(self) -> None:
		self.get_current_game().render()
		self.GUI.render_sidebar()
		self.screen.render()

	def set_delta_time(self) -> None:
		self.delta_time = time.time() - self.prev_time
		self.prev_time = time.time()

	def toggle_fullscreen(self) -> None:
		self.screen.toggle_full_screen()
		for name, game in self.games.items(): game.update_screen_size()
		self.GUI = Minigame_GUI(self)
	
	def get_current_game(self) -> Game: 
		return self.games[self.current_game]
	
	# Game events Parser 
	def parse_event(self, event : pygame.event.Event) -> None:

		self.GUI.containers['sidebar'].parse_event(event, self)
		self.get_current_game().parse_event(event)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.GUI.buttons['collapsed_menu'].is_hovered(pygame.math.Vector2(pygame.mouse.get_pos())):
				self.GUI.buttons['collapsed_menu'].click(self.GUI, self.GUI.buttons['collapsed_menu'])

		if event.type == pygame.MOUSEMOTION: self.GUI.buttons['collapsed_menu'].on_hover()
	
	def quit_game(self) -> None:
		self.running = False

# GUI BUTTON LOGIC

def set_game(parent, comp):
	if parent.current_game == comp.message: return
	parent.current_game = comp.message

def fullscreen(parent, comp):
	parent.toggle_fullscreen()

def quit_game(parent, comp):
	parent.quit_game()

def toggle_sidebar(parent, comp):
	parent.toggle_sidebar()
