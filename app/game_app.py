import pygame, sys, time
from enum import Enum
from typing import Type

from GUI.screen import Screen
from GUI.sidebar import Sidebar
from GUI.components.button import Button, style_quit, fullscreen_inactive_style, fullscreen_active_style, Button_Type
from GUI.components.containers import Container, Scrollable_Container, LAYOUT_PLANE, Padding

from games.game import Game
from games.snake import Snake
from games.wordle import Wordle
from games.tictactoe import Tictactoe
from games.main_menu import Main_menu

from config.app_config import *
import config.games_config as gcfg

class RES1610:
    MEDIUM = 960, 600
    LARGE = 1280, 800



class Game_GUI:
	def __init__(self, minigames):
		self.minigames = minigames
		self.containers = {}
		self.buttons = {}
		self._surface = minigames.screen.surface
		self.populate_GUI()

	@property
	def surface(self): return self.minigames.screen.surface
	@surface.setter
	def surface(self, new_surface): self._surface = new_surface
	@surface.deleter
	def surface(self): del self._surfacex
	
	def populate_GUI(self):
		self.create_containers()
		self.create_buttons()
		self.populate_containers()

	def create_buttons(self):
		game_menu  		= self.containers['game_menu'] 		
		settings  		= self.containers['settings'] 		
		game_selection  = self.containers['game_selection']	
		half_button_size = ((BUTTON_W - PADDING) // 2, BUTTON_H)
		button_size = BUTTON_W, BUTTON_H
		
		quit 			= Button(settings, half_button_size, BG_COLOR, message = "Quit", on_click = quit_game, show_lable= False)
		full_screen 	= Button(settings, half_button_size, BG_COLOR, message = "Fullscreen", on_click = fullscreen, show_lable= False, button_type = Button_Type.SWITCH, active = self.minigames.screen.full_screen)
		menu 			= Button(game_menu, button_size, BUTTON_COLOR, message = "Menu", on_click = set_game, show_lable= True, font_color = FONT_COLOR)
		snake 			= Button(game_selection, button_size, BUTTON_COLOR, message = "Snake", on_click = set_game, show_lable = True, font_color = FONT_COLOR)
		tictactoe 		= Button(game_selection, button_size, BUTTON_COLOR, message = "Tictactoe", on_click = set_game, show_lable= True, font_color = FONT_COLOR)
		wordle 			= Button(game_selection, button_size, BUTTON_COLOR, message = "Wordle", on_click = set_game, show_lable= True, font_color = FONT_COLOR)
		
		style_quit(quit)
		full_screen.set_active_style(fullscreen_active_style, full_screen)
		full_screen.set_inctive_style(fullscreen_inactive_style, full_screen)
		
		self.buttons['quit'] 			= quit
		self.buttons['full_screen'] 	= full_screen
		self.buttons['menu'] 			= menu
		self.buttons['snake'] 			= snake
		self.buttons['tictactoe'] 		= tictactoe
		self.buttons['wordle'] 			= wordle


	def create_containers(self):
		sidebar 		= Container(self, LAYOUT_PLANE.VERTICAL, color = BG_COLOR,padding = Padding(spacing = PADDING * 2), root = True )
		game_menu 		= Container(sidebar, LAYOUT_PLANE.VERTICAL, color = BG_COLOR, padding = Padding(0,0,0,0,PADDING))
		settings 		= Container(game_menu, LAYOUT_PLANE.HORIZONTAL, color = BG_COLOR, padding = Padding(0,0,0,0,PADDING))
		game_selection 	= Scrollable_Container(sidebar, LAYOUT_PLANE.VERTICAL, color = BG_COLOR, padding = Padding(top = 0))
		self.containers['sidebar'] 			= sidebar
		self.containers['game_menu'] 		= game_menu
		self.containers['settings'] 		= settings
		self.containers['game_selection']	= game_selection


	def populate_containers(self):
		quit  			= self.buttons['quit'] 				
		full_screen  	= self.buttons['full_screen'] 		
		menu  			= self.buttons['menu'] 				
		snake  			= self.buttons['snake'] 				
		tictactoe  		= self.buttons['tictactoe'] 			
		wordle  		= self.buttons['wordle'] 				
		sidebar  		= self.containers['sidebar'] 			
		game_menu  		= self.containers['game_menu'] 		
		settings  		= self.containers['settings'] 		
		game_selection  = self.containers['game_selection']	

		game_selection.add_component(snake)
		game_selection.add_component(wordle)
		game_selection.add_component(tictactoe)

		settings.add_component(quit)
		settings.add_component(full_screen)

		game_menu.add_component(settings)
		game_menu.add_component(menu)


		sidebar.add_component(game_menu)
		sidebar.add_component(game_selection)



class Minigames:
	def __init__(self, s_width : int, s_height : int, full_screen : bool) -> None:
		# initialize main pygame surface
		self.screen : Screen = Screen(*RES1610.MEDIUM, full_screen, color = APP_BG_COLOR)
		self.running : bool = True

		# time
		self.clock : pygame.time.Clock =  pygame.time.Clock()
		self.delta_time : float = 0
		self.prev_time : float = time.time()


		# GUI elements
		self.sidebar : Sidebar = Sidebar(self.screen.current_width, self.screen.current_height, self)
		
		#Games

		self.current_game = 'Menu'


		self.games : dict[str, Game]= {
			"Menu" : Main_menu(self),
			"Snake" : Snake(self),
			"Tictactoe" : Tictactoe(self),
			"Wordle" : Wordle(self),
		}

		self.GUI = Game_GUI(self)


	# Main Game Functions

	def run(self) -> None:
		while self.running:
			
			self.get_current_game().surface.fill(self.get_current_game().color)

			self.set_delta_time()
			for event in pygame.event.get(): self.parse_event(event)


			self.update(self.delta_time)
			self.render()

			pygame.display.update()
			
	def update(self, dt : float) -> None:
		self.get_current_game().update(dt)

	def render(self) -> None:
		sidebar = self.GUI.containers['sidebar']
		self.get_current_game().render()
		if sidebar.is_hovered(pygame.mouse.get_pos()) : sidebar.render()
		self.screen.render()

	def set_delta_time(self) -> None:
		self.delta_time = time.time() - self.prev_time
		self.prev_time = time.time()

	def toggle_fullscreen(self) -> None:
		self.screen.toggle_full_screen()
		for name, game in self.games.items(): game.update_surface_size()
		self.GUI = Game_GUI(self)
	
	def get_current_game(self): 
		return self.games[self.current_game]
	
	# Game events Parser 
	def parse_event(self, event : pygame.event.Event) -> None:

		self.GUI.containers['sidebar'].parse_event(event, self)
		self.get_current_game().parse_event(event)
	
	def quit_game(self) -> None:
		self.running = False
		pygame.quit()
		sys.exit()

# GUI BUTTON LOGIC

def set_game(parent, comp):
	if parent.current_game == comp.message: return
	parent.current_game = comp.message

def fullscreen(parent, comp):
	parent.toggle_fullscreen()

def quit_game(parent, comp):
	parent.quit_game()
