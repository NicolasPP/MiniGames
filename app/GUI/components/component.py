import pygame


class Component:
	def __init__(self, parent, pos, size, alpha, color):
		self.parent = parent
		self.alpha = alpha
		self.processed = False
		self.rect = pygame.Rect(pos, size)
		self.color = color
		self.surface = pygame.Surface(size)
		self.surface.fill(self.color)
		

	def update_pos(self, pos_change):
		self.rect.topleft = tuple(pygame.math.Vector2(self.rect.topleft) + pos_change)


	def set_size(self, size):
		pos = self.rect.x , self.rect.y
		self.rect = pygame.Rect(pos, size)
		self.surface = pygame.Surface(size)
		self.surface.fill(self.color)

	def render(self, set_alpha = False):
		self.parent.surface.blit(*self.get_surface_blit(set_alpha = set_alpha))

	def get_surface_blit(self, set_alpha = False):
		if set_alpha: self.surface.set_alpha(self.alpha)
		return self.surface, self.rect

	def is_clicked(self, mouse_pos):
		return self.rect.collidepoint(mouse_pos)
