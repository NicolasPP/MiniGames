from GUI.components.component import Component
from config.games_config import * 
from enum import Enum

class LAYOUT_PLANE(Enum):
	HORIZONTAL = 1
	VERTICAL = 2

class Container(Component):
	def __init__(self, parent, pos, color, plane, size = (0,0), alpha = NORMAL_ALPHA): 
		super().__init__(parent, pos, size, alpha, color)
		self.plane = plane
		self.components = []
		

	def add_component(self, component):
		self.components.append(component)



class Scrollable_Container(Container):
	def __init__(self, parent, pos, color, plane):
		super().__init__(parent, pos, size, alpha, color, plane)
