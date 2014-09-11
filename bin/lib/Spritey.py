# Tyler Robbins
# 9/5/14
# Spritey
# Store Spritey in a separate file to avoid recursion issues with spellcards.py

import pygame
from constants import *
from basic import *

class Spritey(pygame.sprite.Sprite):
	'''Sprite class that defines some basic methods'''
	def __init__(self,num,life=3):
		pygame.sprite.Sprite.__init__(self)

		self.pos = num

		#We've got to make sure that we keep track of the start position
		self.start_pos = self.pos

		# print self.pos

		self.image = pygame.Surface((10,10),pygame.SRCALPHA,32)

		######Rectangular hitbox of sprite######
		self.rect = 	self.image.get_rect()
		self.rect.x = 	self.pos[0]
		self.rect.y = 	self.pos[1]

		self.spritePos = [0,0]

		self.life = 	life
		self.maxLife = 	life

		pygame.draw.circle(self.image,RED,(5,5),5)

		self.isDead = False
		self.showHB = False

		self.bulletGroup = pygame.sprite.Group()

	def shoot(self,group):
		######Generic sprite shooting######
		b = circleShot((self.rect.x,self.rect.y-30),(0,-30))
		group.add(b)

	def setLife(self,life):
		logging("Changing " + str(self) + "'s health from " + str(self.life) + " to " + str(life),"std")
		self.life = life

	def setMaxLife(self,life):
		logging("Max life changed from " + str(self.maxLife) + " to " + str(life),"std")
		self.maxLife = life

	def addLife(self,life):
		self.life += life
		if life > 0:
			logging(str(self) + " has gained a life!", "std", "Health is now " + str(self.life))

	def setPos(self,pos):
		self.pos = pos
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

	def getPos(self):
		x = self.rect.x
		y = self.rect.y
		return [x,y]

	def drawSprite(self,surface):
		pos = surf_center(self.sprite,self.image)
		pos[0] = self.rect.x - pos[0]
		pos[1] = self.rect.y - pos[1]

		self.spritePos = pos

		self.gRect = pygame.Rect(pos,self.sprite.get_size())

		surface.blit(self.sprite,self.spritePos)

	def update(self,speed):
		######Generic sprite position updater######
		self.rect.x += speed[0]
		self.rect.y += speed[1]

	def returnToStart(self):
		self.setPos(self.start_pos)

	def getIsDead(self):
		return self.isDead

	def idle(self):
		'''Stuff to run while the program is running. (E.X: Checking health)'''

		if self.life <= 0:
			self.kill()

	def kill(self):
		if self.life <= self.maxLife:
			# logging("Killing " + str(self) + "!", "std")
			for g in self.groups():
				g.remove(self)

			del self

	def uponDeath(self):
		'''Define an event to take place upon the final death of the sprite.
		This must be redefined for custom events.
		'''
		logging("Oh noes! I have died!","std")

	def followRect(self,rect):
		if self.rect.x < rect.x:
			self.rect.x += self.speed
		elif self.rect.x > rect.x:
			self.rect.x -= self.speed

		else: self.rect.x += 0

		if self.rect.y < rect.y:
			self.rect.y += self.speed
		elif self.rect.y > rect.y:
			self.rect.y -= self.speed

		else: self.rect.y += 0

	def addBullet(self,bullets=[]):
		for b in bullets:
			self.bulletGroup.add(b)

	def showHitBox(self,show=False):
		self.showHB = show

		if show:
			self.image.fill(BLACK)
		else:
			size = self.image.get_size()
			del self.image
			self.image = pygame.Surface(size,pygame.SRCALPHA,32)

nuclear = u'\u2622'