from GUI.components.component import Component
from GUI.components.lable import Lable
from GUI.components.button import Button

import config.games_config as gcfg
import config.app_config as acfg
from enum import Enum
import pygame 
from dataclasses import dataclass

from typing import Callable, Any


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
	LEFT : int = 1
	MIDDLE : int = 2
	RIGHT : int = 3
	SCROLL_UP : int = 4
	SCROLL_DOWN : int = 5

class LAYOUT_PLANE(Enum):
	HORIZONTAL : int = 0
	VERTICAL : int = 1
	RELATIVE  : int = 2

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
	def __init__(self,
				 parent,
				 plane : LAYOUT_PLANE,
				 color : tuple[int, int, int],
				 pos : tuple[int, int] = (0,0),
				 size : tuple[int, int]= (0,0),
				 alpha : float = gcfg.NORMAL_ALPHA,
				 root : bool = False,
				 padding : Padding = Padding()): 
		super().__init__(parent, pos, size, alpha, color)
		self.plane = plane
		self.padding = padding
		
		self.components : list[Component] = []
		self.root = root
		self.conpensate_padding : bool = True
		self.fixed_size : bool = False if size == (0,0) else True
		self.process : dict[LAYOUT_PLANE , Callable] = {
		LAYOUT_PLANE.VERTICAL : self.vertical_process,
		LAYOUT_PLANE.HORIZONTAL : self.horizontal_process
		}

	def add_component(self, component : Component, pos : tuple[int, int] = (0,0) ) -> None:
		component.update_pos(pos)
		self.components.append(component)	
		if self.plane is LAYOUT_PLANE.RELATIVE: return

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

	def get_container_offset(self) -> pygame.math.Vector2:
		if self.root: return pygame.math.Vector2(self.rect.topleft)
		return pygame.math.Vector2(self.rect.topleft) + self.parent.get_container_offset()


	def set_size(self, size : tuple[int, int]) -> None:
		pos = self.rect.x , self.rect.y
		self.rect = pygame.Rect(pos, size)
		self.surface = pygame.Surface(size)
		self.surface.fill(self.color)

	def container_click(self, mouse_pos : tuple[int, int], event : pygame.event.Event, app : Any) -> None:
		if event.type != pygame.MOUSEBUTTONDOWN: return
		if event.button != MOUSECLICK.LEFT: return
		for comp in self.components:
			if isinstance(comp, Container): continue
			if isinstance(comp, Lable): continue
			mouse_p = pygame.math.Vector2(mouse_pos).elementwise()
			offset = pygame.math.Vector2(self.get_container_offset())
			if comp.is_hovered(mouse_p - offset) and \
				isinstance(comp, Button):
				comp.click(app, comp)

	def render(self, set_alpha : bool = False) -> None:
		self.surface.fill(self.color)
		for comp in self.components: comp.render()
		self.parent.surface.blit(*self.get_surface_blit(set_alpha))		

	def process_components(self, width : int, height : int) -> tuple[int, int]:
		for comp in self.components:
			if not comp.processed:
				comp.update_pos((width, height))
				comp.processed = True
			width, height = self.process[self.plane](comp, width, height)
		if not self.fixed_size: width, height = self.set_fixed_dimension(width, height)
		return width, height

	def set_fixed_dimension(self, width : int, height : int) -> tuple[int, int]:
		if self.plane is LAYOUT_PLANE.HORIZONTAL: height += get_largest_height(self.components)
		elif self.plane is LAYOUT_PLANE.VERTICAL: width += get_largest_width(self.components)
		return width, height
	
	def horizontal_process(self, component : Component, width : int, height : int) -> tuple[int, int]: 
		width += component.rect.width
		if self.components[-1]!= component:
			width += self.padding.spacing
		return width, height

	def vertical_process(self, component : Component, width : int, height : int) -> tuple[int, int]: 
		height += component.rect.height
		if self.components[-1]!= component:
			height += self.padding.spacing 
		return width, height

	def parse_event(self, event : pygame.event.Event, root_parent : Any) -> None:
		mouse_pos = pygame.mouse.get_pos()
		for comp in self.components:
			if isinstance(comp, Container):
				comp.parse_event(event, root_parent)
		self.container_click(mouse_pos, event, root_parent)


class Linear_Container(Container):
	def __init__(self,
				 parent : Any,
				 plane : LAYOUT_PLANE,
				 color : tuple[int, int ,int],
				 pos : tuple[int, int] = (0,0),
				 size : tuple[int, int] = (0,0),
				 alpha : float = gcfg.NORMAL_ALPHA,
				 root  : bool = False,
				 padding : Padding = Padding()): 
		super().__init__(parent, plane, color, pos = pos, size = size, alpha = alpha, root = root, padding = padding)


class Scrollable_Container(Container):
	def __init__(self, 
				 parent : Any,
				 plane : LAYOUT_PLANE,
				 color : tuple[int, int, int],
				 pos : tuple[int, int] = (0,0),
				 size : tuple[int, int] = (0,0),
				 alpha : float = gcfg.NORMAL_ALPHA,
				 root : bool = False,
				 padding : Padding = Padding()):
		super().__init__(parent, plane, color, pos, size, alpha, root, padding)
		self.scroll_speed = pygame.math.Vector2(0,10)

	def move_up(self) -> None:
		self.surface.fill(self.color)
		last_comp_pos = self.components[-1].rect.bottom
		if last_comp_pos + self.rect.y <= self.rect.bottom : return
		speed = self.scroll_speed * -1
		for comp in self.components: comp.update_pos((int(round(speed.x)), int(round(speed.y))))
		

	def move_down(self) -> None:
		self.surface.fill(self.color)
		first_comp_pos = self.components[0].rect.y
		if first_comp_pos >= 0: return
		for comp in self.components: comp.update_pos((int(round(self.scroll_speed.x)), int(round(self.scroll_speed.y))))



	def parse_event(self, event : pygame.event.Event, root_parent : Any) -> None:
		mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
		offset = pygame.math.Vector2(self.parent.get_container_offset())
		if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered(mouse_pos - offset):
			if event.button == MOUSECLICK.SCROLL_UP: self.move_down()#self.scroll_offset = self.scroll_speed
			if event.button == MOUSECLICK.SCROLL_DOWN : self.move_up()#self.scroll_offset = self.scroll_speed * -1
			self.container_click(pygame.mouse.get_pos(), event, root_parent)
'''
NOT GOOD FOR NESTING WITH OTHER CONTAINERS
'''
class Relative_Container(Container):
	def __init__(self, 
				 parent : Any,
				 size : tuple[int, int],
				 color: tuple[int, int, int] = (-1, -1 ,-1),
				 pos : tuple[int, int] = (0,0),
				 alpha : float = gcfg.NORMAL_ALPHA,
				 root : bool = False,
				 padding : Padding = Padding()):
		
		super().__init__(parent, LAYOUT_PLANE.RELATIVE,color, pos, size, alpha, root, padding)

	def render(self, set_alpha : bool = False) -> None:
		for comp in self.components: comp.render(set_alpha = set_alpha)
		self.parent.surface.blit(*self.get_surface_blit(set_alpha))	



def get_largest_height(components : list[Component]) -> int:
	components.sort(key = lambda x : x.rect.h)
	return components[-1].rect.h

def get_largest_width(components : list[Component]) -> int:
	components.sort(key = lambda x : x.rect.w)
	return components[-1].rect.w
