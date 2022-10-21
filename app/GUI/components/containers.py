from GUI.components.component import Component
import config.games_config as gcfg
import config.app_config as acfg
from enum import Enum
from functools import partial
import pygame 
from dataclasses import dataclass

@dataclass
class Padding:
	top : int = acfg.PADDING
	bottom : int = acfg.PADDING
	right : int = acfg.PADDING
	left : int = acfg.PADDING
	spacing : int = acfg.PADDING


class Container(Component):
	def __init__(self,\
				 parent,\
				 pos,\
				 color,\
				 plane,\
				 size = (0,0),\
				 alpha = gcfg.NORMAL_ALPHA,\
				 padding = Padding()): 
		super().__init__(parent, pos, size, alpha, color)
		self.plane = plane
		self.padding = padding
		self.components = []
		

	def add_component(self, component): self.plane.value(self, component)
	
	def render(self, set_alpha = False):
		self.parent.surface.blit(*self.get_surface_blit(set_alpha))
		for comp in self.components: comp.render()



class Scrollable_Container(Container):
	def __init__(self, parent, pos, color, plane):
		super().__init__(parent, pos, size, alpha, color, plane)




def add_horizontal_component(container, component):
	container.components.append(component)

	height = 0
	width = 0

	height += container.padding.top
	width += container.padding.left

	last = container.components[-1]
	


	for comp in container.components:
		if not comp.processed: 
			comp.update_pos(pygame.math.Vector2(width, height))
			comp.processed = True
		width += comp.rect.width
		width += container.padding.spacing

	height += get_largest_height(container.components)
	height += container.padding.bottom
	width += container.padding.right 

	container.set_size((width, height))





def add_vertical_component(container, component):
	container.components.append(component)



def get_largest_height(components):
	components.sort(key = lambda x : x.rect.h)
	return components[-1].rect.h

def get_largest_width(components):
	components.sort(key = lambda x : x.rect.w)
	return components[-1].rect.w

class LAYOUT_PLANE(Enum):
	HORIZONTAL = partial(add_horizontal_component)
	VERTICAL = partial(add_vertical_component)
