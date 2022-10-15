from game_app import MiniGameApp
from config.app_config import *


'''
TODO: make system where only the selected game is instanciated
TODO: make sidebar be able to scroll, take any amount of buttons
TODO: Games to add in the future
		- Game of life
		- algorithm visualizer
		- sudoku
		- kakuro
		- boids flocking
		- level generation (maybe)
		- chess
		- galton board (HARD)
TODO: BIG refactor, clean up all classes, remove functions from class.
	  - Game []
	  	- wordle []
	  	- snake []
'''


if __name__ == '__main__': MiniGameApp(S_WIDTH, S_HEIGHT, FULLSCREEN).run()