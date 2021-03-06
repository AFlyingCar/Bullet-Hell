#Tyler Robbins
#7/16/14
#Sprites
#A place to store all of the sprite classes

import pygame.sprite,random
from debugger import logging
from dependencies import *
from spellcards import *
from globalVar import *
from constants import *
from settings import *
from Spritey import *
from bullets import *
from basic import *

class Player(Spritey):
	def __init__(self,num,maxs,sprite,life):
		'''Player class that defines the basics of what every player can do.
		num 	<- (x,y)					<-- Starting position
		maxs 	<- integer 					<-- Maximum speed
		sprite 	<- string or Surface object <-- Sprite image to use
		life 	<- integer 					<-- Starting number of lives
		'''
		Spritey.__init__(self,num,life=life)
		self.grazep = 	0
		self.power = 	1
		self.defBombs = 4
		self.maxBombs = 10
		self.maxLife = 	10
		self.maxPower = 300
		self.damage = 	playerdamage

		self.bombs = self.defBombs

		self.bombing = 	False
		self.god = 		False
		
		self.default =	maxs
		self.focus = 	maxs/2
		self.speed = 	self.default
		
		#Sprite is visible by default, but can be made invisible
		self.visible = 			True

		self.visibleSprite = 	loadImage(sprite)
		self.invisSprite = 		pygame.Surface((1,1),pygame.SRCALPHA,32)
		self.sprite = 			self.visibleSprite

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

		self.timesRun = 0

	def update(self,direction):
		'''Update the player's position based on their speed'''
		self.rect.x += direction[0]
		self.rect.y += direction[1]

		if self.rect.x <= 0: 									self.rect.x += self.speed #LEFT
		if self.rect.x >= (OVERLAX-self.image.get_width()): 	self.rect.x -= self.speed #RIGHT
		if self.rect.y >= (OVERLAY-self.image.get_width()): 	self.rect.y -= self.speed #BOTTOM
		if self.rect.y <= 0: 									self.rect.y += self.speed #TOP

		self.coll_Rect.x = self.spritePos[0]+self.collideSize
		self.coll_Rect.y = self.spritePos[1]+self.collideSize

	def makeGod(self):
		'''Toggle god mode'''
		self.god = not self.god

		logging(("Activating" if self.god else "Deactivating") + " god mode...","std")

	def isGod(self):
		'''Return whether god mode is active.'''
		return self.god

	def bomb(self,nei,nei2,nei3,nei4):
		'''Since bomb is broken currently, I'm making sure that it doesn't work ever. This will prevent the program from crashing every time it is run.'''
		return None

		#5 large red orbs rain from above. Once all have hit the ground, a large white laser shoots up the middle ofthe screen.
		name = "Origin Sign: Red Rain"
		name = FONT_THSPATIAL.render(name,True,BLACK)

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

		# return FONT_THSPATIAL.render(name,True,BLACK)

	def addBomb(self,bomb):
		self.bombs += bomb

	def setFocus(self,shift):
		'''Toggle focus mode'''
		if shift:
			self.speed = self.focus
			if not self.bombing: pygame.draw.circle(self.image,RED,(5,5),5)
		else:
			self.speed = self.default
			del self.image
			self.image = pygame.Surface((10,10),pygame.SRCALPHA,32)

	def getPower(self):
		'''Get the current amount of power, using MAX if power is as high as possible.'''
		if self.power >= self.maxPower: return "MAX"
		else: 							return self.power

	def setPower(self,point):
		'''Set power level, using max to set power as high as possible.'''
		if type(point) == str:
			if point.lower() == "max": 	self.power = self.maxPower
		else: 							self.power += point

	def kill(self,cause="Generic"):
		if not self.god:
		 	self.god = True
			self.bombs = self.defBombs
		 	self.death_time = float(pygame.time.get_ticks())/1000

		 	self.cLife = self.life

		 	if not self.isDead:
			 	playSound(P_DEATH_S,getSetting("soundVolume"))
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

			stopMusic()
			lose = True

		if self.pointColl >= self.maxPointColl:
			self.addLife(1)
			self.maxPointColl *= 4
			playSound(LIFE_UP_S,getSetting("soundVolume"))

		if self.shooting and not self.playerbomb and not self.isDead:
			self.shoot()

		#Change whether the sprite is visible or not
		if self.visible: 	self.sprite = self.visibleSprite
		else: 				self.sprite = self.invisSprite

		self.death_anim.idle()
		anim_pos = self.spritePos
		self.death_anim.setPos(anim_pos)
		self.uponDeath()

	def shoot(self,group=None):
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
		'''Add points if grazing bullets.'''
		if not self.isDead:
			for i in group.sprites():
				if i.gRect.colliderect(self.rect) and not i.rect.colliderect(self.rect) and not i.grazed:
					#For some reason, graze points are increasing by two
					self.grazep += 1
					i.grazed = True
					self.score += 100
					playSound(TICK_S)

		return 0

	def collect(self,item):
		'''What to do when collecting items.'''
		if type(item) == PointItem or type(item) == StarPointItem:
			self.score += item.sscore
			self.pointColl += 1

		elif type(item) == (smallPowerUp or bigPowerUp):
			if self.getPower() != "MAX":
				self.power += item.pscore
			else:
				logging("NOT COLLECTING POWER","test")
				return False

		elif type(item) == Lifeup:
			self.addLife(1)

		elif type(item) == Bombup:
			self.addBomb(1)

		playSound(item.sound,getSetting("soundVolume"))

		return True

	def uponDeath(self):
		'''What to do when the player dies.'''
		if self.isDead:
			self.timesRun += 1
			x = FONT_THSPATIAL.render('YOU LOSE!',True,BLACK)
			overlay.blit(x,surf_center(overlay,x))

			self.speed = 0
			# self.sprite = pygame.Surface((1,1))
			if self.visible:
				self.toggleVisible()

			if self.timesRun <= 1:
				stopMusic()

			if not isPlaying():
				mus = getSetting('enable_music')
				if mus: playMusic("th00_04.ogg")

	def toggleVisible(self):
		'''Toggle sprite visibility.'''
		logging("Toggling sprite visiblity...","std","Player is now " + ("visible" if not self.visible else "invisible"))
		self.visible = not self.visible

