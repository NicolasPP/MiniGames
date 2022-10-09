from game_app import MiniGameApp
from config.app_config import *


'''
TODO: make system where only the selected game is instanciated
TODO: make sidebar be able to scroll, take any amount of buttons
TODO: make class for drawing letter on the screen
	  right now evrything is too hard coded. pretty sure
	  could write one function to complete all functionality needed
TODO: add click library, add option to run without pyenchat.
	  couldnt find any dictionaries when using pyenchant on windows
TODO: Games to add in the future
		- Game of life
		- algorithm visualizer
		- sudoku
		- kakuro
		- boids flocking
		- level generation (maybe)
'''


if __name__ == '__main__': MiniGameApp(S_WIDTH, S_HEIGHT, FULLSCREEN).run()