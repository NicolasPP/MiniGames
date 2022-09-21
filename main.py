import pygame
from app.game_app import MiniGameApp
from app.app_config import *



done = False
game_app = MiniGameApp(S_WIDTH, S_HEIGHT, FULLSCREEN)


while not done:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: done = True
		game_app.parse_event(event)


	game_app.run()	

	pygame.display.flip()