class Enemy(Spritey):
	def __init__(self,pos,img,life=4):
		'''Base Enemy class.
		pos 	<- (x,y)						<-- starting position
		img 	<-	string or surface object	<--	sprite to use
		life=4	<- 	integer 					<-- Starting life. 100 by default.
		'''
		Spritey.__init__(self,pos,life=life)

		self.image = loadImage(img)

		self.maxLife = life

		self.rect = self.image.get_rect()
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

		self.last_time = pygame.time.get_ticks()

		self.drops = []

	def dropItem(self):
		'''Drop collectable items'''
		dropList = []

		drops = self.drops

		for item in drops:
			newPos = (random.randint(self.rect.x-20,self.rect.x+20),self.rect.y)

			if item == 'p1': 	
				d = smallPowerUp(newPos)
				dropList.append(d)
			elif item == 'p2':
				d = bigPowerUp(newPos)
				dropList.append(d)
			elif item == 's': 	
				d = PointItem(self.pos[0],self.pos[1],newPos)
				dropList.append(d)
			elif item == 'l': 	
				d = Lifeup(self.pos[0],self.pos[1],newPos)
				dropList.append(d)
			elif item == 'b': 	
				d = Bombup(self.pos[0],self.pos[1],newPos)
				dropList.append(d)

			else: logging("Invalid item token '" + item + "'", "err")


		for d in dropList:
			if type(d) is 	smallPowerUp or type(d) is bigPowerUp:
				powerGroup.add(d)
			elif type(d) == PointItem: 						scoreGroup.add(d)
			elif type(d) == Lifeup: 						lifeGroup.add(d)
			elif type(d) == Bombup: 						bombupGroup.add(d)
			else: logging("[Unknown item: "+ str(type(d)) +"]","err")

	def shoot(self):
		'''Shoot method that is to be customized for each sprite.'''
		pass

	def idle(self):
		'''Custom idle method.'''
		self.kill()
		self.shoot()
		self.update()
		self.uponDeath()

	def kill(self):
		if self.life < 0:
			self.dropItem()
			self.isDead = True

