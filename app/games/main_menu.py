from config.app_config import *
from GUI.components.containers import Relative_Container
from games.game import Game

class Main_menu(Game):
	def __init__(self, app):
		super().__init__(app, MAIN_MENU_COLOR)
		self.root_container = Relative_Container(self, self.rect.size)