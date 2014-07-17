#Tyler Robbins
#7/16/14
#Sprites
#A place to store all of the sprite classes

import pygame.sprite,random
from constants import *
from basic import surf_center,clear_b

x = 20
y = 25

class Spritey(pygame.sprite.Sprite):
	'''Sprite class that defines some basic methods'''
	def __init__(self,x,y,num,life=3):
		pygame.sprite.Sprite.__init__(self)

		if num is 1: 	self.pos = START_POS_1
		elif num is 0: 	self.pos = START_POS_2
		else:			self.pos = num

		print self.pos

		self.image = pygame.Surface((10,10),pygame.SRCALPHA,32)

		######Rectangular hitbox of sprite######
		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]
		self.life = life
		self.start = self.pos

		pygame.draw.circle(self.image,RED,(5,5),5)

	def shoot(self,group):
		######Generic sprite shooting######
		b = bullet(x,y,(self.rect.x,self.rect.y-30),'75'.join(IMG),(0,-30))
		group.add(b)

	def setLife(self,life): self.life += life

	def setPos(self,pos):
		self.pos = pos
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

	def drawSprite(self,surface):
		pos = surf_center(self.sprite,self.image)
		pos[0] = self.rect.x - pos[0]
		pos[1] = self.rect.y - pos[1]

		self.gRect = pygame.Rect(pos,self.sprite.get_size())

		surface.blit(self.sprite,pos)

	def update(self,speed):
		######Generic sprite position updater######
		self.rect.x += speed[0]
		self.rect.y += speed[1]

