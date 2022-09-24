from app.app_config import *
from games.game import Game
class Main_menu(Game):
	def __init__(self, app):
		super().__init__(app)
		self.paused = False
		self.bg_color = MAIN_MENU_COLOR
		self.surface.fill(self.bg_color)
		self.set_current_surface()