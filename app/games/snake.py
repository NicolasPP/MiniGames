from config.games_config import *
from games.game import Game
import pygame
from random import choice
from enum import Enum
from utils.time import Time_Man


'''
TODO : clean display functions with fonts
TODO : change pause and death screen to say press space
TODO : change self.paused, self.snake.isalive,
TODO: implement 
		self.screens = Enum(
			"SCREENS",
			[
				("PAUSE",app.get_game_surface(PAUSE_COLOR, alpha = PAUSE_ALPHA)),
				("DEATH",app.get_game_surface(LOOSE_COLOR, alpha = LOOSE_ALPHA))
			])
'''

class DIRECTION(Enum):
	UP = (0, -1)
	DOWN = (0 ,1)
	RIGHT = (1,0)
	LEFT = (-1, 0)

	def inverse(direction):
		x, y = direction.value
		return x * -1, y * -1

	def __mul__(self, other):
		x1, y1 = self.value
		x2 = y2 = 1
		self.assert_opperation_types(other)
		if isinstance(other, tuple): x2, y2 = other
		else: x2 = y2 = other
		return x1 * x2 , y1 * y2

	def __rmul__(self, other):
		x1 = y1 = 1
		x2, y2 = self.value
		self.assert_opperation_types(other)
		if isinstance(other, tuple): x1, y1 = other
		else: x1 = y1 = other
		return x1 * x2 , y1 * y2

	def assert_opperation_types(self, other):
		assert isinstance(other, (tuple, int, float))
		if isinstance(other, tuple):
			assert len(other) == 2
			for i in other: assert isinstance(i, (int, float))
			return 

class SNAKE:
	def __init__(self, snake_game):
		self.snake_game = snake_game
		self.rect = snake_game.get_mid_cell()
		self.rect.width -= 1
		self.rect.height -= 1
		self.size = 0
		self.body = []
		self.color = SNAKE_COLOR
		self.timer = Time_Man()
		self._direction = choice(list(DIRECTION))
		self.distance_to_move = 0
		self._pos = pygame.math.Vector2(self.rect.topleft)
		self.speed = S_CELL_SIZE / (TIME_TO_COVER_CELL / 1000)
		self.alive = True


	@property
	def direction(self): return self._direction
	@property
	def pos(self): return self._pos

	@direction.setter
	def direction(self, new_direction):
		assert isinstance(new_direction, DIRECTION)
		if new_direction is self._direction: return
		if new_direction.value == self.direction.inverse(): return
		self._direction = new_direction
	@pos.setter
	def pos(self, new_pos): 
		self._pos = new_pos
		x, y = new_pos
		self.rect.x, self.rect.y = round(x), round(y)

	@direction.deleter
	def direction(self): del self._direction
	@pos.deleter
	def pos(self): del self._pos

	def render(self):
		for bdy in self.body: self.snake_game.surface.blit(self.snake_game.get_rect_surface(bdy, self.color), bdy.topleft)
		self.snake_game.surface.blit(self.snake_game.get_rect_surface(self.rect, self.color), self.rect.topleft)

	def update(self, dt):# snake not bound to the board
		self.body_collision()
		self.wall_collision()
		self.food_collision()
		self.set_move_distance(dt)
		self.move(dt)

	def set_move_distance(self, dt):
		if self.timer.dt_wait(dt, SNAKE_MOVE_FREQ + TIME_TO_COVER_CELL):
			self.distance_to_move += S_CELL_SIZE
			prev_rec = self.rect.copy()
			self.add(prev_rec)
	
	def move(self, dt):
		if self.distance_to_move <= 0: return
		dist = self.speed * dt
		if self.distance_to_move - dist < 0: dist += (self.distance_to_move - dist)
		self.pos = self.pos + (self.direction * dist)
		self.distance_to_move -= dist
		
	def add(self, rect):
		self.body.append(rect)
		body_size = len(self.body)
		if body_size > self.size: self.body = self.body[1:body_size]

	
	def body_collision(self):
		p1, p2 = self.get_collision_points()
		for bdy in self.body:
			if bdy.collidepoint(p1) or bdy.collidepoint(p2):
				self.die()
	
	def wall_collision(self):
		width, height = self.snake_game.surface.get_size()
		p1, p2 = self.get_collision_points()
		if p1[0] >= width or p1[0] <= 0 \
			or p1[1] >= height or p1[1] <= 0: self.die()
	
	def food_collision(self):
		collided = []
		for food in self.snake_game.foods:
			if food.colliderect(self.rect):
				self.size += 1
				self.snake_game.score += 1
				collided.append(food)
		for food in collided: self.snake_game.foods.remove(food)

	def get_collision_points(self):
		h_offset = S_CELL_SIZE // 2
		direc_x, direc_y = self.direction.value
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

	def die(self): self.alive = False

