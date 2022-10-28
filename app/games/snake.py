from config.games_config import *
from games.game import Game
from GUI.components.lable import Lable
from GUI.components.containers import Relative_Container
import pygame
from random import choice
from enum import Enum
from utils.time import Time_Man


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
		self.rect = get_mid_cell(snake_game)
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

	# -- Direction --
	@property
	def direction(self): return self._direction

	@direction.setter
	def direction(self, new_direction):
		assert isinstance(new_direction, DIRECTION)
		if new_direction is self._direction: return
		if new_direction.value == self.direction.inverse(): return
		self._direction = new_direction

	@direction.deleter
	def direction(self): del self._direction
	
	# -------------


	# -- Pos --
	@property
	def pos(self): return self._pos


	@pos.setter
	def pos(self, new_pos): 
		self._pos = new_pos
		x, y = new_pos
		self.rect.x, self.rect.y = round(x), round(y)

	@pos.deleter
	def pos(self): del self._pos
	# -------------


	# -- Render --
	def render(self):
		for bdy in self.body: self.snake_game.surface.blit(get_rect_surface(self.snake_game, bdy, self.color), bdy.topleft)
		self.snake_game.surface.blit(get_rect_surface(self.snake_game, self.rect, self.color), self.rect.topleft)
	# ------------

	# -- Update --
	def update(self, dt):
		self.body_collision()
		self.wall_collision()
		self.food_collision()
		self.set_move_distance(dt)
		self.move(dt)
	# ------------
	

	# -- Collision Detection --
	def body_collision(self):
		p1, p2 = get_collision_points(self)
		for bdy in self.body:
			if bdy.collidepoint(p1) or bdy.collidepoint(p2):
				self.die()
	
	def wall_collision(self):
		width, height = self.snake_game.surface.get_size()
		p1, p2 = get_collision_points(self)
		if p1[0] >= width or p1[0] <= 0 \
			or p1[1] >= height or p1[1] <= 0: self.die()
	
	def food_collision(self):
		collided = []
		for food in self.snake_game.foods:
			if food.colliderect(self.rect):
				self.size += 1
				self.snake_game.score += 1
				self.snake_game.snake_GUI.lables['score_lable'].message = f'{self.snake_game.score}'
				collided.append(food)
		for food in collided: self.snake_game.foods.remove(food)
	# -------------------------


	# -- Game Logic --
	def die(self): 
		self.alive = False
		self.snake_game.snake_GUI.lables['final_score_lable'].message = f'{self.snake_game.score}'
	
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
	
	def set_move_distance(self, dt):
		if self.timer.dt_wait(dt, SNAKE_MOVE_FREQ + TIME_TO_COVER_CELL):
			self.distance_to_move += S_CELL_SIZE
			prev_rec = self.rect.copy()
			self.add(prev_rec)
	# ----------------


class Snake_GUI:
	def __init__(self, snake_game):
		self.snake_game = snake_game
		self.containers = {}
		self.lables = {}
		self._surface = snake_game.surface
		self.populate_GUI()

	@property
	def surface(self): return self.snake_game.surface
	@surface.setter
	def surface(self, new_surface): self._surface = new_surface
	@surface.deleter
	def surface(self): del self._surfacex
	
	def populate_GUI(self):
		self.create_containers()
		self.create_lables()
		self.populate_containers()
		

	def create_containers(self):
		game_container = Relative_Container(self.snake_game, pygame.display.get_surface().get_size(), root = True)
		paused_container = Relative_Container(self.snake_game, pygame.display.get_surface().get_size(), root = True, alpha = PAUSE_ALPHA)
		loose_container = Relative_Container(self.snake_game, pygame.display.get_surface().get_size(), root = True, alpha = LOOSE_ALPHA)
		
		loose_surface = pygame.Surface(pygame.display.get_surface().get_size())
		loose_surface.fill(LOOSE_COLOR)
		paused_surface = pygame.Surface(pygame.display.get_surface().get_size())
		paused_surface.fill(PAUSE_COLOR)
		
		loose_container.surface = loose_surface
		paused_container.surface = paused_surface


		self.containers['game_container'] = game_container
		self.containers['paused_container'] = paused_container
		self.containers['loose_container'] = loose_container
		

	def populate_containers(self):
		s_width, s_height = pygame.display.get_surface().get_size()
		center = s_width // 2, s_height // 2
		score_pos = s_width - 30, 30
		retry_pos = center[0] , center[1] + 60

		score_lable = self.lables['score_lable']
		paused_lable = self.lables['paused_lable']
		retry_lable = self.lables['retry_lable']
		final_score_lable = self.lables['final_score_lable']

		game_container = self.containers['game_container']
		paused_container = self.containers['paused_container']
		loose_container = self.containers['loose_container']

		game_container.add_component(score_lable, score_pos)
		paused_container.add_component(paused_lable, center)
		loose_container.add_component(retry_lable, retry_pos)
		loose_container.add_component(final_score_lable, center)


	def create_lables(self):
		score_lable = Lable(self.snake_game, f'{self.snake_game.score}', SCORE_FONT_SIZE, LETTER_COLOR, PAUSE_ALPHA)
		paused_lable = Lable(self.snake_game, " PAUSED ", PAUSE_FONT_SIZE , SCORE_COLOR ,NORMAL_ALPHA)
		retry_lable = Lable(self .snake_game, " SPACE TO RETRY ", 30 , SCORE_COLOR, NORMAL_ALPHA)
		final_score_lable = Lable(self.snake_game, f'{self.snake_game.score}', SCORE_FONT_SIZE, SCORE_COLOR, NORMAL_ALPHA)

		self.lables['score_lable'] = score_lable
		self.lables['paused_lable'] = paused_lable	
		self.lables['retry_lable'] = retry_lable	
		self.lables['final_score_lable'] = final_score_lable	
	


