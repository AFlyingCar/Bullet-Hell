#Tyler Robbins
#7/16/14
#Sprites
#A place to store all of the sprite classes

import pygame.sprite,random
from debugger import logging
from dependencies import *
from constants import *
from globalVar import *
from spellcards import *
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

		self.bulletGroup = pygame.sprite.Group()

	def shoot(self,group):
		######Generic sprite shooting######
		b = circleShot((self.rect.x,self.rect.y-30),(0,-30))
		group.add(b)

	def setLife(self,life):
		logging("Changing " + str(self) + "'s health from " + str(self.life) + " to " + str(life),"std")
		self.life = life

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

class Player(Spritey):
	def __init__(self,num,maxs,sprite,life):
		Spritey.__init__(self,num,life=life)
		self.power = 	0
		self.grazep = 	0
		self.power = 	1
		self.defBombs = 4
		self.maxBombs = 10
		self.maxLife = 	10
		self.maxPower = 300

		self.bombs = self.defBombs

		self.bombing = 	False
		self.god = 		False
		
		self.default =	maxs
		self.focus = 	maxs/2
		self.speed = 	self.default
		
		self.sprite = 	loadImage(sprite)

		self.death_time = 	0
		self.score = 		0

		self.playerbomb = 	False
		self.shooting = 	False

		self.pointColl = 	0
		self.maxPointColl = 1

		self.cLife 	   = 	self.life

		self.death_anim = Anim((0,0),P_DEATH_ANIM,play=False)

		self.collideSize = 20

		collidePos = [self.spritePos[0]+self.collideSize,self.spritePos[1]+self.collideSize]
		size = [self.sprite.get_width()+self.collideSize,self.sprite.get_height()+self.collideSize]

		self.coll_Rect = pygame.Rect(collidePos,size)

		self.lose = False

	def update(self,direction):
		self.rect.x += direction[0]
		self.rect.y += direction[1]

		if self.rect.x <= 0: 									self.rect.x += self.speed #LEFT
		if self.rect.x >= (OVERLAX-self.image.get_width()): 	self.rect.x -= self.speed #RIGHT
		if self.rect.y >= (OVERLAY-self.image.get_width()): 	self.rect.y -= self.speed #BOTTOM
		if self.rect.y <= 0: 									self.rect.y += self.speed #TOP

		self.coll_Rect.x = self.spritePos[0]+self.collideSize
		self.coll_Rect.y = self.spritePos[1]+self.collideSize

	def makeGod(self):
		self.god = not self.god

		if self.god: 	logging("Activating God mode...","std")
		else: 			logging("Deactivating God mode...","std")

	def bomb(self,nei,nei2,nei3,nei4):
		'''Since bomb is broken currently, I'm making sure that it doesn't work ever. This will prevent the program from crashing every time it is run.'''
		return None

		#5 large red orbs rain from above. Once all have hit the ground, a large white laser shoots up the middle ofthe screen.
		name = "Origin Sign: Red Rain"
		name = fontObj.render(name,True,BLACK)

		if name not in messages:
			namepos = (0, overlay.get_height()-(name.get_height()+5))
			messages[name] = namepos

		# dispText("Origin Sign: Red Rain",overlay,namepos)
		
		# self.bombing = True

		# self.playerbomb = False
		# print self.bombing

		if not self.bombing:
			self.bombs -= 1
			# print ":",self.bombing
			for b in range(5):
				x1 = random.randint(boss.rect.x-100,boss.rect.x+100)

				b = bullet((x1,0),BULL3,(0,5),playerb=True)
				bombBullet.add(b)

			self.bombing = True
			# print ">",self.bombing

		if len(bombBullet.sprites()) <= 0:
			# print "running"
			logging("Running playerbomb!","std")
			self.playerbomb = False

			# self.god = 			False
			self.makeGod()
			focus = 			False
			# bomb_fin = 			True

			self.bombing = False

			del messages[name]

			clear_b(boss.bulletGroup)
			clear_b(player.bulletGroup)
			
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

	def kill(self,cause="Generic"):
		if not self.god:
		 	self.god = True
			self.bombs = self.defBombs
		 	self.death_time = float(pygame.time.get_ticks())/1000
		 	self.addLife(-1)

		 	self.cLife = self.life

		 	if not self.isDead:
			 	playSound(P_DEATH_S)
				logging("The player has died!","std","Cause: " + cause)
				self.death_anim.playAnim(True)

			if self.death_anim.isFinished():
				self.returnToStart()

	def idle(self):
		'''Stuff to run while the program is running. (E.X: Checking health)'''

		if self.life < self.cLife:
			self.kill()

		if self.life < 0 or self.lose:
			if not self.isDead:
				clear_b(groups=[self.bulletGroup])

			for i in self.groups():
				i.remove(self)

			self.setLife(0)

			self.isDead = True

			self.kill()

			stopMusic()
			lose = True

		if self.pointColl >= self.maxPointColl:
			self.addLife(1)
			self.maxPointColl *= 4
			playSound(LIFE_UP_S)

		self.death_anim.idle()
		anim_pos = self.spritePos
		self.death_anim.setPos(anim_pos)

	def shoot(self,group):
		bullet_list = []

		if self.power >= self.maxPower:
			x1 = self.rect.x - (self.sprite.get_width()/2)
			x2 = self.rect.x + (self.sprite.get_width()/2)
			x3 = self.rect.x + 10
			x4 = self.rect.x - 10

			b = needleShot((x1,self.rect.y-30),(0,-30),playerb=True)
			b2 = needleShot((x2,self.rect.y-30),(0,-30),playerb=True)
			b3 = needleShot((x3,self.rect.y-30),(0,-30),playerb=True)
			b4 = needleShot((x4,self.rect.y-30),(0,-30),playerb=True)

			bullet_list.append(b)
			bullet_list.append(b2)
			bullet_list.append(b3)
			bullet_list.append(b4)

		elif self.power >= ((self.maxPower/4) * 3):
			x1 = self.rect.x - (self.sprite.get_width()/2)
			x2 = self.rect.x + (self.sprite.get_width()/2)
			x3 = self.rect.x

			b = needleShot((x1,self.rect.y-30),(0,-30),playerb=True)
			b2 = needleShot((x2,self.rect.y-30),(0,-30),playerb=True)
			b3 = needleShot((x3,self.rect.y-30),(0,-30),playerb=True)

			bullet_list.append(b)
			bullet_list.append(b2)
			bullet_list.append(b3)

		elif self.power >= (self.maxPower/2):
			x1 = self.rect.x - (self.sprite.get_width()/2)
			x2 = self.rect.x + (self.sprite.get_width()/2)
			
			b = needleShot((x1,self.rect.y-30),(0,-30),playerb=True)
			b2 = needleShot((x2,self.rect.y-30),(0,-30),playerb=True)
			
			bullet_list.append(b)
			bullet_list.append(b2)

		else:
			x1 = self.rect.x

			b = needleShot((x1,self.rect.y-30),(0,-30),playerb=True)
			
			bullet_list.append(b)

		self.bulletGroup.add(bullet_list)

	def graze(self,group):
		# for i in boss.bulletGroup.sprites():
		# 	if i.gRect.colliderect(self.rect) and not i.rect.colliderect(self.rect):
		# 		self.grazep += 1
		# 		return 100

		# return 0

		for i in group.sprites():
			if i.gRect.colliderect(self.rect) and not i.rect.colliderect(self.rect) and not i.grazed:
				#For some reason, graze points are increasing by two
				self.grazep += 1
				# self.grazep -= 1
				i.grazed = True
				self.score += 100

		return 0

	def collect(self,item):
		if type(item) == PointItem:
			self.score += item.sscore
			self.pointColl += 1

		elif type(item) == Powerup:
			if self.getPower() != "MAX":
				self.score += item.pscore
			else:
				return False

		elif type(item) == Lifeup:
			self.addLife(1)

		elif type(item) == Bombup:
			self.bombs += 1

		playSound(item.sound)

		return True

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
	def __init__(self,num,speed,playerb=False):
		Bullet.__init__(self,num,BULL2,speed,playerb=playerb)

