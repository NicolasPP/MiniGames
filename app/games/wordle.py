import config.app_config as acfg
from config.games_config import *

from GUI.components.lable import Lable
from games.game import Game
import data.data_manager as Data_Man

import pickle
import pygame
from enum import Enum
from random import choice


'''
TODO : display message when user tries to guess a word that does not exist
TODO : add animation for when user makes a guess. make new state color fade in
TODO : add option to pick language in wordle
TODO : show word when loose
'''


'''
WORDLE_DEBUG_MODE - when True,  - will not overwrite words data with
							   new used_words data, because everytime I run 
							   it picks a word and adds it to used_words. 
							   When testing used_words can fill up quickly.
							    - word choosen will be printed in the 
							    console. for ease of testing


'''
WORDLE_DEBUG_MODE = True



class GAMELANG(Enum):
	ENG = 'english'
	PT = 'portuguese'

class LSTATE(Enum):
	BLANK = BLANK_COLOR
	FILLED = FILLED_COLOR
	PRESENT_OUT_OF_PLACE = PRESENT_OUT_OF_PLACE_COLOR
	PRESENT_IN_PLACE = PRESENT_IN_PLACE_COLOR
	NOT_PRESENT = NOT_PRESENT_COLOR

	def __eq__(self, state):
		if isinstance(state, LSTATE): return self.name == state.name
		return False

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
		if WORDLE_DEBUG_MODE:
			self.add_used_word(word)
			print(word)
		else: Data_Man.write_data(WORD_FILE, self.data)
		return word

	def available_words(self):
		for word in self.data[self.language][self.words]:
			if not word in self.data[self.language][self.used_words]: yield word

	def add_used_word(self, word):
		self.data[self.language][self.used_words].append(word)


	def is_guess_valid(self, word):
		return word in self.data[self.language][self.words]

	def empty_used_words(self, *languages):
		for lang in languages: self.data[lang.value][self.used_words] = []
		Data_Man.write_data(WORD_FILE, self.data)

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
		set_card_style(self)

		self.lable = get_value_lable(self)
  
	# -- Getters --
	@property
	def state(self): return self._state
	@property
	def value(self): return self._value
	# -------------
 

	# -- Setters --
	@state.setter
	def state(self, new_state):
		self._state = new_state
		self.bg_color = new_state.value
		set_card_style(self)
		if self.state != LSTATE.BLANK: self.card_bg_surface.set_alpha(NORMAL_ALPHA)
		if self.wordle_game.result == GAME_RESULT.WON: self.card_bg_surface.set_alpha(PAUSE_ALPHA)
		if self.wordle_game.result == GAME_RESULT.LOOSE: self.card_bg_surface.set_alpha(PAUSE_ALPHA)
		self.lable = get_value_lable(self)
		self.render_value()
	@value.setter
	def value(self, new_value):
		self._value = new_value
		self.lable.message = new_value
		self.render_value()
	# -------------
 

	# -- Deleters --
	@value.deleter
	def value(self): del self._value
	@state.deleter
	def state(self): del self._state
	# --------------
	

	# -- Render --
	def render(self):
		self.wordle_game.surface.blit(self.card_bg_surface, self.rect.topleft)

	def render_value(self):
		if not self.value: 
			set_card_style(self)
			return 
		self.card_bg_surface.blit(*self.lable.get_surface_blit())

	def render_card_outline(self):
		self.card_bg_surface.fill(LETTER_OUTLINE_COLOR)
		bg = pygame.Surface((self.rect.width - round(CARD_OUTLINE_THICKNESS / 2) * 2, self.rect.height - round(CARD_OUTLINE_THICKNESS / 2) * 2))
		bg.fill(self.bg_color)
		self.card_bg_surface.set_alpha(OUTLINE_ALPHA)
		self.card_bg_surface.blit(bg, (round(CARD_OUTLINE_THICKNESS / 2), round(CARD_OUTLINE_THICKNESS / 2)))
	# ------------


