#Tyler Robbins
#7/16/14
#Constants
#Holds constant variables for the game

from basic import loadImage,loadSound

########
#COLORS#
########
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = 	(255,0,0)
BLUE = 	(0,0,255)

#####################
#SIZES AND POSITIONS#
#####################

IMG = 			('img-','.png')
SCREEN_SIZE = 	(640,480)
OVERSIZE =		(SCREEN_SIZE[0]-300,SCREEN_SIZE[1]-50)
OVERLAX = 		OVERSIZE[0]
OVERLAY =		OVERSIZE[1]
HEALTH_BAR = 	OVERLAX-30
OVERPOS = 		(10,20)
START_POS_2 = 	((OVERLAX-1)-loadImage("player.png").get_width(),1) #<-- makes sure the image doesn't start offscreen
START_POS_1 = 	(1,1)
DIRECTION1 = 	[0,0] #boss movement

#We load images and sounds before-hand so that less memory is used up trying to constantly reference
# the image/sound files

########
#IMAGES#
########
LIFE_IMG = 		loadImage("79".join(IMG))
BOMB_IMG = 		loadImage("78".join(IMG))
LIFE_UP_IMG = 	loadImage("img_1-up.png")
SCORE_IMG = 	loadImage("img_score.png")
BOMB_UP_IMG = 	loadImage("img_bomb-up.png")
POWER0_IMG = 	loadImage("img_power-0.png")
POWER1_IMG = 	loadImage("img_power-1.png")
S_BKG = 		loadImage("s_bkg".join(IMG))

# pygame.mixer.init()

########
#SOUNDS#
########
P_DEATH_S = 	loadSound("playerdeath.ogg")
PICKUP_S = 		loadSound("pickup.ogg")

nuclear = u'\u2622'