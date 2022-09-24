import pygame
regular_interval = pygame.time.get_ticks()

def regular_interval_tick_wait(time):
    global regular_interval
    now = pygame.time.get_ticks()
    if now - regular_interval >= time:
        regular_interval = now
        return True
    return False