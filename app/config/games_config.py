from color.color_palettes import color_palette2, color_palette3, color_palette1


# ------ GENERAL ------
GAME_BG = color_palette2[0] #rgb(44, 54, 57)
PAUSE_COLOR = "white"
SCORE_COLOR = color_palette3[3] #rgb(231, 171, 121)
LOOSE_COLOR = color_palette2[3] #rgb(220, 215, 201)

PAUSE_ALPHA = 15 # 0 is fully transparent and 255 fully opaque.
LOOSE_ALPHA = 150
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
#----------------------


#------ SNAKE ------
S_CELL_SIZE = 10

SNAKE_COLOR = color_palette2[3] #rgb(220, 215, 201)
FOOD_COLOR = color_palette3[3] #rgb(231, 171, 121)

PAUSE_FONT_SIZE = 50
SCORE_FONT_SIZE = 40


	# time (ms)
FOOD_SPAWN_DELAY = 5000
SNAKE_MOVE_FREQ = 250
ALPHA_CHANGE = 700
TIME_TO_COVER_CELL = 150
#-------------------


#------ WORDLE ------
LETTER_OUTLINE_COLOR = color_palette3[3]#rgb(231, 171, 121)
BLANK_COLOR = color_palette2[0]#rgb(44, 54, 57)
FILLED_COLOR = color_palette2[0]#rgb(44, 54, 57)
PRESENT_OUT_OF_PLACE_COLOR = (181, 159, 59) #rgb(181, 159, 59)
PRESENT_IN_PLACE_COLOR = (83, 141, 78) #rgb(83, 141, 78)
NOT_PRESENT_COLOR = (58, 58, 60) #rgb(58, 58, 60)
LETTER_COLOR = color_palette2[3] #rgb(220, 215, 201)
WON_COLOR = (83, 141, 78) #rgb(83, 141, 78)
LOOSE_COLOR = color_palette3[2] #rgb(178, 80, 104)
LETTER_CARD_SIZE = 65
LETTER_FONT_SIZE = 50
CARD_OUTLINE_THICKNESS = 3
OUTLINE_ALPHA = 50
NORMAL_ALPHA = 255
POST_GAME_ALPHA = 100
WORD_SIZE = 5
WORD_FILE = 'data/wordle_data/words'
TRYS = 6
#-------------------


#------ TICTACTOE ------
#-----------------------