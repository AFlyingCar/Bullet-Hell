#Tyler Robbins
#8/20/14
#Spellcards
#Define all usable spell cards

from basic import *
# from sprites import *
from globalVar import *
from constants import *
from timerv2 import *

class SpellCard(object):
	def __init__(self,time,name,owner,ownerGroup):
		self.start = 	False
		self.name = 	name
		self.time = 	time

		self.timer = 	Timer(time)

		self.owner = 		owner
		self.ownerGroup = 	ownerGroup

	def runCard(self):
		if not self.start:
			self.start = True
			self.timer.startTimer()
		# else:
		self.Card()
		self.timer.stopTimer()
		if self.timer.isFinished():
			self.owner.kill()
			self.stopCard()
		# self.timer.timer() # <- This cannot be run with the new timer

	def Card(self):
		'''This will spawn bullets when SpellCard is called'''
		pass

	def isStart(self):
		return self.start

	def getName(self):
		return self.name

	def dispName(self,pos,color=BLACK):
		namee = fontObj.render(self.name,True,color)
		overlay.blit(namee,pos)

	def ChangeBKG(self,img):
		# '''Don't know how to successfully use this yet, so I'm leaving it blank for now'''
		# overlay.blit(img,(0,0))
		return img

	def idle(self):
		pass

	def stopCard(self):
		self.start = False
		# self.timer.pauseTimer()
		self.timer.reset()

	def changeOwnerPos(self,speed,newPos):
		if self.owner.rect.x < newPos[0]: self.owner.rect.x += speed
		if self.owner.rect.x > newPos[0]: self.owner.rect.x -= speed
		if self.owner.rect.y < newPos[1]: self.owner.rect.y += speed
		if self.owner.rect.y > newPos[1]: self.owner.rect.y -= speed

	def dispTime(self,pos,surf,font,cutoff=0,count=0):
		self.timer.dispTime(pos,surf,font,cutoff=cutoff)

class LargeEX(SpellCard):
	def __init__(self,owner,ownerGroup,playerb=False):
		SpellCard.__init__(self,30000,"Large X: Generic Danmaku",owner,ownerGroup)

		self.spawn2 = [0,0]
		self.spawn3 = [OVERLAX-40,0]
		# self.ctime = float(pygame.time.get_ticks())/1000 - float(self.last_time)/1000
		self.ctime = self.timer.getTimePassed()

		self.spellBKG = loadImage("SpellBKG.png",fail_size=OVERSIZE)

		self.playerb = playerb

	def Card(self):
		# self.shoot(5,group,surf)
		if self.start:
			name_size = fontObj.render(self.name,True,BLACK).get_width()
			pos = (OVERLAX-(name_size+5),10)
			self.dispName(pos)
			# self.ctime = float(pygame.time.get_ticks())/1000 - float(self.last_time)/1000
			self.ctime = self.timer.getTimePassed()

			if self.ctime >= 0.3:
				b2 = circleShot(spawn2,(5,5),self.playerb)
				b = circleShot(spawn3,(-5,5),self.playerb)

				self.last_time = pygame.time.get_ticks()

				self.ownerGroup.add(b)
				self.ownerGroup.add(b2)

	def idle(self):
		self.runCard()
		# self.Card()
		# self.timer.timer()

		return self.ChangeBKG(self.spellBKG)

	def getBGroup(self):
		return self.ownerGroup

nuclear = u'\u2622'