class Wordle(Game):
	def __init__(self, app):
		if WORDLE_DEBUG_MODE: print('WORDLE_DEBUG_MODE is TRUE -------------- REMOVE BEFORE UPDATING DIST --------------')
		super().__init__(app)
		self.current_letter_index = 0
		self.current_word_index = 0
		self.word_bank = Word_Bank(GAMELANG.PT)
		self.words = []
		self.letters = []
		create_board(self)
		self.game_word = self.word_bank.get_random_word()
		self._result = GAME_RESULT.UNDEFINED
		self.restart_alpha = 255
		self.restart_alpha_change = -1
		self.lables = get_wordle_lables(self)

	# -- Getters --
	@property
	def result(self): return self._result
	# -------------


	# -- Setters --
	@result.setter
	def result(self, new_result):
		self._result = new_result
		invalidate_letters_state(self)
	# -------------


	# -- Deleters --
	@result.deleter
	def result(sefl): del self._result
	# --------------


	# -- Render --
	def render(self):
		for letter in self.letters: letter.render()
		if self.result is GAME_RESULT.WON: self.render_message('win', 'restart')
		elif self.result is GAME_RESULT.LOOSE: self.render_message('loose', 'restart')
		self.app.screen.surface.blit(self.surface, self.rect)
	
	def render_message(self, *lable_ids):
		for l_id in lable_ids:
			lable = self.lables[l_id]['lable']
			lable_surface  = self.lables[l_id]['surface']
			if lable_surface : self.surface.blit(lable_surface, (0,0))  	
			lable.render(set_alpha = True)
	# ------------


	# -- Update --
	def update(self, dt):
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
		self.update_letters_size()
		self.lables = get_wordle_lables(self)

	def update_letters_size(self):
		x, y = get_first_letter_pos(self)
		for t in range(TRYS):
			for l in range(WORD_SIZE):
				new_rect = pygame.Rect((x + ((LETTER_CARD_SIZE + acfg.PADDING) * l) ,y + ((LETTER_CARD_SIZE + acfg.PADDING) * t)),(LETTER_CARD_SIZE,LETTER_CARD_SIZE))
				self.words[t][l].rect = new_rect
	# ------------


	# -- Player Input --
	def parse_event(self, event):
		if event.type == pygame.KEYDOWN:
			if self.result == GAME_RESULT.UNDEFINED:
				if self.user_input[pygame.K_BACKSPACE]: remove_letter_value(self) # delete
				elif self.user_input[pygame.K_RETURN]: 	check_current_board_word(self) # enter
				else : add_letter_value(self, pygame.key.name(event.key))
			else:
				if self.user_input[pygame.K_SPACE]: restart_game(self)
	# ------------------


# -- letter helpers --
def set_card_style(letter):
	letter.card_bg_surface.fill(letter.bg_color)
	if letter.state == LSTATE.BLANK: letter.render_card_outline() 

