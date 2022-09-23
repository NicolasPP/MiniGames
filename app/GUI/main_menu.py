from app.app_config import * 
class Main_menu:
	def __init__(self, app):
		self.app = app
		self.surface = self.get_surface()

	def update_surface_size(self):
		self.surface = self.get_surface()

	def get_surface(self):
		s = self.app.get_game_surface()
		s.fill(MAIN_MENU_COLOR)
		return s