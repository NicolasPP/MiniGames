import pygame
from time import time


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

  
  
def timer_func(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func




