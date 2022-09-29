import pygame
import app.app_config as acfg
from games.games_config import *
from games.game import Game
from enum import Enum

class Word_Bank:
	def __init__(self):
		self.words = self.read_word_bank()

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
	def __init__(self, wordle_game, rect = 1):
		self.rect = rect
		self.wordle_game = wordle_game
		self.state = LSTATE.BLANK
		self.card_bg_surface = pygame.Surface(rect.size)
		self.value = ''
		self.bg_color = self.state.value

	def render(self):
		self.set_card_style()
		self.wordle_game.surface.blit(self.card_bg_surface, self.rect.topleft)

	def set_card_style(self):
		self.bg_color = self.state.value
		self.card_bg_surface.fill(self.bg_color)
		if self.state == LSTATE.BLANK: self.render_card_outline() 

	def render_card_outline(self):
		self.card_bg_surface.fill(LETTER_OUTLINE_COLOR)
		bg = pygame.Surface((self.rect.width - round(CARD_OUTLINE_THICKNESS / 2) * 2, self.rect.height - round(CARD_OUTLINE_THICKNESS / 2) * 2))
		bg.fill(self.bg_color)
		self.card_bg_surface.set_alpha(OUTLINE_ALPHA)
		self.card_bg_surface.blit(bg, (round(CARD_OUTLINE_THICKNESS / 2), round(CARD_OUTLINE_THICKNESS / 2)))
		
class Wordle(Game):
	def __init__(self, app):
		super().__init__(app)
		self.word_bank = Word_Bank()
		self.words = []
		self.letters = []
		self.create_board()

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
				letter = Letter(self, pygame.Rect((x + ((LETTER_CARD_SIZE + acfg.PADDING) * l) ,y + ((LETTER_CARD_SIZE + acfg.PADDING) * t)),(LETTER_CARD_SIZE,LETTER_CARD_SIZE)))
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
