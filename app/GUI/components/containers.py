from GUI.components.component import Component
import config.games_config as gcfg
import config.app_config as acfg
from enum import Enum
import pygame 
from dataclasses import dataclass


'''
TODO : fix padding logic
	   make nicer looking
'''

class LAYOUT_PLANE(Enum):
	HORIZONTAL = 0
	VERTICAL = 1

@dataclass
class Padding:
	top : int = acfg.PADDING
	bottom : int = acfg.PADDING
	right : int = acfg.PADDING
	left : int = acfg.PADDING
	spacing : int = acfg.PADDING

	def __sub__(self, other):
		top = abs(self.top - other.top)
		bottom = abs(self.bottom - other.bottom)
		right = abs(self.right - other.right)
		left = abs(self.left - other.left)
		spacing = self.spacing
		return Padding(top, bottom, right, left, spacing)
	

class Container(Component):
	@staticmethod
	def get_container_offset(container):
		if container.root: return pygame.math.Vector2(container.rect.topleft)
		return pygame.math.Vector2(container.rect.topleft) + Container.get_container_offset(container.parent)

	def __init__(self,\
				 parent,\
				 color,\
				 plane,\
				 pos = (0,0),\
				 size = (0,0),\
				 alpha = gcfg.NORMAL_ALPHA,\
				 root = False,\
				 padding = Padding()): 
		super().__init__(parent, pos, size, alpha, color)
		self.plane = plane
		self.padding = padding
		self.components = []
		self.root = root
		self.process = {
		LAYOUT_PLANE.VERTICAL : self.vertical_process,
		LAYOUT_PLANE.HORIZONTAL : self.horizontal_process
		}

	def add_component(self, component):
		self.components.append(component)
		
		
		height = 0
		width = 0
		#------------------
		height += self.padding.top
		width += self.padding.left
		if isinstance(component, Container):
			height -= component.padding.top
			width -= component.padding.left

		# print(width, height, '  left, top')
		#------------------	
		width, height = self.process_components(width, height)
		# print(width, height, '  process')
		#------------------
		height += self.padding.bottom
		width += self.padding.right
		if isinstance(component, Container):
			height -= component.padding.bottom
			width -= component.padding.right
		# print(width, height, '  right, bottom ')
		#------------------
		self.set_size((width, height))
		# self.processed = True

	def container_click(self, mouse_pos, app):
		for comp in self.components:
			if isinstance(comp, Container): comp.container_click(mouse_pos, app)
			else:
				m = pygame.math.Vector2(mouse_pos)
				offset = Container.get_container_offset(self)
				if comp.is_clicked(m - offset):
					comp.click(app, comp)
	
	def render(self, set_alpha = False):
		for comp in self.components: comp.render()
		self.parent.surface.blit(*self.get_surface_blit(set_alpha))		

	def process_components(self, width, height):
		for comp in self.components:
			if not comp.processed:
				comp.update_pos(pygame.math.Vector2(width, height))
				comp.processed = True
			
			width, height = self.process[self.plane](comp, width, height)
		width, height = self.set_fixed_dimension(width, height)
		return width, height

	def set_fixed_dimension(self, width, height):
		if self.plane is LAYOUT_PLANE.HORIZONTAL: height += get_largest_height(self.components)
		elif self.plane is LAYOUT_PLANE.VERTICAL: width += get_largest_width(self.components)
		return width, height
	
	def horizontal_process(self, component, width, height): 
		width += component.rect.width
		if self.components[-1]!= component: 
			width += self.padding.spacing
			if isinstance(component, Container):
				if self.plane is component.plane: width -= component.padding.bottom
				else: width -= component.padding.spacing 

		return width, height

	def vertical_process(self, component, width, height): 
		height += component.rect.height
		if self.components[-1]!= component:
			height += self.padding.spacing
			if isinstance(component, Container):
				if self.plane is component.plane: height -= component.padding.left
				else: height -= component.padding.spacing 
		return width, height


class Scrollable_Container(Container):
	def __init__(self, parent, pos, color, plane):
		super().__init__(parent, pos, size, alpha, color, plane)


def get_largest_height(components):
	components.sort(key = lambda x : x.rect.h)
	return components[-1].rect.h

def get_largest_width(components):
	components.sort(key = lambda x : x.rect.w)
	return components[-1].rect.w
