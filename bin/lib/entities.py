# Tyler Robbins
# 8/19/14
# Entities
# Store all sprites/entities so that all files can access them

from globalVar import *
from constants import *
from sprites import *
from players import *
from bosses  import *

##########
# PLAYER #
##########

player = Alraune([posx,OVERLAY-5])
playerGroup.add(player)

##########
# BOSSES #
##########

#Set the boss's life to any positive integer, but I'm leaving it at 100 right now for testing
# Note: Setting it to a negative integer means an instant win
boss = VivianJames([posx,40],life=100,lives=3)
bossGroup.add(boss)

for s in bossGroup.sprites():
	all_sprites.add(s)
for s in playerGroup.sprites():
	all_sprites.add(s)

nuclear = u'\u2622'