# Tyler Robbins
# 8/7/14
# Dependencies
# Image and sound dependencies

from basic import loadImage,loadSound
from pygame.mixer import init

#We load images and sounds before-hand so that less memory is used up trying to constantly reference
# the image/sound files

########
#IMAGES#
########
LIFE_IMG = 		loadImage("img-79.png")
BOMB_IMG = 		loadImage("img-78.png")
LIFE_UP_IMG = 	loadImage("img_1-up.png")
SCORE_IMG = 	loadImage("img_score.png")
BOMB_UP_IMG = 	loadImage("img_bomb-up.png")
STARPOINT_IMG = loadImage("img_starpoint.png")
POWER0_IMG = 	loadImage("img_power-0.png")
POWER1_IMG = 	loadImage("img_power-1.png")
S_BKG = 		loadImage("img-s_bkg.png")

	#########
	#Bullets#
	#########
BULL1 = 		loadImage("img-75.png")
BULL2 = 		loadImage("img-77.png")
BULL3 = 		loadImage("img-76.png")

#This is to make sure that the mixer loads so that
# loadSound doesn't ask the user for confirmation to continue
init(frequency=22050, size=-16, buffer=500)

########
#SOUNDS#
########
P_DEATH_S = 	loadSound("playerdeath.ogg")
PICKUP_S = 		loadSound("pickup.ogg")
LIFE_UP_S = 	loadSound("lifeup.ogg")
BOMB_UP_S = 	loadSound("bombup.ogg")

nuclear = u'\u2622'