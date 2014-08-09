#Tyler Robbins
#7/16/14
#Constants
#Holds constant variables for the game

from settings import *

playerSpeed = getSetting("playerSpeed")

############
#FILE PATHS#
############
log_path = 		getSetting("path_log")
font_path = 	getSetting("path_font")
image_path = 	getSetting("path_image")
sound_path = 	getSetting("path_sound")
music_path = 	getSetting("path_music")

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

#MAX-SIZE of the game overlay
OVERSIZE =		(SCREEN_SIZE[0]-300,SCREEN_SIZE[1]-50)
OVERLAX = 		OVERSIZE[0]
OVERLAY =		OVERSIZE[1]

#Position of the game overlay
OVERPOS = 		(10,20)

HEALTH_BAR = 	OVERLAX-30
START_POS_1 = 	(1,1)
# START_POS_2 = 	((OVERLAX-1)-loadImage("player.png").get_width(),1) #<-- makes sure the image doesn't start offscreen
# print START_POS_2
DIRECTION1 = 	[0,0] #boss movement

FPS = 			60
HI = 			0 #HI-Score, thscore.dat


nuclear = u'\u2622'