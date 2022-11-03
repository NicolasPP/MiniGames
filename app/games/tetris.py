from config.games_config import *
from games.game import Game, Game_GUI
from GUI.components.containers import Relative_Container

from typing import TypeAlias
from enum import Enum

class TETROMINO(Enum):
	T_SHAPE : TypeAlias = tuple[list[list[int]], tuple[int,int,int]]
	I : T_SHAPE = [
	 	[1,1,1,1],
	 	[0,0,0,0]
	 ], (50, 199, 239) # rgb(50, 199, 239)
	O : T_SHAPE = [
	 	[1,1,0,0],
	 	[1,1,0,0]
	 ], (247, 211, 7) # rgb(247, 211, 7)
	T : T_SHAPE = [
	 	[0,1,0,0],
	 	[1,1,1,0]
	 ], (173, 77, 156) # rgb(173, 77, 156)
	S : T_SHAPE = [
	 	[0,1,1,0],
	 	[1,1,0,0]
	 ], (66, 182, 66) # rgb(66, 182, 66) 
	Z : T_SHAPE = [
	 	[1,1,0,0],
	 	[0,1,1,0]
	 ], (239, 33, 41) # rgb(239, 33, 41)
	J : T_SHAPE = [
		[0,0,1,0],
	 	[1,1,1,0]
	 ], (90, 101, 173) # rgb(90, 101, 173)
	L : T_SHAPE = [
	 	[1,0,0,0],
	 	[1,1,1,0]
	 ], (239, 121, 33) # rgb(239, 121, 33)


class Tetris_GUI(Game_GUI):
	def __init__(self, tetris_game):
		super().__init__(tetris_game)
		self.populate_GUI()

	def populate_GUI(self) -> None:
		self.create_containers()
		self.create_lables()
		self.populate_containers()

	def create_containers(self) -> None:
		game_board = Relative_Container(self.game, (100, 100), (255, 255, 255))
		self.containers['game_board'] = game_board


	def create_lables(self) -> None: pass
	def create_buttons(self) -> None: pass
	def populate_containers(self) -> None: pass

class Tetris(Game):
	def __init__(self, app):
		super().__init__(app)
		self.tetris_GUI = Tetris_GUI(self)

	def render(self) -> None:
		self.tetris_GUI.containers['game_board'].render()
		self.app.surface.blit(self.surface, (0,0))
