from games.game import Game, Game_GUI
from GUI.components.containers import Relative_Container

from typing import TypeAlias
from enum import Enum
from dataclasses import dataclass

class TETRIS_CONFIG:
	def __init__(self):
		self.I_COLOR : tuple[int, int, int] = (50, 199, 239) 	#rgb(50, 199, 239)
		self.O_COLOR : tuple[int, int, int] = (247, 211, 7) 	#rgb(247, 211, 7)
		self.T_COLOR : tuple[int, int, int] = (173, 77, 156) 	#rgb(173, 77, 156)
		self.S_COLOR : tuple[int, int, int] = (66, 182, 66) 	#rgb(66, 182, 66)
		self.Z_COLOR : tuple[int, int, int] = (239, 33, 41) 	#rgb(239, 33, 41)
		self.J_COLOR : tuple[int, int, int] = (90, 101, 173) 	#rgb(90, 101, 173)
		self.L_COLOR : tuple[int, int, int] = (239, 121, 33) 	#rgb(239, 121, 33)
		self.I_SHAPE : list[list[int]] = [[1,1,1,1],[0,0,0,0]]
		self.O_SHAPE : list[list[int]] = [[1,1,0,0],[1,1,0,0]]
		self.T_SHAPE : list[list[int]] = [[0,1,0,0],[1,1,1,0]]
		self.S_SHAPE : list[list[int]] = [[0,1,1,0],[1,1,0,0]]
		self.Z_SHAPE : list[list[int]] = [[1,1,0,0],[0,1,1,0]]
		self.J_SHAPE : list[list[int]] = [[0,0,1,0],[1,1,1,0]]
		self.L_SHAPE : list[list[int]] = [[1,0,0,0],[1,1,1,0]]
CONFIG = TETRIS_CONFIG()


@dataclass
class TETROMINO:
	shape : list[list[int]]
	color : tuple[int, int, int]

class TETROMINOES(Enum):
	I : TETROMINO = TETROMINO(CONFIG.I_SHAPE, CONFIG.I_COLOR)
	O : TETROMINO = TETROMINO(CONFIG.O_SHAPE, CONFIG.O_COLOR)
	T : TETROMINO = TETROMINO(CONFIG.T_SHAPE, CONFIG.T_COLOR)
	S : TETROMINO = TETROMINO(CONFIG.S_SHAPE, CONFIG.S_COLOR) 
	Z : TETROMINO = TETROMINO(CONFIG.Z_SHAPE, CONFIG.Z_COLOR)
	J : TETROMINO = TETROMINO(CONFIG.J_SHAPE, CONFIG.J_COLOR)
	L : TETROMINO = TETROMINO(CONFIG.L_SHAPE, CONFIG.L_COLOR)


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
