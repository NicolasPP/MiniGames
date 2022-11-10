import pygame
from enum import Enum
from dataclasses import dataclass
from utils.time import timer_func


class MODIFIER(Enum):
	PERCENTAGE : float = 1/100
	RATIO : float = 1


@dataclass
class MOD:
	parent_size : pygame.math.Vector2
	modifier_type : MODIFIER
	ratio : pygame.math.Vector2

def Modifier(*, 
		parent_size : pygame.math.Vector2,
		modifier_type : MODIFIER,
		ratio : float = 0,
		width_ratio : float = 0,
		height_ratio : float = 0) -> MOD:
	'''
		either width and height ratio must be passed in
		or ratio must be passed in
		if both are passed ratio will override the others
		neither can be 0
	'''
	if ratio == 0: assert width_ratio != 0 and height_ratio != 0
	else: width_ratio = height_ratio = ratio

	return MOD(parent_size, modifier_type, pygame.math.Vector2(width_ratio, height_ratio))


def get(modifier : MOD
	) -> tuple[int, int]:
	size = modifier.parent_size.elementwise() * (modifier.modifier_type.value * modifier.ratio)
	return round(size.x), round(size.y)

def get_width(modifier : MOD
	) -> int:
	return modifier.parent_size.x * (modifier.modifier_type.value * modifier.ratio.x)

def get_height(modifier : MOD
	) -> int:
	return modifier.parent_size.y * (modifier.modifier_type.value * modifier.ratio.y)

def get_font_size(max_message_size : tuple[int, int], message : str
	) -> int:
	done = False
	max_font_size = 0
	max_width, max_height = max_message_size
	while not done:
		max_font_size += 1
		font = pygame.font.Font(None, max_font_size)
		message_width, message_height = pygame.font.Font.size(font, message)
		if max_width < message_width or \
			max_height < message_height: done = True
	return max_font_size - 1






def current_screen_size(
	)-> pygame.math.Vector2:
	return pygame.math.Vector2(pygame.display.get_surface().get_size())



