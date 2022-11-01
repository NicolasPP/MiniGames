from game_app import Minigames
from config.app_config import *


'''
TODO: make system where only the selected game is instanciated
TODO: Games to add in the future
		- Game of life
		- algorithm visualizer
		- sudoku
		- kakuro
		- boids flocking
		- level generation (maybe)
		- chess
		- galton board (HARD)
		- tetris
TODO: find logo online for application, add to assets folder
	  update dist.sh scrpit to generate executable with the
	  logo
TODO: some things are still not type hinted, most parents or root_parents are just Any
'''


if __name__ == '__main__': Minigames(S_WIDTH, S_HEIGHT, FULLSCREEN).run()