import pygame


class Lable:
	def __init__(self, pos, message, font_size, color, font = False, r_topleft = False ):
		self.pos = pos
		self.message = message
		self.font = font if font else pygame.font.Font(None, font_size)
		self.color = color
		self.r_topleft = r_topleft # default is center


	def get_lable_blit(self):
		message_render = self.font.render(self.message, True, self.color)
		message_rect = message_render.get_rect(center = self.pos)
		if self.r_topleft: message_rect = message_render.get_rect(topleft = self.pos)
		return message_render, message_rect


'''
Wordle - get_center_message_render -> render message in the center of the screen
'''