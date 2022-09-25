from games.games_config import *
from games.game import Game
from utils.time import regular_interval_tick_wait
import pygame
from random import choice


class SNAKE:
	def __init__(self, rect, sidebar_offset):
		self.rect = rect
		self.size = 1
		self.body = [self.rect]
		self.sidebar_offset = sidebar_offset

	def render(self, grid_surface):
		for bdy in self.body: pygame.draw.rect(grid_surface, "Black", bdy)

	def update(self, dt): 
		mx, my = pygame.mouse.get_pos()
		ox, oy = self.sidebar_offset
		self.rect.topleft = (mx - ox, my - oy)

	def add(self, rect):
		self.body.append(rect)
		body_size = len(self.body)
		if body_size + 1 > self.size: self.body = self.body[1:body_size]
		

	def collide_cells(self, cells):
		for cell in cells:
			if cell.collidepoint(self.rect.center):
				if cell not in self.body: self.add(cell)

	


class Snake(Game):
	def __init__(self, app):
		super().__init__(app)
		self.bg_color = SNAKE_BG
		self.surface.fill(self.bg_color)
		self.paused_surface.fill(self.bg_color)
		self.font = pygame.font.Font(None, 50)
		self.blink = False
		self.display_paused()
		self.blink_delay = 650 #milisecs
		self.grid = []
		self.cells = []
		self.fruits = []
		self.create_grid()
		self.pause_message_render = self.get_pause_message_render()
		self.paused_surface.set_alpha(5)
		self.snake = SNAKE(choice(self.cells), self.sidebar_offset)

	def update(self, dt):
		if self.paused: pass
		else:
			self.snake.update(dt)
			self.snake.collide_cells(self.cells)
			self.collide_fruits()
			self.spawn_fruit()

	def render(self, parent_surface):
		for fruit in self.fruits: pygame.draw.rect(self.surface, "Green", fruit)
		self.snake.render(self.surface)
		parent_surface.blit(self.surface, self.app.get_gs_position())
		

	def grid_test(self):
		for row in self.grid:
			for cell in row:
				mp = pygame.mouse.get_pos()
				x, y = mp[0] - self.sidebar_offset[0], mp[1] - self.sidebar_offset[1]
				if cell.collidepoint((x, y)):
					pygame.draw.rect(self.current_surface, "Black", cell)

	def display_paused(self):
		self.paused_surface.fill(self.bg_color)
		if not self.blink: return
		self.paused_surface.blit(*self.pause_message_render)

	def get_pause_message_render(self):
		pause_lable_render = self.font.render("press ' SPACE ' to play", True, "White")
		s_width, s_height = self.paused_surface.get_size()
		pause_lable_rect = pause_lable_render.get_rect(topleft = (0, 0))
		pause_lable_rect = pause_lable_render.get_rect(topleft = ((s_width // 2) - (pause_lable_rect.width // 2), (s_height // 2) - (pause_lable_rect.height // 2)))
		return pause_lable_render, pause_lable_rect

	def toggle_pause(self):
		self.paused = not self.paused
		self.set_current_surface()


	def collide_fruits(self):
		collided = []
		for fruit in self.fruits:
			if fruit.collidepoint(self.snake.rect.center):
				self.snake.size += 1
				collided.append(fruit)
		for fruit in collided: self.fruits.remove(fruit)


	def create_grid(self):
		for h in range(self.current_surface.get_rect().height // S_CELL_SIZE):
			row = []
			for w in range(self.current_surface.get_rect().width // S_CELL_SIZE):
				cell = pygame.Rect((w * S_CELL_SIZE, h * S_CELL_SIZE),(S_CELL_SIZE, S_CELL_SIZE))
				row.append(cell)
				self.cells.append(cell)
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

	def spawn_fruit(self):
		t = 3000
		if regular_interval_tick_wait(t):
			fruit = choice(self.cells)
			while not self.is_valid_fruit_pos(fruit): fruit =choice(self.cells)
			self.fruits.append(fruit)

	def is_valid_fruit_pos(self, fruit):
		return fruit not in self.snake.body and \
					fruit not in self.fruits

	def parse_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: self.toggle_pause()





