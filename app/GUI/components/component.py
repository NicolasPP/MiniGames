import pygame


class Component:
	def __init__(self, parent, pos : tuple[int, int], size : tuple[int, int], alpha : float, color : tuple[int, int, int]):
		self.parent = parent
		self.alpha : float = alpha
		self.processed : bool = False
		self.rect  : pygame.rect.Rect = pygame.rect.Rect(pos, size)
		self.color = (255, 255, 255) if color == (-1,-1,-1) else color
		self.surface : pygame.Surface | pygame.surface.Surface = pygame.Surface(size)
		self.show : bool = True
		self.surface.set_alpha(int(round(self.alpha)))
		

	def update_pos(self, pos_change : tuple[int, int]) -> None:
		new_pos = pygame.math.Vector2(self.rect.topleft) + pygame.math.Vector2(pos_change)
		self.rect.topleft = int(round(new_pos.x)), int(round(new_pos.y))


	def render(self, set_alpha : bool = False) -> None:
		if not self.show: return
		self.parent.surface.blit(*self.get_surface_blit(set_alpha = set_alpha))

	def render_dest(self, dest : pygame.Surface, set_alpha : bool = False):
		if not self.show: return
		dest.blit(*self.get_surface_blit(set_alpha))

	def get_surface_blit(self, set_alpha : bool = False) -> tuple[pygame.Surface | pygame.surface.Surface, pygame.rect.Rect]:
		if set_alpha: self.surface.set_alpha(int(round(self.alpha)))
		return self.surface, self.rect

	def is_hovered(self, mouse_pos : pygame.math.Vector2) -> bool:
		return self.rect.collidepoint(mouse_pos.x, mouse_pos.y)