class Snake(Game):
	def __init__(self, app):
		super().__init__(app)
		self.grid = []
		self.cells = []
		self.foods = []
		self.score = 0

		self.snake_GUI = Snake_GUI(self)
		self.food_timer = Time_Man()
		
		create_grid(self)
		self.snake = SNAKE(self)
		
	# -- Render --
	def render(self):
		if self.snake.alive:
			for food in self.foods: self.surface.blit(get_rect_surface(self, food, FOOD_COLOR), food.topleft)
			self.snake.render()
			self.snake_GUI.containers['game_container'].render(set_alpha = True)
		
		if self.paused: self.snake_GUI.containers['paused_container'].render(set_alpha = True)

		
		if not self.snake.alive: self.snake_GUI.containers['loose_container'].render(set_alpha = True)

		self.app.screen.surface.blit(self.surface, self.rect)
	# ------------


	# -- Update --
	def update(self, dt):
		if self.paused:
			self.snake_GUI.lables['paused_lable'].blink(dt) 
		else:
			if self.snake.alive:
				self.snake.update(dt)
				spawn_food(self, dt)
			else: self.snake_GUI.lables['retry_lable'].blink(dt) 

	
	def update_surface_size(self):
		self.surface = self.get_game_surface(self.color)
		self.snake_GUI = Snake_GUI(self)
		create_grid(self)
	# ------------


	# -- Player Input --
	def parse_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: toggle_pause(self)
			if event.key == pygame.K_UP or event.key == pygame.K_w: self.snake.direction = DIRECTION.UP
			if event.key == pygame.K_DOWN or event.key == pygame.K_s: self.snake.direction = DIRECTION.DOWN
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d: self.snake.direction = DIRECTION.RIGHT
			if event.key == pygame.K_LEFT or event.key == pygame.K_a: self.snake.direction = DIRECTION.LEFT
			if event.key == pygame.K_SPACE and not self.snake.alive: restart(self)
	# ------------------


# -- SNAKE helpers --
def get_collision_points(snake):
		h_offset = S_CELL_SIZE // 2
		direc_x, direc_y = snake.direction.value
		center_x, center_y = snake.rect.center
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
# -------------------

# -- snake game helpers --
def get_mid_cell(snake_game):
	row_num = len(snake_game.grid)
	col_num = len(snake_game.grid[0])
	return snake_game.grid[row_num // 2][col_num // 2].copy()
	

def get_rect_surface(snake_game, rect, color):
	rect_surface = pygame.Surface(rect.size)
	rect_surface.fill(color)
	if snake_game.paused: rect_surface.set_alpha(PAUSE_ALPHA)
	else: rect_surface.set_alpha(NORMAL_ALPHA)
	return rect_surface

def toggle_pause(snake_game): 
	if snake_game.snake.alive: snake_game.paused = not snake_game.paused
	snake_game.snake_GUI.lables['score_lable'].alpha = PAUSE_ALPHA if snake_game.paused else NORMAL_ALPHA

def restart(snake_game):
	snake_game.score = 0
	snake_game.foods = []
	snake_game.snake_GUI.lables['score_lable'].update_message()
	snake_game.cells = []
	snake_game.grid = []
	create_grid(snake_game)
	del snake_game.snake
	snake_game.snake = SNAKE(snake_game)

def create_grid(snake_game):
	for h in range(snake_game.surface.get_rect().height // S_CELL_SIZE):
		row = []
		for w in range(snake_game.surface.get_rect().width // S_CELL_SIZE):
			cell = pygame.Rect((w * S_CELL_SIZE, h * S_CELL_SIZE),(S_CELL_SIZE, S_CELL_SIZE))
			row.append(cell)
			snake_game.cells.append(cell)
		snake_game.grid.append(row)

def spawn_food(snake_game, dt):
	if snake_game.food_timer.dt_wait(dt, FOOD_SPAWN_DELAY):
		food = choice(snake_game.cells)
		while not is_valid_food_pos(snake_game, food): food =choice(snake_game.cells)
		snake_game.foods.append(food)

def is_valid_food_pos(snake_game, food):
	return food not in snake_game.snake.body and \
				food not in snake_game.foods
# ------------------------