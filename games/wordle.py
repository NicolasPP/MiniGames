import pygame
import app.app_config as acfg
from games.games_config import *
from games.game import Game
from enum import Enum
from random import choice

class Word_Bank:
	def __init__(self):
		self.words = self.read_word_bank()
		self.used_words = self.get_used_words()

	def get_random_word(self):
		word = choice(self.words)
		while word in self.used_words: word = choice(self.words)
		self.used_words.append(word)
		return word

	def get_used_words(self): return [] # make a txt file where we can store used words

	def read_word_bank(self):
		words = []
		with open(WORD_BANK) as wb:
			while True:
				word = wb.readline()
				if not word: break
				words.append(word)
			wb.close()
		return(words)

class LSTATE(Enum):
	BLANK = BLANK_COLOR
	FILLED = FILLED_COLOR
	PRESENT_OUT_OF_PLACE = PRESENT_OUT_OF_PLACE_COLOR
	PRESENT_IN_PLACE = PRESENT_IN_PLACE_COLOR
	NOT_PRESENT = NOT_PRESENT_COLOR

class Letter:
	def __init__(self, wordle_game, rect, index, r, c):
		self.rect = rect
		self.index = index
		self.r = r
		self.c = c
		
		self.wordle_game = wordle_game
		self.card_bg_surface = pygame.Surface(rect.size)
		self.font = pygame.font.Font(None, LETTER_FONT_SIZE)
		self.bg_color = LSTATE.BLANK.value
  
		self._value = ''
		self._state = LSTATE.BLANK
		self.set_card_style()
  
	# --Getters--
	@property
	def state(self): return self._state
	@property
	def value(self): return self._value
	# -----------
 

	# --Setters--
	@state.setter
	def state(self, new_state):
		self._state = new_state
		self.bg_color = new_state.value
		self.set_card_style()
		if self.state is not LSTATE.BLANK: self.card_bg_surface.set_alpha(NORMAL_ALPHA)
		self.render_value()
	@value.setter
	def value(self, new_value):
		self._value = new_value
		self.render_value()
	# -----------
 

	# --Deletters--
	@value.deleter
	def value(self): del self._value
	@state.deleter
	def state(self): del self._state
	# -------------
	
	

	def render(self):
		self.wordle_game.surface.blit(self.card_bg_surface, self.rect.topleft)

	def render_value(self):
		if not self.value: self.set_card_style()
		self.card_bg_surface.blit(*self.get_value_render())

	def render_card_outline(self):
		self.card_bg_surface.fill(LETTER_OUTLINE_COLOR)
		bg = pygame.Surface((self.rect.width - round(CARD_OUTLINE_THICKNESS / 2) * 2, self.rect.height - round(CARD_OUTLINE_THICKNESS / 2) * 2))
		bg.fill(self.bg_color)
		self.card_bg_surface.set_alpha(OUTLINE_ALPHA)
		self.card_bg_surface.blit(bg, (round(CARD_OUTLINE_THICKNESS / 2), round(CARD_OUTLINE_THICKNESS / 2)))

	def set_card_style(self):
		self.card_bg_surface.fill(self.bg_color)
		if self.state is LSTATE.BLANK: self.render_card_outline() 
	
	def get_value_render(self):
		value_lable_render = self.font.render(self.value.upper(), True, LETTER_COLOR)
		s_width, s_height = self.card_bg_surface.get_size()
		# value_lable_rect = value_lable_render.get_rect(topleft = (0, 0))
		value_lable_rect = value_lable_render.get_rect(center = (self.rect.width // 2, self.rect.height // 2))
		return value_lable_render, value_lable_rect


class Wordle(Game):
	def __init__(self, app):
		super().__init__(app)
		self.current_letter_index = 0
		self.current_word_index = 0
		self.word_bank = Word_Bank()
		self.words = []
		self.letters = []
		self.create_board()
		self.game_word = self.word_bank.get_random_word()
		print(self.game_word)

	def update_surface_size(self):
		self.surface = self.app.get_game_surface(self.bg_color)
		self.resize_letters()

	def render(self):
		for letter in self.letters: letter.render()
		self.app.screen.surface.blit(self.surface, self.app.get_gs_position())

	def create_board(self):
		self.words = []
		self.letters = []
		x, y = self.get_first_letter_pos()
		for t in range(TRYS):
			word = []
			for l in range(WORD_SIZE):
				rect = pygame.Rect((x + ((LETTER_CARD_SIZE + acfg.PADDING) * l) ,y + ((LETTER_CARD_SIZE + acfg.PADDING) * t)),(LETTER_CARD_SIZE,LETTER_CARD_SIZE))
				letter = Letter(self, rect, len(self.letters), t, l)
				word.append(letter)
				self.letters.append(letter)
			self.words.append(word)

	def resize_letters(self):
		x, y = self.get_first_letter_pos()
		for t in range(TRYS):
			for l in range(WORD_SIZE):
				new_rect = pygame.Rect((x + ((LETTER_CARD_SIZE + acfg.PADDING) * l) ,y + ((LETTER_CARD_SIZE + acfg.PADDING) * t)),(LETTER_CARD_SIZE,LETTER_CARD_SIZE))
				self.words[t][l].rect = new_rect

	def get_first_letter_pos(self):
		board_size = (LETTER_CARD_SIZE * WORD_SIZE) + (acfg.PADDING * WORD_SIZE - 1)
		s_width = self.surface.get_width()
		return round(s_width / 2) - round(board_size / 2), acfg.PADDING

	def add_letter_value(self, letter_value):
		if self.current_letter_index == (WORD_SIZE): return
		current_letter = self.words[self.current_word_index][self.current_letter_index]
		self.current_letter_index += 1
		current_letter.state = LSTATE.FILLED
		current_letter.value = letter_value
		

	def remove_letter_value(self):
		if self.current_letter_index == 0: return
		self.current_letter_index -= 1
		current_letter = self.words[self.current_word_index][self.current_letter_index]
		
		current_letter.state = LSTATE.BLANK
		current_letter.value = ''

	def check_current_board_word(self):
		if self.current_letter_index != WORD_SIZE: return
		for game_word_letter, user_letter in zip(self.game_word, self.words[self.current_word_index]):
			if game_word_letter == user_letter.value: user_letter.state = LSTATE.PRESENT_IN_PLACE
			elif user_letter.value in self.game_word: user_letter.state = LSTATE.PRESENT_OUT_OF_PLACE
			else: user_letter.state = LSTATE.NOT_PRESENT 

		self.current_word_index += 1
		self.current_letter_index = 0


	def parse_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE: self.remove_letter_value() # delete
			if event.key == pygame.K_RETURN: self.check_current_board_word() # enter
			if event.key == pygame.K_a: self.add_letter_value('a')
			if event.key == pygame.K_b: self.add_letter_value('b')
			if event.key == pygame.K_c: self.add_letter_value('c')
			if event.key == pygame.K_d: self.add_letter_value('d')
			if event.key == pygame.K_e: self.add_letter_value('e')
			if event.key == pygame.K_f: self.add_letter_value('f')
			if event.key == pygame.K_g: self.add_letter_value('g')
			if event.key == pygame.K_h: self.add_letter_value('h')
			if event.key == pygame.K_i: self.add_letter_value('i')
			if event.key == pygame.K_j: self.add_letter_value('j')
			if event.key == pygame.K_k: self.add_letter_value('k')
			if event.key == pygame.K_l: self.add_letter_value('l')
			if event.key == pygame.K_m: self.add_letter_value('m')
			if event.key == pygame.K_n: self.add_letter_value('n')
			if event.key == pygame.K_o: self.add_letter_value('o')
			if event.key == pygame.K_p: self.add_letter_value('p')
			if event.key == pygame.K_q: self.add_letter_value('q')
			if event.key == pygame.K_r: self.add_letter_value('r')
			if event.key == pygame.K_s: self.add_letter_value('s')
			if event.key == pygame.K_t: self.add_letter_value('t')
			if event.key == pygame.K_u: self.add_letter_value('u')
			if event.key == pygame.K_v: self.add_letter_value('v')
			if event.key == pygame.K_w: self.add_letter_value('w')
			if event.key == pygame.K_x: self.add_letter_value('x')
			if event.key == pygame.K_y: self.add_letter_value('y')
			if event.key == pygame.K_z: self.add_letter_value('z')