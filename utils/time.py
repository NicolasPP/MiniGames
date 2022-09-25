import pygame
regular_interval = pygame.time.get_ticks()

def regular_interval_tick_wait(time):
    global regular_interval
    now = pygame.time.get_ticks()
    if now - regular_interval >= time:
        regular_interval = now
        return True
    return False


class Time_Man:
    def __init__(self):
        self.waited_time = 0

    def dt_wait(self, dt, time):
        if self.waited_time >= time / 1000:
            self.waited_time = 0
            return True
        self.waited_time += dt




