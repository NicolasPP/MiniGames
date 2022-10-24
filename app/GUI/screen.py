import pygame

## when we resize the screen we delete the current surface and get a new one of different size
## this could cause a problem when passing surface as a parameter in class definitions
## this error to be more specific :') -> fatal Python error: (pygame parachute) Segmentation Fault

class Screen:
    pygame.display.init()
    screen_info = pygame.display.Info()
    full_screen_height =  screen_info.current_h
    full_screen_width =  screen_info.current_w

    @staticmethod
    def get_full_screen_size():
        screen_info = pygame.display.Info()
        return screen_info.current_w, screen_info.current_h

    def __init__(self, window_width, window_height, full_screen = True, color = "black"):
        pygame.init()
        self.bg_color = color

        self.windowed_height = window_height
        self.windowed_width = window_width

        self._full_screen = full_screen

        self.surface = pygame.Surface((window_width, window_height))

        self.set_current_dimentions()


    @property
    def full_screen(self): return self._full_screen
    @full_screen.setter
    def full_screen(self, new_full_screen): 
        self._full_screen = new_full_screen
        self.set_current_dimentions()
        self.update_surface()
    @full_screen.deleter
    def full_screen(self): del self._full_screen
    

    def set_current_dimentions(self):
        if self.full_screen:
            self.current_height = Screen.full_screen_height
            self.current_width = Screen.full_screen_width
        else:
            self.current_height = self.windowed_height
            self.current_width = self.windowed_width

    def update_surface(self):
        pygame.display.quit()
        self.display()

    def set_windowed_dimentions(self, new_windowed_width, new_windowed_height):
        self.windowed_width = new_windowed_width
        self.windowed_height = new_windowed_height
    
    def display(self):
        pygame.display.set_mode((self.current_width, self.current_height), pygame.NOFRAME)
        self.surface = pygame.Surface((self.current_width, self.current_height))
        self.surface.fill(self.bg_color)

    def get_current_size(self): return self.current_width, self.current_height
    
    def render(self):
        content_surface = self.surface      
        pygame.display.get_surface().blit(content_surface, (0,0))

    def toggle_full_screen(self):
        self.full_screen = not self.full_screen