def get_value_lable(letter):
	s_width, s_height = letter.card_bg_surface.get_size()
	pos = (letter.rect.width // 2, letter.rect.height // 2)
	return Lable(letter, letter.card_bg_surface.get_rect().center, letter.value, LETTER_FONT_SIZE, LETTER_COLOR, NORMAL_ALPHA)

def reset(letter):
	letter.value = ''
	letter.state = LSTATE.BLANK
# --------------------

# -- wordle game helpers --
def get_wordle_lables(wordle_game):
		s_width, s_height = wordle_game.surface.get_size()
		center = s_width // 2, s_height // 2
		restart_pos = center[0] , center[1] + 60
		win_surface = wordle_game.app.get_game_surface(PRESENT_IN_PLACE_COLOR, alpha = POST_GAME_ALPHA)
		loose_surface = wordle_game.app.get_game_surface(LOOSE_COLOR, alpha = POST_GAME_ALPHA)
		return {
			'win' : 
				{
				'lable' : Lable(wordle_game, center, " GAME WON  ", 50, LETTER_COLOR,POST_GAME_ALPHA),
				'surface' : win_surface,
				},
			'loose' : 
				{
				'lable' : Lable(wordle_game, center, " GAME LOST ", 50, LETTER_COLOR,POST_GAME_ALPHA),
				'surface' : loose_surface,
				},
			'restart' : 
				{
				'lable' : Lable(wordle_game, restart_pos, " SPACE TO RESTART ", 30, LETTER_COLOR,NORMAL_ALPHA),
				'surface' : False,
				}
		}

def get_first_letter_pos(wordle_game):
		board_size = (LETTER_CARD_SIZE * WORD_SIZE) + (acfg.PADDING * WORD_SIZE - 1)
		s_width = wordle_game.surface.get_width()
		return round(s_width / 2) - round(board_size / 2), acfg.PADDING

def get_board_word(wordle_game):
		result = ''
		current_word = wordle_game.words[wordle_game.current_word_index]
		for letter in current_word: result += letter.value
		return result

def restart_game(wordle_game):
		for letter in wordle_game.letters: reset(letter)
		wordle_game.result = GAME_RESULT.UNDEFINED
		wordle_game.game_word = wordle_game.word_bank.get_random_word()
		wordle_game.current_letter_index = 0
		wordle_game.current_word_index = 0

def create_board(wordle_game):
		wordle_game.words = []
		wordle_game.letters = []
		x, y = get_first_letter_pos(wordle_game)
		for t in range(TRYS):
			word = []
			for l in range(WORD_SIZE):
				rect = pygame.Rect((x + ((LETTER_CARD_SIZE + acfg.PADDING) * l) ,y + ((LETTER_CARD_SIZE + acfg.PADDING) * t)),(LETTER_CARD_SIZE,LETTER_CARD_SIZE))
				letter = Letter(wordle_game, rect, len(wordle_game.letters), t, l)
				word.append(letter)
				wordle_game.letters.append(letter)
			wordle_game.words.append(word)

def invalidate_letters_state(wordle_game):
	for letter in wordle_game.letters: letter.state = letter.state
def add_letter_value(wordle_game, letter_value):
		if not letter_value in ALPHABET: return 
		if wordle_game.current_letter_index == (WORD_SIZE): return
		current_letter = wordle_game.words[wordle_game.current_word_index][wordle_game.current_letter_index]
		wordle_game.current_letter_index += 1
		current_letter.state = LSTATE.FILLED
		current_letter.value = letter_value

def remove_letter_value(wordle_game):
		if wordle_game.current_letter_index == 0: return
		wordle_game.current_letter_index -= 1
		current_letter = wordle_game.words[wordle_game.current_word_index][wordle_game.current_letter_index]
		
		current_letter.state = LSTATE.BLANK
		current_letter.value = ''

def check_current_board_word(wordle_game):
		correct_letters = 0
		game_word = wordle_game.game_word
		if wordle_game.current_letter_index != WORD_SIZE: return
		if not wordle_game.word_bank.is_guess_valid(get_board_word(wordle_game)): return
		update_letter_state = {}

		for game_word_letter, user_letter in zip(game_word, wordle_game.words[wordle_game.current_word_index]):
			if game_word_letter == user_letter.value:
				user_letter.state = LSTATE.PRESENT_IN_PLACE
				correct_letters += 1
			elif user_letter.value in game_word: user_letter.state = LSTATE.PRESENT_OUT_OF_PLACE
			else: user_letter.state = LSTATE.NOT_PRESENT

		if correct_letters == WORD_SIZE: wordle_game.result = GAME_RESULT.WON
		if wordle_game.current_word_index == TRYS - 1\
			and correct_letters != WORD_SIZE: wordle_game.result = GAME_RESULT.LOOSE

		wordle_game.current_word_index += 1
		wordle_game.current_letter_index = 0
# -------------------------