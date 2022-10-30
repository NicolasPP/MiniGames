from GUI.components.component import Component
from GUI.components.lable import Lable

import config.games_config as gcfg
import config.app_config as acfg
from enum import Enum
import pygame 
from dataclasses import dataclass


'''
TODO : fix padding logic
	   make nicer looking
TODO : move process logic where we update padding depending on orientation
	   to padding class
TODO : container_click function will recognise a click and call click() on all its children 
	   this will break when adding lables to Containers. Either add isinstance check to see if its a button
	   or add click() to component class
'''

class MOUSECLICK:
	LEFT = 1
	MIDDLE = 2
	RIGHT = 3
	SCROLL_UP = 4
	SCROLL_DOWN = 5

class LAYOUT_PLANE(Enum):
	HORIZONTAL = 0
	VERTICAL = 1
	RELATIVE  = 2

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

	def __init__(self,
				 parent,
				 plane,
				 color,
				 pos = (0,0),
				 size = (0,0),
				 alpha = gcfg.NORMAL_ALPHA,
				 root = False,
				 padding = Padding()): 
		super().__init__(parent, pos, size, alpha, color)
		self.plane = plane
		self.padding = padding
		self.components = []
		self.root = root
		self.conpensate_padding = True
		self.fixed_size = False if size == (0,0) else True
		self.process = {
		LAYOUT_PLANE.VERTICAL : self.vertical_process,
		LAYOUT_PLANE.HORIZONTAL : self.horizontal_process
		}
	def add_game(self, game):
		last_width = get_largest_width(self.components)
		game_component = Component(self, (0,0), game.surface.get_rect().size, 255, game.color)
		self.add_component(game_component)
		return game_component

	def add_component(self, component):
		self.components.append(component)		
		height = 0
		width = 0
		#------------------
		height += self.padding.top
		width += self.padding.left
		if isinstance(component, Container):
			if self.conpensate_padding:
				height -= component.padding.top
				width -= component.padding.left
		#------------------	
		width, height = self.process_components(width, height)
		#------------------
		height += self.padding.bottom
		width += self.padding.right
		if isinstance(component, Container):
			if self.conpensate_padding:
				height -= component.padding.bottom
				width -= component.padding.right
		#------------------
		if not self.fixed_size: self.set_size((width, height))


	def set_size(self, size):
		pos = self.rect.x , self.rect.y
		self.rect = pygame.Rect(pos, size)
		self.surface = pygame.Surface(size)
		self.surface.fill(self.color)

	def container_click(self, mouse_pos, event, app):
		if event.type != pygame.MOUSEBUTTONDOWN: return
		if event.button != MOUSECLICK.LEFT: return
		for comp in self.components:
			if isinstance(comp, Container): continue
			if isinstance(comp, Lable): continue
			mouse_p = pygame.math.Vector2(mouse_pos)
			offset = Container.get_container_offset(self)
			if comp.is_hovered(mouse_p - offset):
				comp.click(app, comp)

	def render(self, set_alpha = False):
		self.surface.fill(self.color)
		for comp in self.components: comp.render()
		self.parent.surface.blit(*self.get_surface_blit(set_alpha))		

	def process_components(self, width, height):
		for comp in self.components:
			if not comp.processed:
				comp.update_pos(pygame.math.Vector2(width, height))
				comp.processed = True
			width, height = self.process[self.plane](comp, width, height)
		if not self.fixed_size: width, height = self.set_fixed_dimension(width, height)
		return width, height

	def set_fixed_dimension(self, width, height):
		if self.plane is LAYOUT_PLANE.HORIZONTAL: height += get_largest_height(self.components)
		elif self.plane is LAYOUT_PLANE.VERTICAL: width += get_largest_width(self.components)
		return width, height
	
	def horizontal_process(self, component, width, height): 
		width += component.rect.width
		if self.components[-1]!= component:
			width += self.padding.spacing
		return width, height

	def vertical_process(self, component, width, height): 
		height += component.rect.height
		if self.components[-1]!= component:
			height += self.padding.spacing 
		return width, height

	def parse_event(self, event, root_parent):
		mouse_pos = pygame.mouse.get_pos()
		for comp in self.components:
			if isinstance(comp, Container):
				comp.parse_event(event, root_parent)
		self.container_click(mouse_pos, event, root_parent)


class Linear_Container(Container):
	def __init__(self,
				 parent,
				 plane,
				 color,
				 pos = (0,0),
				 size = (0,0),
				 alpha = gcfg.NORMAL_ALPHA,
				 root = False,
				 padding = Padding()): 
		super().__init__(parent, plane, color, pos = pos, size = size, alpha = alpha, root = root, padding = padding)
		self.plane = plane
		self.padding = padding
		self.components = []
		self.root = root
		self.conpensate_padding = True
		self.fixed_size = False if size == (0,0) else True
		self.process = {
		LAYOUT_PLANE.VERTICAL : self.vertical_process,
		LAYOUT_PLANE.HORIZONTAL : self.horizontal_process
		}


class Scrollable_Container(Container):
	def __init__(self, 
				 parent,
				 plane,
				 color,
				 pos = (0,0),
				 size = (0,0),
				 alpha = gcfg.NORMAL_ALPHA,
				 root = False,
				 padding = Padding()):
		super().__init__(parent, plane, color, pos, size, alpha, root, padding)


	def move_up(self):
		self.surface.fill(self.color)
		last_comp_pos = self.components[-1].rect.bottom
		if last_comp_pos + self.rect.y <= self.rect.bottom : return
		for comp in self.components: comp.update_pos(self.scroll_speed * -1)
		

	def move_down(self):
		self.surface.fill(self.color)
		first_comp_pos = self.components[0].rect.y
		if first_comp_pos >= 0: return
		for comp in self.components: comp.update_pos(self.scroll_speed)



	def parse_event(self, event, root_parent):
		mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
		offset = pygame.math.Vector2(Container.get_container_offset(self.parent))
		if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered(mouse_pos - offset):
			if event.button == MOUSECLICK.SCROLL_UP: self.move_down()#self.scroll_offset = self.scroll_speed
			if event.button == MOUSECLICK.SCROLL_DOWN : self.move_up()#self.scroll_offset = self.scroll_speed * -1
			self.container_click(pygame.mouse.get_pos(), event, root_parent)
'''
NOT GOOD FOR NESTING WITH OTHER CONTAINERS
'''
class Relative_Container(Container):
	def __init__(self, 
				 parent,
				 size,
				 color = (-1, -1 ,-1),
				 pos = (0,0),
				 alpha = gcfg.NORMAL_ALPHA,
				 root = False,
				 padding = Padding()):
		
		super().__init__(parent, LAYOUT_PLANE.RELATIVE,color, pos, size, alpha, root, padding)

	def add_component(self, component, pos):
		component.update_pos(pos)
		self.components.append(component)


	def render(self, set_alpha = False):
		for comp in self.components: comp.render(set_alpha = set_alpha)
		self.parent.surface.blit(*self.get_surface_blit(set_alpha))	



def get_largest_height(components):
	components.sort(key = lambda x : x.rect.h)
	return components[-1].rect.h

def get_largest_width(components):
	components.sort(key = lambda x : x.rect.w)
	return components[-1].rect.w
