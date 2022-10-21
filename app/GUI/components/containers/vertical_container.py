from GUI.components.containers.container import Container
from GUI.components.containers.scrollable import Scrollable


class Vertical_Container(Scrollable, Container):
	def __init__(self, parent, pos, size, alpha, color): 
		super().__init__(parent, pos, size, alpha, color)