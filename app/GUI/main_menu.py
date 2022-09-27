from app.app_config import *
from games.game import Game
class Main_menu(Game):
	def __init__(self, app):
		super().__init__(app, MAIN_MENU_COLOR)