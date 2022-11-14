from GUI.components.containers import Relative_Container
from games.game import Game
from config import *

MAIN_MENU_COLOR : tuple[int, int, int] = COLORS['palette2']['on_primary'] #rgb(63, 78, 79)

class Main_menu(Game):
	def __init__(self, app):
		super().__init__(app, MAIN_MENU_COLOR)
		self.root_container = Relative_Container(self, self.rect.size)