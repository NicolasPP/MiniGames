import pygame
from app.game_app import MiniGameApp
from app.app_config import *


game_app = MiniGameApp(S_WIDTH, S_HEIGHT, FULLSCREEN)


while game_app.running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: done = True
		game_app.parse_event(event)


	game_app.run()	

	pygame.display.flip()
pygame.quit()