from games.games_config import *
from games.game import Game
import pygame
from random import choice
from enum import Enum
from utils.time import Time_Man


class SNAKE:
	def __init__(self, rect, sidebar_offset):
		self.rect = rect
		self.rect.width -= 1
		self.rect.height -= 1
		self.size = 15
		self.body = []
		self.sidebar_offset = sidebar_offset
		self.direction_input = {
			"UP" : (0, -1),
			"DOWN" : (0 ,1),
			"RIGHT" : (1,0),
			"LEFT" : (-1, 0)
		}
		self.timer = Time_Man()
		self.direction = choice(list(self.direction_input.values()))
		self.speed = S_CELL_SIZE * 10
		self.move_distance = 0
		self.x = rect.x
		self.y = rect.y
		self.alive = True


	def render(self, grid_surface):
		for bdy in self.body: pygame.draw.rect(grid_surface, S_COLOR, bdy)
		pygame.draw.rect(grid_surface, S_COLOR, self.rect)


	def update(self, dt):# snake not bound to the board
		self.check_collision()
		self.set_move_distance(dt)
		self.move(dt)


	def set_move_distance(self, dt):
		if self.timer.dt_wait(dt, SNAKE_MOVE_FREQ):
			self.move_distance += S_CELL_SIZE
			prev_rec = self.rect.copy()
			self.add(prev_rec)

	
	def move(self, dt):
		direc_x, direc_y = self.direction
		if self.move_distance <= 0: return
		dist = self.speed * dt
		if self.move_distance - (self.speed * dt) < 0: dist += (self.move_distance - (self.speed * dt))
		self.x += (dist) * direc_x
		self.y += (dist) * direc_y
		self.move_distance -= (dist)
		self.rect.x = round(self.x)
		self.rect.y = round(self.y)

	def add(self, rect):
		self.body.append(rect)
		body_size = len(self.body)
		if body_size > self.size: self.body = self.body[1:body_size]
		

	def check_collision(self):
		p1, p2 = self.get_collision_points()
		for bdy in self.body:
			if bdy.collidepoint(p1) or bdy.collidepoint(p2):
				self.die()

	def die(self): self.alive = False


	def set_direction(self, new_direction):
		if self.direction_input[new_direction] == self.direction: return
		if self.direction_input[new_direction] == self.get_inverse_direction(): return
		self.direction = self.direction_input[new_direction]

	def get_inverse_direction(self):
		x, y = self.direction
		return x * -1, y * -1
	def get_collision_points(self):
		h_offset = S_CELL_SIZE // 2
		direc_x, direc_y = self.direction
		center_x, center_y = self.rect.center
		center_head_x = center_x + (direc_x * h_offset)
		center_head_y = center_y + (direc_y * h_offset)

		p1 = [center_head_x, center_head_y]
		p2 = [center_head_x, center_head_y]

		if direc_x == 0: 
			p1[0] += h_offset
			p2[0] -= h_offset
		if direc_y == 0: 
			p1[1] += h_offset
			p2[1] -= h_offset

		return tuple(p1), tuple(p2)

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
		self.fruit_timer = Time_Man()
	def update(self, dt):
		if self.paused: pass
		else:
			if self.snake.alive:
				self.snake.update(dt)
				self.collide_fruits()
				self.spawn_fruit(dt)

	def render(self, parent_surface):
		for fruit in self.fruits: pygame.draw.rect(self.surface, "Green", fruit)
		self.snake.render(self.surface)
		parent_surface.blit(self.surface, self.app.get_gs_position())
		

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
			if fruit.colliderect(self.snake.rect):
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

	def spawn_fruit(self, dt):
		if self.fruit_timer.dt_wait(dt, FRUIT_SPAWN_DELAY):
			fruit = choice(self.cells)
			while not self.is_valid_fruit_pos(fruit): fruit =choice(self.cells)
			self.fruits.append(fruit)

	def is_valid_fruit_pos(self, fruit):
		return fruit not in self.snake.body and \
					fruit not in self.fruits

	def parse_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: self.toggle_pause()
			if event.key == pygame.K_UP or event.key == pygame.K_w: self.snake.set_direction("UP")
			if event.key == pygame.K_DOWN or event.key == pygame.K_s: self.snake.set_direction("DOWN")
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d: self.snake.set_direction("RIGHT")
			if event.key == pygame.K_LEFT or event.key == pygame.K_a: self.snake.set_direction("LEFT")