class needleShot(Bullet):
	def __init__(self,num,speed,playerb=False):
		Bullet.__init__(self,num,BULL1,speed,playerb=playerb)

class genericLaser(Bullet):
	def __init__(self,num,img,playerb=False):
		bullet.__init__(self,num,img,speed=0,playerb=playerb)

class boss(Spritey):
	def __init__(self,font,num,img,life=100,lives=1):
		Spritey.__init__(self,num,life=life)
		self.lives = lives
		self.spellFont = font

		self.spell = 1

		self.spells = [self.shoot]

		self.image = loadImage(img)

		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

		self.maxLife = life
		self.maxLives = lives

		self.last_time = pygame.time.get_ticks()

		self.pwr = {'p':0}

		self.clife = 0

		self.lifes = [self.maxLife]

		self.spellTimer = Timer(2500)

		# self.spellTimer.startTimer()

		self.last_time = pygame.time.get_ticks()/1000

	def shoot(self,atak,group,surf):
		#Fire a bullet every second
		self.spellTimer.timer()

		if self.spellTimer.isFinished():
			self.kill()

		if pygame.time.get_ticks()/1000 - self.last_time >= 1:
			self.last_time = pygame.time.get_ticks()/1000
			
			for i in range(atak):
				start = surf_center(self.image,BULL2)
				start[0] += self.rect.x
				start[1] += self.rect.y

				if i is 1:
					b = circleShot(start,(0,5))
				elif i is 2:
					b = circleShot(start,(0,-5))
				elif i is 3:
					b = circleShot(start,(-5,0))
				elif i is 4:
					b = circleShot(start,(5,0))
				else:
					b = circleShot(start,(0,5))

				group.add(b)

	def dispLife(self,surface):
		start = (5*self.lives,5)
		percent = float(self.life)/float(self.maxLife)
		end = (start[0] + float(HEALTH_BAR*percent),5)
	
		for l in range(self.lives-1):
			#display all health bars
			pygame.draw.line(surface,BLUE,(5*l,5),(5+(5*l),5),3)

		pygame.draw.line(surface,BLUE,start,end,3) #Boss health bar

	def dropItem(self):
		dropList = []

		for i in self.pwr:
			newPos = (random.randint(self.rect.x-20,self.rect.x+20),self.rect.y)
			if i == 'p':
				d = Powerup(self.pos[0],self.pos[1],newPos,self.pwr[i])
				# powerGroup.add(p)

			elif i == 's':
				d = PointItem(self.pos[0],self.pos[1],newPos)
				# scoreGroup.add(s)

			elif i == 'l':
				d = Lifeup(self.pos[0],self.pos[1],newPos)
				# lifeGroup.add(l)

			elif i == 'b':
				d = Bombup(self.pos[0],self.pos[1],newPos)
				# bombupGroup.add(b)

			else:
				logging("Invalid item token '" + i + "'", "err")
				# print "ItemError: Invalid token '" + i + "'"

			dropList.append(d)

		return dropList

	def kill(self):
		self.clife += 1

		self.setLife(self.lifes[self.clife])

		self.maxLife = self.life

		self.lives -= 1
		self.spell += 1

		if not self.isDead:
			clear_b(groups=[self.bulletGroup])

		logging(str(self) + " has died!", "std","Remaining lives: " + str(self.lives))

		self.spellTimer.startTimer()

		return self.dropItem()

	def attack(self,surf,args=[]):
		card = self.maxLives - self.lives

		if card == 1:
			# self.bulletGroup = self.spells[card].getBGroup()
			for b in self.spells[card].getBGroup():
				if b not in self.bulletGroup.sprites():
					self.bulletGroup.add(b)

			return self.spells[card].idle()

		if args == []:
			self.spells[card](self.bulletGroup)
		else:
			self.spells[card](args,self.bulletGroup,surf)

	def idle(self,args={}):
		for arg in args:
			if arg == "player":
				player = args[arg]

		if self.life < 0:
			self.kill()

		# if pygame.sprite.spritecollide(self,player.bulletGroup):
		if False:
			self.addLife(-1)
			player.score += 10

		#display boss health bar
		self.dispLife(overlay)
		# self.spellTimer.dispTime((OVERLAX/2-20,5),overlay,fontObj,cutoff=1)

		self.update()

