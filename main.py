import pygame
form app.game_app import MiniGameApp
from app.app_config import *
from app.screen import Screen


screen = Screen(S_WIDTH, S_HEIGHT, FULLSCREEN)
done = False

game_app = MiniGameApp()

screen.display()


while not done:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: done = True
		game_app.parse_event(event)


	game_app.run()	

	pygame.display.flip()
