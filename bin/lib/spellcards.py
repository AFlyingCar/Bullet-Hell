#Tyler Robbins
#8/20/14
#Spellcards
#Define all usable spell cards

import pygame

from basic import *
from enemies import *
from bullets import *
from timerv2 import *
from fontlib import *
from patterns import *
from globalVar import *
from constants import *
from dependencies import *

class SpellCard(object):
	def __init__(self,time,name,owner,ownerGroup,playerb=False,newMaxLife=1000):
		'''A generic spellcard class that will spawn bullets in a pre-defined pattern
		   time 		<- How long is the spellcard supposed to last in milliseconds (i.e: 30 seconds = 30000 milliseconds)
		   owner 		<- The owner of the spellcard. (i.e: boss, player, fairy1, etc.).
		   ownerGroup 	<- The bullet group of the owner (i.e: bossBullet, playerBullet, etc.)
		   name="" 		<- The name of the spellcard. This is optional, and will default to empty string.
		'''
		self.start = 	False #Does not start until runCard is called
		self.name = 	name  #Name of spellcard
		self.time = 	time
		self.namepos = 	None
		self.timepos = 	(OVERLAX/2-20,5)

		self.timer = 	Timer(time)

		self.owner = 		owner
		self.ownerGroup = 	ownerGroup

		self.playerb = playerb

		self.spellBKG = pygame.Surface(overlay.get_size())
		self.spellBKG.fill(WHITE)

		self.ctime = 		float(pygame.time.get_ticks())/1000
		self.last_time = 	self.ctime

		self.owner.speed = [3,0]

		self.newMax = newMaxLife

		self.drops = ["p1","p2","l","s","b"]

		self.running = False

	def runCard(self):
		'''This will begin the spellcard when called for the first time. It must be continuously called by idle.'''
		if not self.start:
			self.start = True
			self.running = True
			self.timer.startTimer()

		if self.running:
			self.Card()

		self.timer.stopTimer()

		if self.timer.isFinished():
			self.owner.kill(True)
			self.stopCard()

	def Card(self):
		'''This defines what bullets to spawn and when, and must be overwritten by custom spellcards.'''
		if self.start:
			# self.ctime = (self.timer.getTimePassed()/1000) - self.last_time
			self.ctime = pygame.time.get_ticks()/1000-self.last_time

			if self.ctime >= 1:
				self.last_time = pygame.time.get_ticks()/1000

				for i in range(4):
					start = surf_center(self.owner.image,BULL2)
					start[0] += self.owner.rect.x
					start[1] += self.owner.rect.y

					if i is 0:
						b = circleShot(start,(0,-5))
					elif i is 1:
						b = circleShot(start,(0,5))
					elif i is 2:
						b = circleShot(start,(-5,0))
					elif i is 3:
						b = circleShot(start,(5,0))

					self.ownerGroup.add(b)

	def isStart(self):
		'''Return if the spellcard has been started.'''
		return self.start

	def getName(self):
		'''Return spellcard name as a string.'''
		return self.name

	def dispName(self,pos,color=BLACK):
		'''Display the spellcard name on the overlay.'''
		name = 		wrapline(self.name,FONT_THSPATIAL,overlay,pos)
		ystart = 	pos[1]

		for n in name:
			namee = FONT_THSPATIAL.render(n,True,color)

			overlay.blit(namee,(pos[0],ystart))
			ystart += namee.get_height()

	def idle(self):
		'''Default idle method. Can be overwritten for custom content.'''
		self.runCard() #Run spellcard

		self.renderInfo(self.timepos,overlay,FONT_THSPATIAL) #Render name and time

		return self.spellBKG #Return the custom background of the spellcard

	def stopCard(self):
		'''End the spellcard if it hasn't already'''
		if self.start:
			self.running = False
			self.start = False
			self.timer.forceStop()
			self.timer.reset()

	def changeOwnerPos(self,speed,newPos):
		'''Change the position of the owner. Will move the owner incrementally if they are not already there.'''
		if self.owner.rect.x < newPos[0]: self.owner.rect.x += speed
		if self.owner.rect.x > newPos[0]: self.owner.rect.x -= speed
		if self.owner.rect.y < newPos[1]: self.owner.rect.y += speed
		if self.owner.rect.y > newPos[1]: self.owner.rect.y -= speed

	def dispTime(self,pos,surf,font,color=BLACK,cutoff=0,count=0):
		'''Display current time.'''
		self.timer.dispTime(pos,surf,font,color=color,cutoff=cutoff,count=count)

	def renderInfo(self,pos,surf,font,color1=BLACK,color2=BLACK):
		self.dispTime(pos,surf,font,color=color1,cutoff=1,count=0)

		fsize = self.timer.getTimeFont(font).get_size()

		pos2 = (pos[0]+fsize[0],pos[1])

		if not self.namepos:
			self.namepos = pos2

		self.dispName(self.namepos,color2)

	def getBGroup(self):
		'''Returns bullet group'''
		return self.ownerGroup

	def getDrops(self):
		'''Returns all items to drop'''
		return self.drops

	def getNewLife(self):
		'''Give the owner a new maximum life.'''
		self.owner.setMaxLife(self.newMax)

	def getSpellBKG(self):
		'''Get spellcard background.'''
		return self.spellBKG

	def getCardTime(self):
		'''Return the amount of time left on the spellcard's timer as a float.'''
		self.timer.getTimeLeft()