class Player(Spritey):
	def __init__(self,x,y,num,maxs,sprite,life):
		Spritey.__init__(self,x,y,num,life=life)
		self.power = 	0
		self.grazep = 	0
		self.power = 	1
		self.maxBombs = 4
		self.maxLife = 	10
		self.maxPower = 300

		self.bombs = self.maxBombs

		self.bombing = 	False
		self.god = 		False
		
		self.default =	maxs
		self.focus = 	maxs/2
		self.speed = 	self.default
		
		self.sprite = 	loadImage(sprite)

		self.death_time = 	0
		self.score = 		0

		self.playerbomb = 	False

	def update(self,direction):
		self.rect.x += direction[0]
		self.rect.y += direction[1]

		if self.rect.x <= 0: 									self.rect.x += self.speed #LEFT
		if self.rect.x >= (OVERLAX-self.image.get_width()): 	self.rect.x -= self.speed #RIGHT
		if self.rect.y >= (OVERLAY-self.image.get_width()): 	self.rect.y -= self.speed #BOTTOM
		if self.rect.y <= 0: 									self.rect.y += self.speed #TOP

	def bomb(self,font,surf,group1,group2):
		#5 large red orbs rain from above. Once all have hit the ground, a large white laser shoots up the middle ofthe screen.
		name = "Origin Sign: Red Rain"
		name = font.render(name,True,BLACK)

		# if name not in messages:
		# 	namepos = (0, surf.get_height()-(name.get_height()+5))
		# 	messages[name] = namepos
		# namepos = (0, surf.get_height()-(name.get_height()+5))

		# dispText("Origin Sign: Red Rain",overlay,namepos)
		
		# self.bombing = True

		# self.playerbomb = False
		# print self.bombing

		if not self.bombing:
			self.bombs -= 1
			# print ":",self.bombing
			for b in range(5):
				x1 = random.randint(boss.rect.x-100,boss.rect.x+100)

				b = bullet(x,y,(x1,0),'76'.join(IMG),(0,5),playerb=True)
				group1.add(b)

			self.bombing = True
			# print ">",self.bombing

		if len(group1.sprites()) <= 0:
			print "running"
			self.playerbomb = False

			self.god = 			False
			focus = 			False
			# bomb_fin = 			True

			self.bombing = False

			# del messages[name]

			clear_b(group1)
			clear_b(group2)
			
			# start = surf_center(boss.image,loadImage('img_laser1.png'))
			# start[1] = OVERLAY-loadImage('img_laser1.png').get_height()
			# l = laser(x,y,start,1,'img_laser1.png',[0,0],playerb=True)
			# bombBullet.add(l)

		# return fontObj.render(name,True,BLACK)

	def setFocus(self,shift):
		if shift:
			self.speed = self.focus
			if not self.bombing: pygame.draw.circle(self.image,RED,(5,5),5)
		else:
			self.speed = self.default
			del self.image
			self.image = pygame.Surface((10,10),pygame.SRCALPHA,32)

	def getPower(self):
		if self.power >= self.maxPower: return "MAX"
		else: 							return self.power

	def setPower(self,point):
		if point.lower() == "max": 	self.power = self.maxPower
		else: 						self.power += point

	def kill(self):
	 	self.god = True
	 	self.setLife(-1)
		self.bombs = self.maxBombs
	 	self.setPos([posx,overlay.get_height()-5])
	 	self.death_time = float(pygame.time.get_ticks())/1000

	 	playSound('playerdeath.ogg')

	def shoot(self,group):
		bullet_list = []

		if self.power >= self.maxPower:
			x1 = self.rect.x - (self.sprite.get_width()/2)
			x2 = self.rect.x + (self.sprite.get_width()/2)
			x3 = self.rect.x + 10
			x4 = self.rect.x - 10

			b = bullet(x,y,(x1,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)
			b2 = bullet(x,y,(x2,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)
			b3 = bullet(x,y,(x3,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)
			b4 = bullet(x,y,(x4,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)


			bullet_list.append(b)
			bullet_list.append(b2)
			bullet_list.append(b3)
			bullet_list.append(b4)

		elif self.power >= ((self.maxPower/4) * 3):
			x1 = self.rect.x - (self.sprite.get_width()/2)
			x2 = self.rect.x + (self.sprite.get_width()/2)
			x3 = self.rect.x

			b = bullet(x,y,(x1,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)
			b2 = bullet(x,y,(x2,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)
			b3 = bullet(x,y,(x3,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)

			bullet_list.append(b)
			bullet_list.append(b2)
			bullet_list.append(b3)

		elif self.power >= (self.maxPower/2):
			x1 = self.rect.x - (self.sprite.get_width()/2)
			x2 = self.rect.x + (self.sprite.get_width()/2)
			
			b = bullet(x,y,(x1,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)
			b2 = bullet(x,y,(x2,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)
			
			bullet_list.append(b)
			bullet_list.append(b2)

		else:
			x1 = self.rect.x

			b = bullet(x,y,(x1,self.rect.y-30),'75'.join(IMG),(0,-30),playerb=True)
			
			bullet_list.append(b)

		group.add(bullet_list)

	def graze(self,bgroup):
		# for i in bossBullet.sprites():
		# 	if i.gRect.colliderect(self.rect) and not i.rect.colliderect(self.rect):
		# 		self.grazep += 1
		# 		return 100

		# return 0

		for i in bgroup.sprites():
			if i.gRect.colliderect(self.rect) and not i.rect.colliderect(self.rect) and not i.grazed:
				#For some reason, graze points are increasing by two
				self.grazep += 1
				# self.grazep -= 1
				i.grazed = True
				self.score += 100

		return 0

class bullet(Spritey):
	def __init__(self,x,y,num,img,speed,playerb=False):
		Spritey.__init__(self,x,y,num)

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

class boss(Spritey):
	def __init__(self,x,y,num,img,life=100,lives=1):
		Spritey.__init__(self,x,y,num,life=life)
		self.lives = lives

		self.spell = 1

		self.spells = [self.shoot]

		self.image = loadImage(img)

		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

		self.maxLife = life

		self.last_time = pygame.time.get_ticks()

		self.pwr = {'p':0}

		self.clife = 0

		self.lifes = [self.maxLife]

		self.spellTimer = Timer(2500)

		# self.spellTimer.startTimer()

		self.last_time = pygame.time.get_ticks()/1000

	def shoot(self,atak,group):
		#Fire a bullet every second
		self.spellTimer.timer()
		if pygame.time.get_ticks()/1000 - self.last_time >= 1:
			self.last_time = pygame.time.get_ticks()/1000
			
			for i in range(atak):
				start = surf_center(self.image,loadImage('img-77.png'))
				start[0] += self.rect.x
				start[1] += self.rect.y

				if i is 1:
					b = bullet(x,y,start,'img-77.png',(0,5))
				elif i is 2:
					b = bullet(x,y,start,'img-77.png',(0,-5))
				elif i is 3:
					b = bullet(x,y,start,'img-77.png',(-5,0))
				elif i is 4:
					b = bullet(x,y,start,'img-77.png',(5,0))
				else:
					b = bullet(x,y,start,'img-77.png',(0,5))

				group.add(b)

	def dispLife(self,surface):
		start = (5*self.lives,5)
		# end = ((5*self.lives)+(self.life/2),5)
		# end = ((5*self.lives)+(self.life/(self.life/OVERLAX)),5)
		# end = (start[0] + (OVERLAX-(self.life/OVERLAX)),5)
		percent = float(self.life)/float(self.maxLife)
		end = (start[0] + float(HEALTH_BAR*percent),5)

		pygame.draw.line(surface,BLUE,start,end,3) #Boss health bar

	def kill(self):
		self.clife += 1

		self.maxLife = self.lifes[self.clife]

		self.lives -= 1
		self.spell += 1
		clear_b(bossBullet)
		self.setLife(-(0-self.life) + self.maxLife)

		for i in self.pwr:
			newPos = (random.randint(self.rect.x-20,self.rect.x+20),self.rect.y)
			if i == 'p':
				p = Powerup(self.pos[0],self.pos[1],newPos,self.pwr[i])
				powerGroup.add(p)

			elif i == 's':
				s = PointItem(self.pos[0],self.pos[1],newPos)
				scoreGroup.add(s)

			elif i == 'l':
				l = Lifeup(self.pos[0],self.pos[1],newPos)
				lifeGroup.add(l)

			elif i == 'b':
				b = Bombup(self.pos[0],self.pos[1],newPos)
				bombupGroup.add(b)

			else:
				print "ItemError: Invalid token '" + i + "'"

		self.spellTimer.startTimer()

		return True

	def attack(self,group,args=None):
		if args == []:
			self.spells[self.spell-1](group)
		else:
			self.spells[self.spell-1](args,group)

class dot_boss(boss):
	def __init__(self,x,y,num,life,lives,speed):
		boss.__init__(self,x,y,num,"Boss-1.png",life=life,lives=lives)
		self.speed = speed

		self.spells.append(self.spell1)

		self.pwr = {'p':0,'p':1,'s':0,'p':0}

		self.lifes.append(1500)

	def spell1(self,speed,group):
		self.spellTimer.setMax(30000)
		if self.spellTimer.isFinished():
			self.kill()

		self.spellTimer.timer()

		self.pwr = {'p':0,'p':1,'s':0,'p':0,'p':1,'l':0}

		name = 				 fontObj.render("EX Sign: Generic Danmaku",True,BLACK)
		pos = 				(overlay.get_width()-(name.get_width()+5),10)
		messages[name] =	 pos

		self.speed = 		[0,0]

		newPos = [surf_center(overlay,self.image)[0],10]

		if self.rect.x < newPos[0]: self.rect.x += speed
		if self.rect.x > newPos[0]: self.rect.x -= speed
		if self.rect.y < newPos[1]: self.rect.y += speed
		if self.rect.y > newPos[1]: self.rect.y -= speed

		spawn2 = [0,0]
		spawn3 = [OVERLAX-40,0]
		self.shoot(5)

		ctime = float(pygame.time.get_ticks())/1000 - float(self.last_time)/1000

		if ctime >= 0.3:
			b2 = bullet(x,y,spawn2,'img-77.png',(5,5))
			b = bullet(x,y,spawn3,'img-77.png',(-5,5))

			self.last_time = pygame.time.get_ticks()

			group.add(b)
			group.add(b2)

	def update(self):
		self.rect.x += self.speed[0]
		self.rect.y += self.speed[1]

		if self.rect.x <= 0:
			self.speed[0] *= -1
			self.rect.x += self.speed[0]
		if self.rect.x >= (OVERLAX-self.image.get_width()): 
			self.speed[0] *= -1
			self.rect.x += self.speed[0]
		if self.rect.y >= (OVERLAY-self.image.get_width()):
			self.speed[1] *= -1
			self.rect.y += self.speed[1]
		if self.rect.y <= 0:
			self.speed[1] *= -1
			self.rect.y += self.speed[1]

class laser(bullet):
	def __init__(self,x,y,num,life,img,speed,playerb=False):
		bullet.__init__(self,x,y,num,img,speed,playerb=playerb)
		self.life = life
		self.birth = pygame.time.get_ticks()

	def kill(self,ctime):
		if not self.life == -1:
			if (float(ctime)/1000) - (float(self.birth)/1000) >= self.life:
				if self.playerb:
					all_bullets.remove(self)
					playerBullet.remove(self)

				else:
					all_bullets.remove(self)
					playerBullet.remove(self)

				del self

class Item(Spritey):
	def __init__(self,x,y,num,img):
		Spritey.__init__(self,x,y,num)
		
		self.image = img

		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

		self.speed = 3

		self.ystart = self.pos[1] + 10
		self.down = False

	def update(self):
		if self.rect.y >= self.ystart:
			if not self.down: 	self.rect.y -= self.speed
			else: 				self.rect.y += self.speed

		if self.rect.y <= self.ystart:
			self.down = True
			self.rect.y += self.speed

class PointItem(Item):
	def __init__(self,x,y,num):
		Item.__init__(self,x,y,num,SCORE_IMG)
		self.sscore = 1000

class Powerup(Item):
	def __init__(self,x,y,num,size):

		if size < 0 or size > 1:
			print "Incorrect size!"
			return None

		self.pscore = (size*10)

		if self.pscore <= 0: self.pscore = 1

		if size is 0: 	img = POWER0_IMG
		else: 			img = POWER1_IMG

		Item.__init__(self,x,y,num,img)

class Lifeup(Item):
	def __init__(self,x,y,num):
		Item.__init__(self,x,y,num,LIFE_UP_IMG)

	def collect(self):
		player.life += 1
		playSound("lifeup.ogg")

class Bombup(Item):
	def __init__(self,x,y,num):
		Item.__init__(self,x,y,num,BOMB_UP_IMG)

	def collect(self):
		player.bomb += 1
		playSound("bombup.ogg")

#NOTE: The Timer class isn't actually supposed to be in this file
# I just haven't figured out a place to put it yet, and the program fails without it.
# Please remember to move Timer to some other file

class Timer(object):
	def __init__(self,maxTime):
		"""Timer class that returns True when finished
		maxTime = time in milliseconds before ending
		"""
		self.clock = pygame.time.Clock()

		self.maxTime = maxTime
		self.timing = False
		self.lastTime = 0
		self.timed = 0
		self.finished = False

	def startTimer(self):
		self.reset()
		self.timing = True
		self.lastTime = pygame.time.get_ticks()

		print self.timing

	def timer(self):
		ctime = pygame.time.get_ticks()

		if self.timing:
			if ctime-self.lastTime >= 1:
				self.timed += 1
				self.lastTime = ctime

			if self.timed >= self.maxTime:
				self.finished = True

	def dispTime(self,pos,surf,font,color=BLACK,cutoff=0):
		time = float(self.maxTime - self.timed)/1000
		time = str(time)

		if len(str(time)) <= 3:
			time = str(0) + time

		if cutoff:
			time = time[:-cutoff]

		ftime = font.render(str(time),True,color)
		surf.blit(ftime,pos)

	def setMax(self,newMax):
		self.maxTime = newMax

	def reset(self):
		self.timing = False
		self.timed = 0
		self.finished = False
		self.lastTime = pygame.time.get_ticks()
		print "RESET"

	def getTime(self):
		return self.timed

	def isFinished(self):
		return self.finished

nuclear = u'\u2622'