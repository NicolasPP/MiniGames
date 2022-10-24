from color.color_palettes import color_palette2, color_palette3, color_palette1


# ------ GENERAL ------
GAME_BG : 		tuple[int, int, int] = color_palette2[0] #rgb(44, 54, 57)
PAUSE_COLOR : 	tuple[int, int,int] = (255, 255, 255) #rbg(255, 255, 255)
SCORE_COLOR : 	tuple[int, int, int] = color_palette3[3] #rgb(231, 171, 121)
LOOSE_COLOR : 	tuple[int, int, int] = color_palette3[1] #

PAUSE_ALPHA : 	int = 15 # 0 is fully transparent and 255 fully opaque.
LOOSE_ALPHA : 	int = 75
ALPHABET : 		str = 'abcdefghijklmnopqrstuvwxyz'
#----------------------


#------ SNAKE ------
S_CELL_SIZE : 			int = 10

SNAKE_COLOR : 			tuple[int, int, int] = color_palette2[3] #rgb(220, 215, 201)
FOOD_COLOR : 			tuple[int, int, int] = color_palette3[3] #rgb(231, 171, 121)

PAUSE_FONT_SIZE : 		int = 50
SCORE_FONT_SIZE : 		int = 40


	# time (ms)
FOOD_SPAWN_DELAY :  	float = 5000
SNAKE_MOVE_FREQ : 		float = 250
ALPHA_CHANGE : 			int = 700
TIME_TO_COVER_CELL :    float = 150
#-------------------


#------ WORDLE ------
LETTER_OUTLINE_COLOR : 			tuple[int, int, int] = color_palette3[3]#rgb(231, 171, 121)
BLANK_COLOR : 					tuple[int, int, int] = color_palette2[0]#rgb(44, 54, 57)
FILLED_COLOR : 					tuple[int, int, int] = color_palette2[0]#rgb(44, 54, 57)
PRESENT_OUT_OF_PLACE_COLOR : 	tuple[int, int, int] = (181, 159, 59) #rgb(181, 159, 59)
PRESENT_IN_PLACE_COLOR : 		tuple[int, int, int] = (83, 141, 78) #rgb(83, 141, 78)
NOT_PRESENT_COLOR : 			tuple[int, int, int] = (58, 58, 60) #rgb(58, 58, 60)
LETTER_COLOR : 					tuple[int, int, int] = color_palette2[3] #rgb(220, 215, 201)
WON_COLOR : 					tuple[int, int, int] = (83, 141, 78) #rgb(83, 141, 78)

LETTER_CARD_SIZE : 				int = 65
LETTER_FONT_SIZE : 				int = 50
CARD_OUTLINE_THICKNESS :		int = 3
OUTLINE_ALPHA : 				int = 50
NORMAL_ALPHA : 					int = 255
POST_GAME_ALPHA : 				int = 100
WORD_SIZE : 					int = 5
WORD_FILE : 					str = 'data/wordle_data/words'
TRYS : 							int = 6
#-------------------


#------ TICTACTOE ------
#-----------------------