class servantSpawn(SpellCard):
	def __init__(self,owner,ownerGroup,playerb=False):
		SpellCard.__init__(self,40000,"LifeLong Servitude: Mystical Beasts",owner,ownerGroup,playerb=playerb,newMaxLife=1000)

		self.spellBKG = loadImage("SpellBKG.png",fail_size=OVERSIZE)
		self.timepos = 	(OVERLAX/2-20,5)

		self.drops = ['p2','p2','p2','p2','s','s','s']

		self.event1 = 0

	def Card(self):
		if self.start:
			name_size = FONT_THSPATIAL.render(self.name,True,BLACK).get_width()
			pos = (OVERLAX-(name_size+5),10)

			if not event1:
				newPos = [surf_center(overlay,self.owner.image)[0],10]
				self.changeOwnerPos(5,newPos)
				self.owner.speed = [0,0]
			else:
				if self.ctime - self.last_time >= 1:
					for i in (0,1):
						s = Fairy1((i*OVERLAX-FAIRY1_IMG.get_width(),OVERLAY/2),life=20)
						self.owner.servants.append(s)

class LargeEX(SpellCard):
	def __init__(self,owner,ownerGroup,playerb=False):
		SpellCard.__init__(self,30000,"Large X: Generic Danmaku",owner,ownerGroup,playerb=playerb,newMaxLife=1500)

		self.spawn2 =		[0,0]
		self.spawn3 =		[OVERLAX-40,0]
		self.timepos = 		(OVERLAX/2-20,5)

		self.spellBKG = loadImage("SpellBKG.png",fail_size=OVERSIZE)

		# self.drops = {'p1':0,'p2':0,'s':0,'p2':0}
		self.drops = ['p2','p2','s','p2']

		#EXPERIMENTAL: Events that can be triggered upon something either happening or changing in the environment
		self.event1 = 0
		self.event2 = 0
		self.event2_run = 0

	def Card(self):
		if self.start:
			newPos = [surf_center(overlay,self.owner.image)[0],10]
			
			self.changeOwnerPos(5,newPos)
			self.owner.speed = [0,0]

			name_size = FONT_THSPATIAL.render(self.name,True,BLACK).get_width()
			pos = (OVERLAX-(name_size+5),10)

			self.ctime = float(pygame.time.get_ticks())/1000

			#Every half a second...
			if self.ctime - self.last_time >= 0.5:
				#Spawn bullets from all four corners, forming an 'X' shape
				b2 = 	circleShot(self.spawn2,(5,5),self.playerb)
				b = 	circleShot(self.spawn3,(-5,5),self.playerb)

				self.ownerGroup.add(b)
				self.ownerGroup.add(b2)
				self.last_time = self.ctime

				self.event1 += 1

			if self.event1 >= 2:
				#Spawn a circle of 10 bullets, radiating out from the owner every 1 second
				amount = 	10
				speed = 	5
				ownerPos = 	self.owner.getCenterPos()

				x = circleSpawn(ownerPos,amount,speed,circleShot,playerb=self.playerb)
				for i in x:
					self.ownerGroup.add(i)

				self.event1 = 0
				self.event2 += 1

			if self.event2 >= 3:
				#Spawn 2 rows of bullets that travel downwards every 3 seconds
				xsize = self.ownerGroup.sprites()[0].getSpriteWidth() + 10
				ypos = OVERLAY/2

				amount = int(OVERLAX/xsize)

				shift = 20

				for i in reversed(xrange(amount)):
					pos = [xsize*i + shift,ypos]
					b = circleShot(pos,(0,2),self.playerb)
					self.ownerGroup.add(b)

				self.event2 = 0

class PlayerBomb(SpellCard):
	def __init__(self,owner,ownerGroup,name):
		'''Since player spellcards differ greatly from those of boss's, players require their own special spellcard class.'''
		SpellCard.__init__(self,0,name,owner,ownerGroup,playerb=True)

	def runCard(self):
		owner.makeGod()

		if self.running:
			self.Card()

	def Card(self):
		''''''
		pass

nuclear = u'\u2622'
