# Tyler Robbins
# 9/8/14
# Enemies
# Define the classes for all enemies.

from sprites import *
from spellcards import *
from dependencies import *

class VivianJames(boss):
	def __init__(self,num,life,lives):
		boss.__init__(self,num,BOSS11_IMG,"th00_02.ogg",life=life,lives=lives)
		self.speed = [0,0]

		spell1 = LargeEX(self,self.bulletGroup)

		self.spells.append(spell1)

nuclear = u'\u2622'