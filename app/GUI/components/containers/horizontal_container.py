from GUI.components.component import Component
from GUI.components.containers.container import Container
from GUI.components.containers.scrollable import Scrollable



class Horizontal_Container(Scrollable, Container):
	def __init__(self, parent, pos, size, alpha, color):
		super().__init__(parent, pos, size, alpha, color) 