class dot_boss(boss):
	def __init__(self,font,num,life,lives,speed):
		boss.__init__(self,font,num,"Boss-1.png",life=life,lives=lives)
		self.speed = speed

		spell1 = LargeEX(self,self.bulletGroup)

		self.spells.append(spell1)
		self.spells.append(self.shoot)

		self.pwr = {'p':0,'p':1,'s':0,'p':0}

		self.lifes.append(1500)

	def spell1(self,speed,group,surf):
		self.spellTimer.setMax(30000)
		if self.spellTimer.isFinished():
			self.kill()

		self.spellTimer.timer()

		self.pwr = {'p':0,'p':1,'s':0,'p':0,'p':1,'l':0}

		name = 				 self.spellFont.render("EX Sign: Generic Danmaku",True,BLACK)
		pos = 				(OVERLAX-(name.get_width()+5),10)
		# messages[name] =	 pos

		self.speed = 		[0,0]

		newPos = [surf_center(surf,self.image)[0],10]

		if self.rect.x < newPos[0]: self.rect.x += speed
		if self.rect.x > newPos[0]: self.rect.x -= speed
		if self.rect.y < newPos[1]: self.rect.y += speed
		if self.rect.y > newPos[1]: self.rect.y -= speed

		spawn2 = [0,0]
		spawn3 = [OVERLAX-40,0]
		self.shoot(5,group,surf)

		ctime = float(pygame.time.get_ticks())/1000 - float(self.last_time)/1000

		if ctime >= 0.3:
			b = circleShot(spawn2,(5,5))
			b2 = circleShot(spawn3,(-5,5))

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