class Fairy(Enemy):
	def __init__(self,pos,img,life,shoot_pattern):
		'''shoot_pattern is a function that is called during the Fairy's shoot method.'''
		Enemy.__init__(pos,img,life=life)

		self.pattern = shoot_pattern

	def shoot(self,args=[]):
		'''Customizable shooting method.'''
		self.pattern(*args)

	def update(self):
		'''Update position based on speed.'''
		self.rect.x += self.speed[0]
		self.rect.y += self.speed[1]

class boss(Enemy):
	def __init__(self,num,img,music,life=100,lives=1):
		'''Base boss class.
		num 		<- (x,y) 					<-- starting position
		img 		<- string or Surface object <-- boss sprite
		life=100 	<- integer 					<-- Starting life. 100 by default. [this may be deprecated]
		lives=1 	<- integer 					<-- Maximum amount of lives the boss has. 1 by default
		'''
		Enemy.__init__(self,num,img,life=life)
		self.lives = lives
		self.spellFont = FONT_THSPATIAL

		self.spell = 0

		spell1 = SpellCard(10000,"",self,self.bulletGroup)
		self.spells = [spell1]

		self.maxLives = lives

		self.clife = 0

		self.ctimer = None

		self.fighting = False

		self.music = music

		self.timesRun = 0 #<- This is necessary for uponDeath, but I would like to get rid of it soon

	def dispLife(self,surface):
		'''Display all of the boss's health bars.'''
		start = 	(5*self.lives,5)

		percent = 	float(self.life)/float(self.maxLife)
		end = 		(start[0] + float(HEALTH_BAR*percent),5)
	
		for l in range(self.lives-1):
			#display all health bars
			pygame.draw.line(surface,BLUE,(5*l,5),(5+(5*l),5),3)

		pygame.draw.line(surface,BLUE,start,end,3) #Boss health bar

	def dropItem(self):
		'''Drop collectable items'''
		dropList = []

		drops = self.spells[self.spell].getDrops()

		for item in drops:
			newPos = (random.randint(self.rect.x-20,self.rect.x+20),self.rect.y)

			if item == 'p1': 	
				d = smallPowerUp(newPos)
				dropList.append(d)
			elif item == 'p2':
				d = bigPowerUp(newPos)
				dropList.append(d)
			elif item == 's': 	
				d = PointItem(self.pos[0],self.pos[1],newPos)
				dropList.append(d)
			elif item == 'l': 	
				d = Lifeup(self.pos[0],self.pos[1],newPos)
				dropList.append(d)
			elif item == 'b': 	
				d = Bombup(self.pos[0],self.pos[1],newPos)
				dropList.append(d)

			else: logging("Invalid item token '" + item + "'", "err")


		for d in dropList:
			if type(d) is 	smallPowerUp or type(d) is bigPowerUp:
				powerGroup.add(d)
			elif type(d) == PointItem: 						scoreGroup.add(d)
			elif type(d) == Lifeup: 						lifeGroup.add(d)
			elif type(d) == Bombup: 						bombupGroup.add(d)
			else: logging("[Unknown item: "+ str(type(d)) +"]","err")

	def StartBossFight(self):
		'''Begin boss fight'''
		self.fighting = True

	def endBossFight(self):
		'''End boss fight.'''
		self.fighting = False

	def kill(self,timerkill=False):
		'''What to do when the boss's health reaches 0.'''
		if self.life < 0 or timerkill:
			self.dropItem()

			if self.spell + 1 > (len(self.spells)-1):
				self.isDead = True
				return

			self.getNewLife()

			self.spells[self.spell].stopCard()

			self.life = self.maxLife

			self.lives -= 1
			self.spell += 1
			self.clife += 1

			if not self.isDead:
				clear_b(groups=[self.bulletGroup])

			logging(str(self) + " has died!", "std","Remaining lives: " + str(self.lives))

	def attack(self,args=[]):
		'''Run current spellcard idle method.'''
		card = self.spell

		if args:
			self.spells[card].idle(*args)
		else:
			self.spells[card].idle()

	def idle(self,args=[]):
		'''Custom idle method.'''
		if self.fighting:
			self.attack(args)

			self.kill()

			if self.spell > self.maxLives:
				self.isDead = True

			if self.lives < 0:
				self.permaKill()
				return

			#display boss health bar
			self.dispLife(overlay)

			self.update()
		
		self.uponDeath()

	def getSpellBKG(self):
		'''Return the current spellcard's custom background.'''
		bkg = self.spells[self.spell].getSpellBKG()

		overlay.blit(bkg,(0,0))

	def uponDeath(self):
		'''What the boss is supposed to do upon death.'''
		if self.isDead:
			self.timesRun += 1
			for b in self.bulletGroup.sprites():
				b.kill()

			self.endBossFight()

	def permaKill(self):
		'''Permanantly kill the boss.'''
		for i in self.groups():
			i.remove(self)

		self.rect.x = -10
		self.rect.y = -10
		# del self

	def update(self):
		'''Update the boss's position based on its speed.'''
		self.speed = spriteWallCollide(self)

		self.rect.x += self.speed[0]
		self.rect.y += self.speed[1]

	def getNewLife(self):
		'''Get the boss's next life.'''
		if False:
			self.clife >= len(self.lifes)
			self.permaKill()
		else:
			pass
		
		self.spells[self.spell-1].getNewLife() # THIS IS EXPERIMENTAL

	def getMusic(self):
		'''Get the music that is supposed to play during the boss battle'''
		return self.music

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