class Snake(Game):
	def __init__(self, app):
		super().__init__(app)
		self.pause_font = pygame.font.Font(None, PAUSE_FONT_SIZE)
		self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
		self.final_score_font = pygame.font.Font(None, 30)
		self.grid = []
		self.cells = []
		self.foods = []
		self.create_grid()
		self.snake = SNAKE(self)
		self.food_timer = Time_Man()
		self.score = 0
		self.p_message_alpha = 255
		self.p_alpha_change = -1
	

	def update(self, dt):
		if self.paused or not self.snake.alive: self.update_pause_alpha(dt)
		else:
			if self.snake.alive:
				self.snake.update(dt)
				self.spawn_food(dt)

	def render(self):
		if self.paused: self.display_paused()
		if self.snake.alive:
			for food in self.foods: self.surface.blit(self.get_rect_surface(food, FOOD_COLOR), food.topleft)
			self.snake.render()
			self.dispaly_score()
		
		if not self.snake.alive: self.display_loose_screen()

		self.app.screen.surface.blit(self.surface, self.app.get_gs_position())

	def update_pause_alpha(self, dt):
		self.p_message_alpha +=  (ALPHA_CHANGE * dt * self.p_alpha_change)

		if self.p_message_alpha <= 0:
			self.p_message_alpha = 0
			self.p_alpha_change = 1

		if self.p_message_alpha >= 255:
			self.p_message_alpha = 255
			self.p_alpha_change = -1

	def get_rect_surface(self, rect, color):
		rect_surface = pygame.Surface(rect.size)
		rect_surface.fill(color)
		if self.paused: rect_surface.set_alpha(PAUSE_ALPHA)
		else: rect_surface.set_alpha(255)
		return rect_surface


	def display_paused(self):
		paused_surface = self.app.get_game_surface(SCORE_COLOR, alpha = PAUSE_ALPHA)
		self.surface.blit(paused_surface, (0,0))
		self.render_pause_message()


	def render_pause_message(self):
		pause_lable_render = self.pause_font.render("PAUSED", True, SCORE_COLOR)
		s_width, s_height = self.surface.get_size()
		pause_lable_rect = pause_lable_render.get_rect(topleft = (0, 0))
		pause_lable_rect = pause_lable_render.get_rect(topleft = ((s_width // 2) - (pause_lable_rect.width // 2), (s_height // 2) - (pause_lable_rect.height // 2)))
		pause_lable_render.set_alpha(self.p_message_alpha)
		self.surface.blit(pause_lable_render, pause_lable_rect)

	def toggle_pause(self): 
		if self.snake.alive: self.paused = not self.paused

	def dispaly_score(self):
		score_lable_render = self.score_font.render(f"{self.score}", True, SCORE_COLOR)
		s_width, s_height = self.surface.get_size()
		score_lable_rect = score_lable_render.get_rect(topleft = (0, 0))
		score_lable_rect = score_lable_render.get_rect(center = ((s_width) - score_lable_rect.width * 2, score_lable_rect.width * 2))
		if self.paused : score_lable_render.set_alpha(PAUSE_ALPHA)
		self.surface.blit(score_lable_render, score_lable_rect)

	def display_final_score(self):
		score_lable_render = self.final_score_font.render(f"[{self.score}]", True, SCORE_COLOR)
		s_width, s_height = self.surface.get_size()
		score_lable_rect = score_lable_render.get_rect(topleft = (0, 0))
		score_lable_rect = score_lable_render.get_rect(topleft = ((s_width // 2) - (score_lable_rect.width // 2), (s_height // 2) - (score_lable_rect.height // 2)))
		self.surface.blit(score_lable_render, score_lable_rect)

	def display_loose_screen(self):
		death_surface = self.app.get_game_surface(LOOSE_COLOR, alpha = LOOSE_ALPHA)
		self.surface.blit(death_surface, (0,0))
		self.display_final_score()
		self.display_restart()

	def display_restart(self):
		restart_lable_render = self.final_score_font.render(f"SPACE", True, SCORE_COLOR)
		s_width, s_height = self.surface.get_size()
		restart_lable_rect = restart_lable_render.get_rect(topleft = (0, 0))
		restart_lable_rect = restart_lable_render.get_rect(topleft = ((s_width // 2) - (restart_lable_rect.width // 2), (s_height // 2) - (restart_lable_rect.height // 2) + 50))
		restart_lable_render.set_alpha(self.p_message_alpha)
		self.surface.blit(restart_lable_render, restart_lable_rect)
	
	def restart(self):
		self.score = 0
		self.foods = []
		del self.snake
		self.snake = SNAKE(self)

	def create_grid(self):
		for h in range(self.surface.get_rect().height // S_CELL_SIZE):
			row = []
			for w in range(self.surface.get_rect().width // S_CELL_SIZE):
				cell = pygame.Rect((w * S_CELL_SIZE, h * S_CELL_SIZE),(S_CELL_SIZE, S_CELL_SIZE))
				row.append(cell)
				self.cells.append(cell)
			self.grid.append(row)

	def update_surface_size(self):
		self.surface =  self.app.get_game_surface(self.bg_color)
		self.create_grid()

	def spawn_food(self, dt):
		if self.food_timer.dt_wait(dt, FOOD_SPAWN_DELAY):
			food = choice(self.cells)
			while not self.is_valid_food_pos(food): food =choice(self.cells)
			self.foods.append(food)



	def get_mid_cell(self):
		row_num = len(self.grid)
		col_num = len(self.grid[0])
		return self.grid[row_num // 2][col_num // 2].copy()


	def is_valid_food_pos(self, food):
		return food not in self.snake.body and \
					food not in self.foods

	def parse_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: self.toggle_pause()
			if event.key == pygame.K_UP or event.key == pygame.K_w: self.snake.direction = DIRECTION.UP
			if event.key == pygame.K_DOWN or event.key == pygame.K_s: self.snake.direction = DIRECTION.DOWN
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d: self.snake.direction = DIRECTION.RIGHT
			if event.key == pygame.K_LEFT or event.key == pygame.K_a: self.snake.direction = DIRECTION.LEFT
			if event.key == pygame.K_SPACE and not self.snake.alive: self.restart()




