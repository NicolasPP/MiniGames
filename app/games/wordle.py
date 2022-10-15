
import config.app_config as acfg
from config.games_config import *

from GUI.lable import Lable
from games.game import Game
import data.data_manager as Data_Man

import pickle
import pygame
from enum import Enum
from random import choice

'''
TODO : display message when user tries to guess a word that does not exist
TODO : add animation for when user makes a guess. make new state color fade in
TODO : show word when loose
'''
class GAMELANG(Enum):
	ENG = 'english'
class LSTATE(Enum):
	BLANK = BLANK_COLOR
	FILLED = FILLED_COLOR
	PRESENT_OUT_OF_PLACE = PRESENT_OUT_OF_PLACE_COLOR
	PRESENT_IN_PLACE = PRESENT_IN_PLACE_COLOR
	NOT_PRESENT = NOT_PRESENT_COLOR
class GAME_RESULT(Enum):
	WON = 1
	LOOSE = 2
	UNDEFINED = 3


class Word_Bank:

	def __init__(self, lang):
		self.language = lang.value
		self.data = Data_Man.get_data(WORD_FILE)
		self.words = 'words'
		self.used_words = 'used_words'

	def get_random_word(self):
		word = choice(list(self.available_words()))
		self.add_used_word(word)
		Data_Man.write_data(WORD_FILE, self.data)
		print(word)
		return word

	def available_words(self):
		for word in self.data[self.language][self.words]:
			if not word in self.data[self.language][self.used_words]: yield word

	def add_used_word(self, word):
		self.data[self.language][self.used_words].append(word)


	def is_guess_valid(self, word):
		return word in self.data[self.language][self.words]

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

		self.lable = self.get_value_lable()
  
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
		if self.wordle_game.result == GAME_RESULT.WON: self.card_bg_surface.set_alpha(PAUSE_ALPHA)
		if self.wordle_game.result == GAME_RESULT.LOOSE: self.card_bg_surface.set_alpha(PAUSE_ALPHA)
		self.lable = self.get_value_lable()
		self.draw_value()
	@value.setter
	def value(self, new_value):
		self._value = new_value
		self.lable = self.get_value_lable()
		self.draw_value()
	# -----------
 

	# --Deleters--
	@value.deleter
	def value(self): del self._value
	@state.deleter
	def state(self): del self._state
	# ------------
	
	
	def update(self, dt): pass

	def render(self):
		self.wordle_game.surface.blit(self.card_bg_surface, self.rect.topleft)

	def draw_value(self):
		if not self.value: self.set_card_style()
		self.card_bg_surface.blit(*self.lable.get_lable_blit())

	def draw_card_outline(self):
		self.card_bg_surface.fill(LETTER_OUTLINE_COLOR)
		bg = pygame.Surface((self.rect.width - round(CARD_OUTLINE_THICKNESS / 2) * 2, self.rect.height - round(CARD_OUTLINE_THICKNESS / 2) * 2))
		bg.fill(self.bg_color)
		self.card_bg_surface.set_alpha(OUTLINE_ALPHA)
		self.card_bg_surface.blit(bg, (round(CARD_OUTLINE_THICKNESS / 2), round(CARD_OUTLINE_THICKNESS / 2)))

	def set_card_style(self):
		self.card_bg_surface.fill(self.bg_color)
		if self.state is LSTATE.BLANK: self.draw_card_outline() 
	
	def get_value_lable(self):
		s_width, s_height = self.card_bg_surface.get_size()
		pos = (self.rect.width // 2, self.rect.height // 2)
		return Lable(pos, self.value, LETTER_FONT_SIZE, LETTER_COLOR, NORMAL_ALPHA)


	def get_value_render(self):
		value_lable_render = self.font.render(self.value.upper(), True, LETTER_COLOR)
		s_width, s_height = self.card_bg_surface.get_size()
		value_lable_rect = value_lable_render.get_rect(center = (self.rect.width // 2, self.rect.height // 2))
		return value_lable_render, value_lable_rect

	def reset(self):
		self.value = ''
		self.state = LSTATE.BLANK

class Wordle(Game):
	def __init__(self, app):
		super().__init__(app)
		self.current_letter_index = 0
		self.current_word_index = 0
		self.word_bank = Word_Bank(GAMELANG.ENG)
		self.words = []
		self.letters = []
		self.create_board()
		self.game_word = self.word_bank.get_random_word()
		self._result = GAME_RESULT.UNDEFINED
		self.restart_alpha = 255
		self.restart_alpha_change = -1
		self.lables = self.get_wordle_lables()

	# --Getters--
	@property
	def result(self): return self._result
	# -----------

	# --Setters--
	@result.setter
	def result(self, new_result):
		self._result = new_result
		self.invalidate_letters_state()
	# -----------

	# --Deleters--
	@result.deleter
	def result(sefl): del self._result
	# ------------	

	def get_wordle_lables(self):
		s_width, s_height = self.surface.get_size()
		center = s_width // 2, s_height // 2
		restart_pos = center[0] , center[1] + 60
		win_surface = self.app.get_game_surface(PRESENT_IN_PLACE_COLOR, alpha = POST_GAME_ALPHA)
		loose_surface = self.app.get_game_surface(LOOSE_COLOR, alpha = POST_GAME_ALPHA)
		return {
			'win' : 
				{
				'lable' : Lable(center, " GAME WON  ", 50, LETTER_COLOR,POST_GAME_ALPHA),
				'surface' : win_surface,
				},
			'loose' : 
				{
				'lable' : Lable(center, " GAME LOST ", 50, LETTER_COLOR,POST_GAME_ALPHA),
				'surface' : loose_surface,
				},
			'restart' : 
				{
				'lable' : Lable(restart_pos, " SPACE TO RESTART ", 30, LETTER_COLOR,NORMAL_ALPHA),
				'surface' : False,
				}
		}

	def render_message(self, *lable_ids):
		for l_id in lable_ids:
			lable = self.lables[l_id]['lable']
			lable_surface  = self.lables[l_id]['surface']
			if lable_surface : self.surface.blit(lable_surface, (0,0))  	
			self.surface.blit(*lable.get_lable_blit())



		


	def update(self, dt):
		for letter in self.letters: letter.update(dt)
		if self.result is not GAME_RESULT.UNDEFINED: self.update_restart_alpha(dt)


	def update_restart_alpha(self, dt):
		self.restart_alpha +=  (ALPHA_CHANGE * dt * self.restart_alpha_change)
		self.lables['restart']['lable'].alpha = self.restart_alpha
		if self.restart_alpha <= 0:
			self.restart_alpha = 0
			self.restart_alpha_change = 1

		if self.restart_alpha >= 255:
			self.restart_alpha = 255
			self.restart_alpha_change = -1

	def update_surface_size(self):
		self.surface = self.app.get_game_surface(self.bg_color)
		self.resize_letters()
		self.lables = self.get_wordle_lables()

	def render(self):
		for letter in self.letters: letter.render()
		if self.result is GAME_RESULT.WON: self.render_message('win', 'restart')
		elif self.result is GAME_RESULT.LOOSE: self.render_message('loose', 'restart')
		self.app.screen.surface.blit(self.surface, self.app.get_gs_position())

	
	def restart_game(self):
		for letter in self.letters: letter.reset()
		self.result = GAME_RESULT.UNDEFINED
		self.game_word = self.word_bank.get_random_word()
		self.current_letter_index = 0
		self.current_word_index = 0

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

	def invalidate_letters_state(self):
		for letter in self.letters: letter.state = letter.state

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
		correct_letters = 0
		game_word = self.game_word
		if self.current_letter_index != WORD_SIZE: return
		if not self.word_bank.is_guess_valid(self.get_board_word()): return
		update_letter_state = {}

		for game_word_letter, user_letter in zip(game_word, self.words[self.current_word_index]):
			if game_word_letter == user_letter.value:
				user_letter.state = LSTATE.PRESENT_IN_PLACE
				correct_letters += 1
			elif user_letter.value in game_word: user_letter.state = LSTATE.PRESENT_OUT_OF_PLACE
			else: user_letter.state = LSTATE.NOT_PRESENT

		if correct_letters == WORD_SIZE: self.result = GAME_RESULT.WON
		if self.current_word_index == TRYS - 1\
			and correct_letters != WORD_SIZE: self.result = GAME_RESULT.LOOSE

		self.current_word_index += 1
		self.current_letter_index = 0

	def get_board_word(self):
		result = ''
		current_word = self.words[self.current_word_index]
		for letter in current_word: result += letter.value
		return result

	def parse_event(self, event):
		if event.type == pygame.KEYDOWN:
			if self.result == GAME_RESULT.UNDEFINED:
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
			else:
				if event.key == pygame.K_SPACE: self.restart_game()