from app.app_config import * 
class Main_menu:
	def __init__(self, surface):
		self.surface = surface
		self.surface.fill(MAIN_MENU_COLOR)