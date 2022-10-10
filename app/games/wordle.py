import pygame
import config.app_config as acfg
from config.games_config import *
from GUI.lable import Lable
from games.game import Game
from enum import Enum
from random import choice
import enchant
import unidecode
import pickle

'''
TODO : display message when user tries to guess a word that does not exist
TODO : add animation for when user makes a guess. make new state color fade in
TODO : reduce the amount of suggested words
TODO : show word when loose
TODO : store only one list of used_words
TODO : maybe remove pt language too many workarounds.
TODO : find new 5 letter words file - https://github.com/dwyl/english-words
       python example - https://github.com/dwyl/english-words/blob/master/read_english_dictionary.py
'''

'''
	Pickle data format - only two languages -
	{
		'pt_BR' : {
			language :
			words :
			used_words :

		},
		'en_US' : {
			language :
			words :
			used_words :

		}

	}
'''

PT = 'pt_BR'
ENG = 'en_US'

class GAMELANG(Enum):
	ENG = enchant.Dict(ENG)
	PT = enchant.Dict(PT)

class LSTATE(Enum):
	BLANK = BLANK_COLOR
	FILLED = FILLED_COLOR
	PRESENT_OUT_OF_PLACE = PRESENT_OUT_OF_PLACE_COLOR
	PRESENT_IN_PLACE = PRESENT_IN_PLACE_COLOR
	NOT_PRESENT = NOT_PRESENT_COLOR

class GAME_RESULT(Enum):
	WON = 1
	LOST = 2
	UNDEFINED = 3

class Word_Bank:

	def __init__(self, lang):
		self.language = lang
		self.lang_tag = self.get_language_tag()
		self.load_data()
		print(self.used_words)

	def get_random_word(self):
		word = choice(self.words)
		while word in self.used_words: word = choice(self.words)
		self.used_words.append(word)
		self.write_data()
		print(word)
		return word

	def get_language_tag(self):
		if self.language is GAMELANG.ENG: return ENG
		elif self.language is GAMELANG.PT: return PT

	def write_data(self):
		file = open(WORD_FILE, 'wb')
		self.data[self.lang_tag]['used_words'] = self.used_words
		pickle.dump(self.data, file)
		file.close()

	def load_data(self):
		file = open(WORD_FILE, 'rb')
		self.data = pickle.load(file)
		self.words = self.data[self.lang_tag]['words']
		self.used_words = self.data[self.lang_tag]['used_words']
		file.close()

	def is_guess_valid(self, word):
		if self.language is GAMELANG.ENG: return self.check_eng(word)
		elif self.language is GAMELANG.PT: return self.check_pt(word)

	def check_pt(self, word):
		'''
		checking pt word is valid without any
		accents. We get a list of surggested words
		and see if if its in there
		'''
		valid = False
		suggestions = self.language.value.suggest(word)
		for sgt in suggestions:
			if unidecode.unidecode(sgt) == word:
				valid = self.language.value.check(sgt)
		return valid
	def check_eng(self, word): 
		if word in self.words: return True
		return self.language.value.check(word)



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
		if self.wordle_game.result == GAME_RESULT.LOST: self.card_bg_surface.set_alpha(PAUSE_ALPHA)
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
		return Lable(pos, self.value, LETTER_FONT_SIZE, LETTER_COLOR)


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
		self.post_message_font = pygame.font.Font(None, 50)
		self.restart_message_font = pygame.font.Font(None, 30)
		self.restart_alpha = 255
		self.restart_alpha_change = -1
		self.SCREENS = self.set_screen_enum()

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

	def set_screen_enum(self):
		return Enum(
			"SCREENS",
			[
				("WON",self.app.get_game_surface(WON_COLOR, alpha = POST_GAME_ALPHA)),
				("LOST",self.app.get_game_surface(LOST_COLOR, alpha = POST_GAME_ALPHA))
			])

	def update(self, dt):
		for letter in self.letters: letter.update(dt)
		if self.result is not GAME_RESULT.UNDEFINED: self.update_restart_alpha(dt)


	def update_restart_alpha(self, dt):
		self.restart_alpha +=  (ALPHA_CHANGE * dt * self.restart_alpha_change)

		if self.restart_alpha <= 0:
			self.restart_alpha = 0
			self.restart_alpha_change = 1

		if self.restart_alpha >= 255:
			self.restart_alpha = 255
			self.restart_alpha_change = -1

	def update_surface_size(self):
		self.surface = self.app.get_game_surface(self.bg_color)
		self.resize_letters()
		self.SCREENS = self.set_screen_enum()


	def render(self):
		for letter in self.letters: letter.render()
		if self.result is GAME_RESULT.WON: self.render_win()
		elif self.result is GAME_RESULT.LOST: self.render_lost()
		self.app.screen.surface.blit(self.surface, self.app.get_gs_position())

	def render_win(self):
		self.surface.blit(self.SCREENS.WON.value, (0,0))
		self.surface.blit(*self.get_center_message_render(" GAME WON  ", self.post_message_font, LETTER_COLOR, NORMAL_ALPHA))
		self.display_restart_message()
	def render_lost(self):
		self.surface.blit(self.SCREENS.LOST.value, (0,0))
		self.surface.blit(*self.get_center_message_render(" GAME LOST ", self.post_message_font, LETTER_COLOR, NORMAL_ALPHA))
		self.display_restart_message()

	def display_restart_message(self):
		self.surface.blit(*self.get_center_message_render(" SPACE TO RESTART", self.restart_message_font, LETTER_COLOR, self.restart_alpha, h_offset = 60))

	def get_center_message_render(self, message, font, color, alpha, w_offset = 0, h_offset = 0):
		message_lable_render = font.render(message, True, color)
		s_width, s_height = self.surface.get_size()
		message_lable_rect = message_lable_render.get_rect(center = ((s_width // 2) + w_offset, (s_height// 2) + h_offset))
		message_lable_render.set_alpha(alpha)
		return message_lable_render, message_lable_rect
	
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
		game_word = unidecode.unidecode(self.game_word)
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
			and correct_letters != WORD_SIZE: self.result = GAME_RESULT.LOST

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