#Tyler Robbins
#8/7/14
#Globals
# A file holding all global variables. Similar to constants

import pygame,os
from settings import *
from constants import *

#Need to initialize this so that we can have access to fonts from anywhere
pygame.font.init()

speed = 		getSetting("playerSpeed")
playerdamage =	getSetting("playerDmg")

messages = 		{} #{<fontObj>:<pos>} <-- This may be deprecated soon...
bomb_name = 	""

fps = 		pygame.time.Clock()
overlay = 	pygame.Surface(OVERSIZE)
screen = 	pygame.display.set_mode(SCREEN_SIZE)
talks = 	open("thcut.dat",'r').read().split("NBOSS")

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
current_boss = 	0
current_playr = getSetting("player")

d_move = False
u_move = False
l_move = False
r_move = False

posx = (OVERLAX/2)-5

bombBullet = 	pygame.sprite.Group()
all_bullets = 	pygame.sprite.Group()
scoreGroup = 	pygame.sprite.Group()
powerGroup =	pygame.sprite.Group()
lifeGroup = 	pygame.sprite.Group()
bombupGroup =	pygame.sprite.Group()
itemGroup = 	pygame.sprite.Group()

playerGroup = 	pygame.sprite.Group()
enemyGroup =	pygame.sprite.Group()
bossGroup = 	pygame.sprite.Group()
all_sprites =	pygame.sprite.Group()

nuclear = u'\u2622'