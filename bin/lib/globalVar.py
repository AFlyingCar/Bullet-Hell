#Tyler Robbins
#8/7/14
#Globals
# A file holding all global variables. Similar to constants
# 	NOTE: This is experimental, and may be deprecated in the future

import pygame,os
from constants import *

#Need to initialize this so that we can have access to fonts from anywhere
pygame.font.init()

speed = 		playerSpeed

messages = 		{} #{<fontObj>:<pos>} <-- This may be deprecated soon...
bomb_name = 	""

fps = 		pygame.time.Clock()
overlay = 	pygame.Surface(OVERSIZE)
screen = 	pygame.display.set_mode(SCREEN_SIZE)
talks = 	open("thcut.dat",'r').read().split("NBOSS")
fontObj =	pygame.font.Font(os.path.join(font_path,'THSpatial.ttf'),29)

direction2 = 	[0,0]
collide =		False
focus =			False
shoot = 		False
lose = 			False
win =			False
ctrl_hold = 	False
bomb_fin = 		True
x = 			20
y = 			25
cooldown = 		0
last_time = 	0

d_move = False
u_move = False
l_move = False
r_move = False

posx = (OVERLAX/2)-5

playerBullet = 	pygame.sprite.Group()
bossBullet = 	pygame.sprite.Group()
bombBullet = 	pygame.sprite.Group()
all_bullets = 	pygame.sprite.Group()
scoreGroup = 	pygame.sprite.Group()
powerGroup =	pygame.sprite.Group()
lifeGroup = 	pygame.sprite.Group()
bombupGroup =	pygame.sprite.Group()
itemGroup = 	pygame.sprite.Group()

playerGroup = 	pygame.sprite.Group()
bossGroup = 	pygame.sprite.Group()
all_sprites =	pygame.sprite.Group()

nuclear = u'\u2622'