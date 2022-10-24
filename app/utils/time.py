import pygame
regular_interval = pygame.time.get_ticks()

class Time_Man:
    def __init__(self):
        self.waited_time : float = 0

    def dt_wait(self, dt : float, time : float) -> bool:
        if self.waited_time >= time / 1000:
            self.waited_time = 0
            return True
        self.waited_time += dt
        return False




