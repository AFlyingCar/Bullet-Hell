# Tyler Robbins
# 9/8/14
# Players
# Define all custom player classes

from sprites import Player
from dependencies import *

class Alraune(Player):
	def __init__(self,num):
		Player.__init__(self,num,5,PLAYER1_IMG,2)

nuclear = u'\u2622'