class laser(Bullet):
	def __init__(self,x,y,num,life,img,speed,playerb=False):
		bullet.__init__(self,x,y,num,img,speed,playerb=playerb)
		self.life = life
		self.birth = pygame.time.get_ticks()

	def kill(self,ctime):
		if not self.life == -1:
			if (float(ctime)/1000) - (float(self.birth)/1000) >= self.life:
				for i in self.groups():
					i.remove(self)

				# if self.playerb:
				# 	all_bullets.remove(self)
				# 	player.bulletGroup.remove(self)

				# else:
				# 	all_bullets.remove(self)
				# 	player.bulletGroup.remove(self)

				del self

class Item(Spritey):
	def __init__(self,num,img):
		Spritey.__init__(self,num,life=1)
		
		self.image = 	img

		self.rect = 	self.image.get_rect()
		self.rect.x = 	self.pos[0]
		self.rect.y = 	self.pos[1]

		self.speed = 	3

		self.ystart = 	self.pos[1] + 10
		self.down = 	False
		self.follow = 	False

		self.sound = 	PICKUP_S

	def update(self):
		if self.rect.y >= self.ystart:
			if not self.down: 	self.rect.y -= self.speed
			else: 				self.rect.y += self.speed

		if self.rect.y <= self.ystart:
			self.down = True
			self.rect.y += self.speed

	def idle(self,player):
		if self.life <= 0:
			self.kill()

		if self.rect.colliderect(player.coll_Rect):
			self.followRect(player.rect)

		if pygame.sprite.spritecollide(self,playerGroup,False):
			collected = player.collect(self)

			if collected:
				self.setLife(-1)

class PointItem(Item):
	def __init__(self,x,y,num):
		Item.__init__(self,num,SCORE_IMG)
		self.sscore = 10000

class StarPointItem(Item):
	def __init__(self,num):
		Item.__init__(self,num,STAR_POINT_IMG)
		self.sscore = 1000

class Powerup(Item):
	def __init__(self,x,y,num,size):

		if size < 0 or size > 1:
			logging("Incorrect size for Powerup item!")
			# print "Incorrect size!"
			return None

		self.pscore = (size*10)

		if self.pscore <= 0: self.pscore = 1

		if size is 0: 	img = POWER0_IMG
		else: 			img = POWER1_IMG

		Item.__init__(self,num,img)


	def idle(self,player):
		if self.life <= 0:
			self.kill()

		if self.rect.colliderect(player.coll_Rect) and not player.getPower() == "MAX":
			self.followRect(player.rect)

