from game_app import MiniGameApp
from config.app_config import *


'''
TODO: make class for serializing data
TODO: make system where only the selected game is instanciated
TODO: make sidebar be able to scroll, take any amount of buttons
TODO: Games to add in the future
		- Game of life
		- algorithm visualizer
		- sudoku
		- kakuro
		- boids flocking
		- level generation (maybe)
'''


if __name__ == '__main__': MiniGameApp(S_WIDTH, S_HEIGHT, FULLSCREEN).run()