import config.app_config as acfg
from config.games_config import *

from GUI.components.lable import Lable
from GUI.components.containers import Relative_Container
from games.game import Game, Game_GUI
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
		self.data = Data_Man.get_wordle_data(WORD_FILE)
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
		self.bg_color = LSTATE.BLANK.value
  
		self._value = ''
		self._state = LSTATE.BLANK
		set_card_style(self)

		self.lable = get_value_lable(self)
  
 	# -- State --
	@property
	def state(self): return self._state
	@state.setter
	def state(self, new_state) -> None:
		self._state = new_state
		self.bg_color = new_state.value
		set_card_style(self)
		if self.state != LSTATE.BLANK: self.card_bg_surface.set_alpha(NORMAL_ALPHA)
		if self.wordle_game.result == GAME_RESULT.WON: self.card_bg_surface.set_alpha(PAUSE_ALPHA)
		if self.wordle_game.result == GAME_RESULT.LOOSE: self.card_bg_surface.set_alpha(PAUSE_ALPHA)
		self.lable = get_value_lable(self)
		self.render_value()
	
	@state.deleter
	def state(self): del self._state
	# -------------
 

	# -- Value --
	@property
	def value(self): return self._value

	@value.setter
	def value(self, new_value):
		self._value = new_value
		self.lable.message = new_value
		self.render_value()

	@value.deleter
	def value(self): del self._value
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

class Wordle_GUI(Game_GUI):
	def __init__(self, wordle_game):
		super().__init__(wordle_game)
		self.populate_GUI()
	
	def populate_GUI(self):
		self.create_containers()
		self.create_lables()
		self.populate_containers()
		

	def create_containers(self):
		win_container = Relative_Container(self.game, pygame.display.get_surface().get_size(), root = True, alpha = POST_GAME_ALPHA)
		loose_container = Relative_Container(self.game, pygame.display.get_surface().get_size(), root = True, alpha = POST_GAME_ALPHA)
		
		win_surface = pygame.Surface(pygame.display.get_surface().get_size())
		win_surface.fill(PRESENT_IN_PLACE_COLOR)
		loose_surface = pygame.Surface(pygame.display.get_surface().get_size())
		loose_surface.fill(LOOSE_COLOR)

		win_container.surface = win_surface
		loose_container.surface = loose_surface

		self.containers['win_container'] = win_container
		self.containers['loose_container'] = loose_container

	def populate_containers(self):
		s_width, s_height = pygame.display.get_surface().get_size()
		center = s_width // 2, s_height // 2
		restart_pos = center[0] , center[1] + 60
		
		win_container = self.containers['win_container'] 
		loose_container = self.containers['loose_container']

		win_lable = self.lables['win_lable']
		loose_lable = self.lables['loose_lable']
		restart_lable = self.lables['restart_lable']
		play_again_lable = self.lables['play_again_lable']

		win_container.add_component(win_lable, center)
		win_container.add_component(play_again_lable, restart_pos)
		loose_container.add_component(loose_lable, center)
		loose_container.add_component(restart_lable, restart_pos)
		
	def create_lables(self):
		win_lable = Lable(self.game, " GAME WON  ", 50, LETTER_COLOR, NORMAL_ALPHA)
		loose_lable = Lable(self.game, " GAME LOST ", 50, LETTER_COLOR, NORMAL_ALPHA)
		restart_lable = Lable(self.game, " SPACE TO RESTART ", 30, LETTER_COLOR, NORMAL_ALPHA)
		play_again_lable = Lable(self.game, " SPACE TO PLAY AGAIN ", 30, LETTER_COLOR, NORMAL_ALPHA)
		
		self.lables['win_lable'] = win_lable
		self.lables['loose_lable'] = loose_lable
		self.lables['restart_lable'] = restart_lable
		self.lables['play_again_lable'] = play_again_lable


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
		self.wordle_GUI = Wordle_GUI(self)

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
		if self.result is GAME_RESULT.WON: self.wordle_GUI.containers['win_container'].render(set_alpha = True)
		elif self.result is GAME_RESULT.LOOSE: self.wordle_GUI.containers['loose_container'].render(set_alpha = True)
		self.app.screen.surface.blit(self.surface, self.rect)
	# ------------


	# -- Update --
	def update(self, dt):
		if self.result is not GAME_RESULT.UNDEFINED:
			self.wordle_GUI.lables['play_again_lable'].blink(dt)
			self.wordle_GUI.lables['restart_lable'].blink(dt)

	
	def update_surface_size(self):
		self.surface = self.get_game_surface(self.color)
		self.update_letters_size()

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
				if pygame.key.get_pressed()[pygame.K_BACKSPACE]: remove_letter_value(self) # delete
				elif pygame.key.get_pressed()[pygame.K_RETURN]: 	check_current_board_word(self) # enter
				else : add_letter_value(self, pygame.key.name(event.key))
			else:
				if pygame.key.get_pressed()[pygame.K_SPACE]: restart_game(self)
	# ------------------


# -- letter helpers --
def set_card_style(letter):
	letter.card_bg_surface.fill(letter.bg_color)
	if letter.state == LSTATE.BLANK: letter.render_card_outline() 

def get_value_lable(letter):
	l = Lable(letter, letter.value, LETTER_FONT_SIZE, LETTER_COLOR, NORMAL_ALPHA, pos = letter.card_bg_surface.get_rect().center)
	return l

def reset(letter):
	letter.value = ''
	letter.state = LSTATE.BLANK
# --------------------

# -- wordle game helpers --
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