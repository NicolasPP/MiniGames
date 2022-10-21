import pygame

class Component:
	def __init__(self, parent, pos, size, alpha, color):
		self.parent = parent
		self.alpha = alpha
		self.rect = pygame.Rect(pos, size)
		self.color = color
		self.offset = parent.rect.topleft
		self.surface = pygame.Surface(size)
		self.processed = False

	def update_pos(self, pos_change): 
		self.rect.topleft = tuple(pygame.math.Vector2(self.rect.topleft) + pos_change)

	def set_size(self, size):
		pos = self.rect.x , self.rect.y
		self.rect = pygame.Rect(pos, size)
		self.surface = pygame.Surface(size)

	def render(self, set_alpha = False):
		self.parent.surface.blit(*self.get_surface_blit(set_alpha = set_alpha))

	def get_surface_blit(self, set_alpha = False):
		if set_alpha: self.surface.set_alpha(self.alpha)
		return self.surface, self.rect