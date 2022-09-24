from games.games_config import *
from games.game import Game
from utils.time import regular_interval_tick_wait
import pygame

class Snake(Game):
	def __init__(self, app):
		super().__init__(app)
		self.bg_color = SNAKE_BG
		self.surface.fill(self.bg_color)
		self.paused_surface.fill(self.bg_color)
		self.font = pygame.font.Font(None, 50)
		self.blink = False
		self.display_paused()
		self.blink_delay = 750 #milisecs
		self.grid = []
		self.create_grid()
		self.pause_message_render = self.get_pause_message_render()

	def update(self, dt):
		if self.paused:
			if regular_interval_tick_wait(self.blink_delay):
				self.blink = not self.blink
				self.paused_surface.fill(self.bg_color)
				self.display_paused()

	def display_paused(self):
		if not self.blink: return
		self.paused_surface.blit(*self.pause_message_render)

	def get_pause_message_render(self):
		pause_lable_render = self.font.render("press ' SPACE ' to play", True, "White")
		pause_lable_render.set_alpha(PAUSE_ALPHA)
		s_width, s_height = self.paused_surface.get_size()
		pause_lable_rect = pause_lable_render.get_rect(topleft = (0, 0))
		pause_lable_rect = pause_lable_render.get_rect(topleft = ((s_width // 2) - (pause_lable_rect.width // 2), (s_height // 2) - (pause_lable_rect.height // 2)))
		return pause_lable_render, pause_lable_rect

	def toggle_pause(self):
		self.paused = not self.paused
		self.set_current_surface()

	def create_grid(self):
		for h in range(self.current_surface.get_rect().height):
			row = []
			for w in range(self.current_surface.get_rect().width):
				row.append(pygame.Rect((w * S_CELL_SIZE, h * S_CELL_SIZE),(S_CELL_SIZE, S_CELL_SIZE)))
			self.grid.append(row)

	def update_surface_size(self):
		new_s = self.app.get_game_surface(False)
		new_ps = self.app.get_game_surface(True)
		new_s.fill(self.bg_color)
		new_ps.fill(self.bg_color)
		self.paused_surface = new_ps
		self.surface =  new_s
		self.set_current_surface()
		self.create_grid()
		self.pause_message_render = self.get_pause_message_render()
		self.display_paused()

	def parse_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: self.toggle_pause()
