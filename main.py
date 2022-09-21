import pygame
from app_config import *
from screen import Screen





screen = Screen(S_WIDTH, S_HEIGHT, FULLSCREEN)
done = False


screen.display()


while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	pygame.display.flip()
