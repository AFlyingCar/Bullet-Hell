# Tyler Robbins
# 9/5/14
# Spritey
# Store Spritey in a separate file to avoid recursion issues with spellcards.py

import pygame
from constants import *
from basic import *

class Spritey(pygame.sprite.Sprite):
	def __init__(self,num,life=3):
		'''Base sprite class.
		num 	<- integer. Starting position.
		life=3 	<- integer. Starting life of the sprite.
		'''
		pygame.sprite.Sprite.__init__(self)

		self.pos = num

		#We've got to make sure that we keep track of the start position
		self.start_pos = self.pos

		# print self.pos

		self.image = pygame.Surface((10,10),pygame.SRCALPHA,32)
		self.sprite= self.image

		######Rectangular hitbox of sprite######
		self.rect = 	self.image.get_rect()
		self.rect.x = 	self.pos[0]
		self.rect.y = 	self.pos[1]

		self.spritePos = [0,0,0]

		self.life = 	life
		self.maxLife = 	life

		pygame.draw.circle(self.image,RED,(5,5),5)

		self.isDead = False
		self.showHB = False

		self.bulletGroup = pygame.sprite.Group()

	def getSprite(self):
		'''Return the current sprite being used.'''
		return self.sprite

	def getSpriteWidth(self):
		'''Return the width of the sprite'''
		return self.sprite.get_width()

	def getSpriteHeight(self):
		'''Return the height of the sprite'''
		return self.sprite.get_height()

	def getImage(self):
		'''Return the image being displayed on-screen.'''
		return self.image

	def setSprite(self,newSprite):
		'''Set the current sprite to the Surface object newSprite.'''
		self.sprite = newSprite

	def getCenterPos(self,newSurface=None):
		'''Get the position in the center of the displayed sprite (A.K.A: self.image).'''
		if not newSurface:
			centerx = surf_center(self.image)[0] + self.rect.x
			centery = surf_center(self.image)[1] + self.rect.y
		else:
			centerx = surf_center(self.image,newSurface)[0] + self.rect.x
			centery = surf_center(self.image,newSurface)[0] + self.rect.y

		center = [centerx,centery]
		return center

	def shoot(self,group):
		'''Generic sprite shooting.
		Customize this for all sprites that extend from this class.'''
		b = circleShot((self.rect.x,self.rect.y-30),(0,-30))
		group.add(b)

	def setLife(self,life):
		'''Set the sprite's life to a new integer.
		life <- integer.'''
		logging("Changing " + str(self) + "'s health from " + str(self.life) + " to " + str(life),"std")
		self.life = life

	def setMaxLife(self,life):
		'''Change the sprite's maximum life to a new integer.
		life <- integer.'''
		logging("Max life changed from " + str(self.maxLife) + " to " + str(life),"std")
		self.maxLife = life

	def addLife(self,life):
		'''Add an integer to current life.
		life <- integer'''
		self.life += life
		if life > 0:
			logging(str(self) + " has gained a life!", "std", "Health is now " + str(self.life))

	def setPos(self,pos):
		'''Set the sprite's position.
		pos <- (x,y)'''
		self.pos = pos
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

	def getPos(self):
		'''Returns the current x,y position of the sprite.'''
		x = self.rect.x
		y = self.rect.y
		return [x,y]

	def drawSprite(self,surface):
		'''Draw the sprite to the specified surface.'''
		pos = surf_center(self.sprite,self.image)
		pos[0] = self.rect.x - pos[0]
		pos[1] = self.rect.y - pos[1]

		self.spritePos = pos

		self.gRect = pygame.Rect(pos,self.sprite.get_size())

		surface.blit(self.sprite,self.spritePos)

	def update(self,speed):
		'''Update sprite position based on its speed.
		speed <- (x,y)'''
		self.rect.x += speed[0]
		self.rect.y += speed[1]

	def returnToStart(self):
		'''Return to location the sprite was instantiated at.'''
		self.setPos(self.start_pos)

	def getIsDead(self):
		'''Return true if the sprite has lost all of its life, and false if the sprite's life is greater than 0.'''
		return self.isDead

	def idle(self):
		'''Run commands constantly.'''

		if self.life <= 0:
			self.kill()

	def kill(self):
		'''Run commands after the sprite has died.'''
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
		'''Change position based on the Rect rect's position
		rect <- pygame.Rect'''
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
		'''Add bullets to the sprite's bullet group.'''
		for b in bullets:
			self.bulletGroup.add(b)

	def showHitBox(self,show=False):
		'''Color in the normally invisible hitbox.'''
		self.showHB = show

		if show:
			self.image.fill(BLACK)
		else:
			size = self.image.get_size()
			del self.image
			self.image = pygame.Surface(size,pygame.SRCALPHA,32)

nuclear = u'\u2622'