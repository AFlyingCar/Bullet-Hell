# Tyler Robbins
# 9/5/14
# bullets
# Store all bullets in a separate file

import pygame
from Spritey import *
from dependencies import *

class Bullet(Spritey):
	def __init__(self,num,img,speed,playerb=False):
		Spritey.__init__(self,num,life=1)

		self.sprite = loadImage(img)

		size = [int(self.sprite.get_width()/2)-5,int(self.sprite.get_height()/2)-5]

		if size[0] <= 0: size[0] = 0 + 5
		if size[1] <= 0: size[0] = 0 + 5

		if playerb: size = self.sprite.get_size()

		self.image = pygame.Surface(size,pygame.SRCALPHA,32)
		# self.image = pygame.Surface(size)

		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]
		self.speed = speed

		self.gRect = pygame.Rect((0,0),self.sprite.get_size())

		self.playerb = playerb

		self.grazed = False

	def update(self):
		self.rect.x += self.speed[0]
		self.rect.y += self.speed[1]

	def turn(self,degrees):
		'''This will allow a bullet to turn by a certain amout of degrees, changing it's direction and speed.'''
		pass

class circleShot(Bullet):
	def __init__(self,pos,speed,playerb=False):
		Bullet.__init__(self,pos,BULL2,speed,playerb=playerb)

class needleShot(Bullet):
	def __init__(self,pos,speed,playerb=False):
		Bullet.__init__(self,pos,BULL1,speed,playerb=playerb)

class genericLaser(Bullet):
	def __init__(self,pos,img,playerb=False):
		bullet.__init__(self,pos,img,speed=0,playerb=playerb)

nuclear = u'\u2622'