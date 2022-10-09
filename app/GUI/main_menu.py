from config.app_config import *
from games.game import Game

'''
TODO : add user's stats
	- Snake
		- max score in snake
		- amount of games played
	- Wordle
		- amount of words guessed right
		- amount og words guessed wrong
		- little screenshot / smaller version of board of best game (game with smallest amount of moves)
	- Tictactoe
		- player One games won
		- player Two games won
	- sudoku
		- games solved
		- fastest game solved
		- animation of fastest game solved
	- kakuro
		- games solved
		- fastest game solved
		- animation of fastest game solved
'''

class Main_menu(Game):
	def __init__(self, app):
		super().__init__(app, MAIN_MENU_COLOR)