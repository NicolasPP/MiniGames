from GUI.components.component import Component
from enum import Enum

class LAYOUT_PLANE(Enum):
	HORIZONTAL = 1
	VERTICAL = 2

class Container(Component):
	def __init__(self, parent, pos, size, alpha, color, plane): 
		super().__init__(parent, pos, size, alpha, color)
		self.plane = plane


class Scrollable_Container(Container):
	def __init__(self, parent, pos, size, alpha, color, plane):
		super().__init__(parent, pos, size, alpha, color, plane)
