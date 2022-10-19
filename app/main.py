from game_app import MiniGameApp
from config.app_config import *


'''
TODO: make new screen class. Being able to pick resolution and aspect ratio
	  maybe use upscaling
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
TODO: remove game_data folder. have wordle_data in data folder
	  add assets folder in data
TODO: find logo online for application, add to assets folder
	  update dist.sh scrpit to generate executable with the
	  logo
'''


if __name__ == '__main__': MiniGameApp(S_WIDTH, S_HEIGHT, FULLSCREEN).run()