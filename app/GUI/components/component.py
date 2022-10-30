import pygame


'''
TODO : Change render logic of GUI components so that you have a invalidate fucntion for all components
	   where. when called it cause a rerender of the component.
	   right now everything is being rendered in every frame of the game
'''

class Component:
	def __init__(self, parent, pos, size, alpha, color):
		self.parent = parent
		self.alpha = alpha
		self.processed = False
		self.rect = pygame.rect.Rect(pos, size)
		self.color = (255, 255, 255) if color == (-1,-1,-1) else color
		self.surface = pygame.Surface(size)
		self.show = True
		

	def update_pos(self, pos_change):
		self.rect.topleft = tuple(pygame.math.Vector2(self.rect.topleft) + pos_change)


	def render(self, set_alpha = False):
		if not self.show: return
		self.parent.surface.blit(*self.get_surface_blit(set_alpha = set_alpha))

	def render_dest(self, dest, set_alpha = False):
		if not self.show: return
		dest.blit(*self.get_surface_blit(set_alpha))

	def get_surface_blit(self, set_alpha = False):
		if set_alpha: self.surface.set_alpha(self.alpha)
		return self.surface, self.rect

	def is_hovered(self, mouse_pos):
		return self.rect.collidepoint(mouse_pos)
