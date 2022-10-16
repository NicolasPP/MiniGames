import pygame

## when we resize the screen we delete the current surface and get a new one of different size
## this could cause a problem when passing surface as a parameter in class definitions
## this error to be more specific :') -> fatal Python error: (pygame parachute) Segmentation Fault

class Screen:
    pygame.display.init()
    screen_info = pygame.display.Info()
    full_screen_height = screen_info.current_h
    full_screen_width = screen_info.current_w

    def __init__(self, window_width, window_height, full_screen = True, color = "black"):
        pygame.init()
        self.bg_color = color
        self.full_screen = full_screen
        self.windowed_height = window_height
        self.windowed_width = window_width
        self.set_current_dimentions()
    
    def set_current_dimentions(self):
        if self.full_screen:
            self.current_height = Screen.full_screen_height
            self.current_width = Screen.full_screen_width
        else:
            self.current_height = self.windowed_height
            self.current_width = self.windowed_width
    
    def set_windowed_dimentions(self, new_windowed_height, new_windowed_width):
        self.windowed_height = new_windowed_height
        self.windowed_width = new_windowed_width

    def display(self):
        surface = pygame.display.set_mode((self.current_width, self.current_height), pygame.NOFRAME)
        surface.fill(self.bg_color)
        self.surface = surface

    
    def toggle_full_screen(self):
        pygame.display.quit()
        self.full_screen = not self.full_screen
        self.set_current_dimentions()
        self.display()
        