class smallPowerUp(Item):
	def __init__(self,pos):
		Item.__init__(self,pos,POWER0_IMG)
		self.pscore = 5

	def idle(self,player):
		if self.rect.colliderect(player.coll_Rect) and not player.getPower() == "MAX":
			self.followRect(player.rect)

		if pygame.sprite.spritecollide(self,playerGroup,False):
			collected = player.collect(self)

			if collected:
				self.setLife(-1)

		if self.life <= 0:
			self.kill()

class bigPowerUp(Item):
	def __init__(self,pos):
		Item.__init__(self,pos,POWER1_IMG)
		self.pscore = 10

	def idle(self,player):
		if self.rect.colliderect(player.coll_Rect) and not player.getPower() == "MAX":
			self.followRect(player.rect)

		if pygame.sprite.spritecollide(self,playerGroup,False):
			collected = player.collect(self)

			if collected:
				self.setLife(-1)

		if self.life <= 0:
			self.kill()

class Lifeup(Item):
	def __init__(self,x,y,num):
		Item.__init__(self,num,LIFE_UP_IMG)
		self.sound = LIFE_UP_S

class Bombup(Item):
	def __init__(self,x,y,num):
		Item.__init__(self,num,BOMB_UP_IMG)

		self.sound = BOMB_UP_S

class Anim(Spritey):
	def __init__(self,num,frames,speed=1,frame=0,play=True,times=1):
		'''Animation sprite
		num <- start position
		frames <- list of images
		speed <- integer for how fast to go through the frames
		frame <- optional start frame
		play <- run animation
		times <- amount of times to run animation before stopping
		'''
		
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
		'''Set the speed of the animation.'''
		self.speed = speed

	def getFrame(self):
		'''Get the current frame of the animation as a Surface object.'''
		try:
			return self.anim_frames[self.c_frame]
		except BaseException:
			return pygame.Surface((0,0),pygame.SRCALPHA)

	def playAnim(self,play,repeat=False):
		'''Start playing the animation.'''
		self.play = play
		self.finished = True

		self.repeat = repeat

	def resetAnim(self):
		'''Reset the animation to the beginning frame.'''
		self.c_frame = 0

	def renderAnim(self):
		'''Render the animation to the overlay.'''
		overlay.blit(self.image,self.pos)

	def isFinished(self):
		'''Check if the animation has finished running through all frames.'''
		return self.finished

	def setRepeat(self):
		'''Toggle repetition of the animation.'''
		self.repeat = not self.repeat

	def getRepeat(self):
		'''Get if the animation is set to repeat.'''
		return self.repeat

	def idle(self):
		if self.play:
			self.c_frame += 1

			if self.c_frame > len(self.anim_frames):
				self.c_frame = 0
				self.times +=  1

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
