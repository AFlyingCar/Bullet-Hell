# Tyler Robbins
# 9/8/14
# Enemies
# Define the classes for all enemies.

from sprites import *
# from .sprites import Fairy
from dependencies import *

class Fairy(object):
	def __init__(self,num,img,life):
		pass

class Fairy1(Fairy):
	def __init__(self,pos,life=4):
		Fairy.__init__(self,pos,FAIRY1_IMG,life=life)

nuclear = u'\u2622'