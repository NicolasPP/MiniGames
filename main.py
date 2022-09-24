from app.game_app import MiniGameApp
from app.app_config import *

if __name__ == '__main__':
	game_app = MiniGameApp(S_WIDTH, S_HEIGHT, FULLSCREEN).run()