class Lifeup(Item):
	def __init__(self,x,y,num):
		Item.__init__(self,num,LIFE_UP_IMG)
		self.sound = LIFE_UP_S

class Bombup(Item):
	def __init__(self,x,y,num):
		Item.__init__(self,num,BOMB_UP_IMG)

		self.sound = BOMB_UP_S

class Anim(Spritey):
	def __init__(self,num,frames,speed=1,frame=0,play=True,times=1,fps=30):
		'''Animation sprite
		num <- start position
		frames <- list of images
		speed <- integer for how fast to go through the frames
		frame <- optional start frame
		play <- run animation
		times <- amount of times to run animation before stopping'''
		
		Spritey.__init__(self,num,life=1)
		
		self.c_frame = 		frame
		self.anim_frames =  frames

		try:
			self.image = self.anim_frames[self.c_frame]
		except:
			self.image = pygame.Surface((0,0),pygame.SRCALPHA)

		self.speed = 	 speed
		self.play =  	 play
		self.times = 	 0
		self.maxTimes =  times
		self.finished =  False
		self.timeStart = 0

	def setSpeed(self,speed):
		self.speed = speed

	def getFrame(self):
		try:
			return self.anim_frames[self.c_frame]
		except BaseException:
			return pygame.Surface((0,0),pygame.SRCALPHA)

	def playAnim(self,play,repeat=False):
		self.play = play
		self.finished = True

		self.repeat = repeat

	def renderAnim(self):
		overlay.blit(self.image,self.pos)

	def isFinished(self):
		return self.finished

	def setRepeat(self,repeat):
		self.repeat = repeat

	def getRepeat(self):
		return self.repeat

	def idle(self):
		if self.play:
			self.c_frame += 1

			if self.c_frame > len(self.anim_frames):
				self.c_frame = 0
				self.times +=  1

			# try:
			# 	self.image = self.anim_frames[self.c_frame]
			# except:
			# 	self.image = pygame.Surface((0,0),pygame.SRCALPHA)

			self.image = self.getFrame()

		else:
			self.image = pygame.Surface((0,0),pygame.SRCALPHA)

		self.renderAnim()

		if self.times >= self.maxTimes:
			logging("Resetting animation...","std")
			self.times = 0

			if not self.repeat:
				self.play = False
				self.finished = True

nuclear = u'\u2622'

class LargeEX(SpellCard):
	def __init__(self,owner,ownerGroup,playerb=False):
		SpellCard.__init__(self,30000,"Large X: Generic Danmaku",owner,ownerGroup)

		self.spawn2 = [0,0]
		self.spawn3 = [OVERLAX-40,0]
		self.ctime = float(pygame.time.get_ticks())/1000
		self.last_time = self.ctime
		# self.ctime = self.timer.getTimePassed()

		self.spellBKG = loadImage("SpellBKG.png",fail_size=OVERSIZE)

		self.playerb = playerb

	def Card(self):
		if self.start:
			newPos = [surf_center(overlay,self.owner.image)[0],10]
			
			self.changeOwnerPos(5,newPos)
			self.owner.speed = [0,0]

			name_size = fontObj.render(self.name,True,BLACK).get_width()
			pos = (OVERLAX-(name_size+5),10)
			self.dispName(pos)

			self.ctime = float(pygame.time.get_ticks())/1000

			if self.ctime - self.last_time >= 0.3:
				b2 = circleShot(self.spawn2,(5,5),self.playerb)
				b = circleShot(self.spawn3,(-5,5),self.playerb)

				self.last_time = self.ctime

				self.ownerGroup.add(b)
				self.ownerGroup.add(b2)

	def idle(self):
		self.runCard()
		self.dispTime((OVERLAX/2-20,5),overlay,fontObj,cutoff=1)

		return self.ChangeBKG(self.spellBKG)

	def getBGroup(self):
		return self.ownerGroup