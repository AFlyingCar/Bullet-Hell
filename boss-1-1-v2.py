#Tyler Robbins
#5/19/14
#Boss-1-1 v2
#Boss battle, using all of the pygame components I've learned up till this point.

#TO-DO LIST:
'Fix broken bullet movement (Boss spell-card)' 							#COMPLETE
'Turn game into a "game-overlay"' 										#COMPLETE
'Fix right border of game-overlay'										#COMPLETE
'Make player invincible after being hit (for a short time)' 			#COMPLETE
'Add information on the side (player health, player bombs, etc.)'		#COMPLETE
'Symbols for player lives and player bombs'								#COMPLETE
'Add music/sound effects'												#COMPLETE
'Add power up items and point items'									#COMPLETE

'Add grazing mechanics' 												#Nearly Complete (Still grazing when hit)
'Add spell-timer'														#Nearly Complete (Timer runs a bit slow for some reason: probably FPS)

'Add point system' 														#Partially Complete (HI-Score not done)

'Modularize code and split code into separate files'					#Partially Complete (Haven't finished modularizing sprites)

'Have characters "talk" (sprite cutins)'								#NOT IMPLEMENTED

'Create proper images/backgrounds'										#INCOMPLETE
'Add levels'															#INCOMPLETE
'More bullet types'														#INCOMPLETE
'Bullet Patterns'														#INCOMPLETE
'Fix music delay'														#INCOMPLETE
'Fix Player bomb name'													#INCOMPLETE (Text doesn't disappear once the bomb ends)

import pygame,sys,random,os
from pygame.locals import *
from bin.lib.basic import *

#Haven't finished modularizing this yet.
# from bin.lib.sprites import *

#Keep constants in a separate folder to make the code less cluttered
from bin.lib.constants import *

FPS = 			60
HI = 			0 #HI-Score, thscore.dat

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

	def shoot(self):
		######Generic sprite shooting######
		b = bullet(x,y,(self.rect.x,self.rect.y-30),'75'.join(IMG),(0,-30))
		playerBullet.add(b)

	def setLife(self,life): self.life += life

	def setPos(self,pos):
		self.pos = pos
		self.rect.x = self.pos[0]
		self.rect.y = self.pos[1]

	def drawSprite(self):
		pos = surf_center(self.sprite,self.image)
		pos[0] = self.rect.x - pos[0]
		pos[1] = self.rect.y - pos[1]

		self.gRect = pygame.Rect(pos,self.sprite.get_size())

		overlay.blit(self.sprite,pos)

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

	def update(self):
		player.rect.x += direction2[0]
		player.rect.y += direction2[1]

		if self.rect.x <= 0: 									self.rect.x += self.speed #LEFT
		if self.rect.x >= (OVERLAX-self.image.get_width()): 	self.rect.x -= self.speed #RIGHT
		if self.rect.y >= (OVERLAY-self.image.get_width()): 	self.rect.y -= self.speed #BOTTOM
		if self.rect.y <= 0: 									self.rect.y += self.speed #TOP

	def bomb(self):
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

				b = bullet(x,y,(x1,0),'76'.join(IMG),(0,5),playerb=True)
				bombBullet.add(b)

			self.bombing = True
			# print ">",self.bombing

		if len(bombBullet.sprites()) <= 0:
			print "running"
			self.playerbomb = False

			self.god = 			False
			focus = 			False
			# bomb_fin = 			True

			self.bombing = False

			del messages[name]

			clear_b(bossBullet)
			clear_b(playerBullet)
			
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

	def shoot(self):
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

		playerBullet.add(bullet_list)

	def graze(self):
		# for i in bossBullet.sprites():
		# 	if i.gRect.colliderect(self.rect) and not i.rect.colliderect(self.rect):
		# 		self.grazep += 1
		# 		return 100

		# return 0

		for i in bossBullet.sprites():
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

	def shoot(self,atak):
		#Fire a bullet every second
		self.spellTimer.timer()
		if pygame.time.get_ticks()/1000 - last_time >= 1:
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

				bossBullet.add(b)

	def dispLife(self):
		start = (5*self.lives,5)
		# end = ((5*self.lives)+(self.life/2),5)
		# end = ((5*self.lives)+(self.life/(self.life/OVERLAX)),5)
		# end = (start[0] + (OVERLAX-(self.life/OVERLAX)),5)
		percent = float(self.life)/float(self.maxLife)
		end = (start[0] + float(HEALTH_BAR*percent),5)

		pygame.draw.line(overlay,BLUE,start,end,3) #Boss health bar

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

	def attack(self,args=None):
		if args == []:
			self.spells[self.spell-1]()
		else:
			self.spells[self.spell-1](args)

class dot_boss(boss):
	def __init__(self,x,y,num,life,lives,speed):
		boss.__init__(self,x,y,num,"Boss-1.png",life=life,lives=lives)
		self.speed = speed

		self.spells.append(self.spell1)

		self.pwr = {'p':0,'p':1,'s':0,'p':0}

		self.lifes.append(1500)

	def spell1(self,speed):
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

			bossBullet.add(b)
			bossBullet.add(b2)

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

	def isFinished(self):
		return self.finished

def move():
	#Change player direction based on pressed keys#
	if r_move and not l_move: 	direction2[0] =  player.speed
	elif l_move and not r_move: direction2[0] = -player.speed
	elif r_move and l_move: 	direction2[0] =  0
	else: 						direction2[0] =  0
	
	if u_move and not d_move: 	direction2[1] = -player.speed
	elif d_move and not u_move: direction2[1] =  player.speed
	elif d_move and u_move: 	direction2[1] =  0
	else: 						direction2[1] =  0

def updateScreen(BKG):
	screen.blit(BKG,(0,0))
	screen.blit(overlay,OVERPOS)

	infoPrint()
	fpsPrint(fps,OVERSIZE,fontObj,screen)

	pygame.display.update()

def infoPrint():
	new_info = []
	n = (OVERPOS[0] + 10 + OVERLAX, 50) #Y position of information

	for i in def_info:
		loc = def_info.index(i)

		x = i + str(info[loc])
		m = fontObj.render(x,True,WHITE)

		if i == "Player":
			ppos = list(n)
			ppos[0] += m.get_width() + 10
			ploc = loc
		elif i == "Bomb":
			bpos = list(n)
			bpos[0] += m.get_width() + 10
			bloc = loc

		new_info.append(m)

	for i in new_info:
		screen.blit(i,n)
		if new_info.index(i) == ploc:
			ppos[1] = n[1]
		elif new_info.index(i) == bloc:
			bpos[1] = n[1]

		n = (n[0],n[1]+new_info[1].get_height() + 10)

	x = "POWER: " + str(player.getPower())
	i = fontObj.render(x,True,WHITE)
	screen.blit(i,n)

	symbol(player.life,LIFE_IMG,ppos,screen)
	symbol(player.bombs,BOMB_IMG,bpos,screen)

def cutin(bosss,players,stage):
	'''bosss and players are cutin images.'''
	bosst = 	[]
	playert = 	[]

	text = talks[stage-1]
	text = text.split("\n")

	for i in text:
		if i.startswith("BOSS:"):
			bosst.append(i.split(":")[1])
		elif i.startswith("PLAY:"):
			playert.append(i.split(":")[1])
		else:
			print "TalkError: Invalid speach tag.", i.split(":")[0], "is not valid."
			return [False] + + [x for x in [None for y in range(5)]]

		text[text.index(i)] = i.split(":")[1]

	box = pygame.Surface((OVERLAX-20,OVERLAY-200))

	return ([True,box,text,bosst,playert,pygame.time.get_ticks()])

speed = 		int(raw_input("Max speed: "))
direction2 = 	[0,0]
collide =		False
focus =			False
shoot = 		False
lose = 			False
win =			False
ctrl_hold = 	False
bomb_fin = 		True
x = 			20
y = 			25
# score = 		0
cooldown = 		0
messages = 		{} #{<fontObj>:<pos>}
bomb_name = 	""

playerbomb = False

d_move = False
u_move = False
l_move = False
r_move = False

def_info = ["HI-Score: ",
		"Score: ",
		"Player",
		"Bomb",
		"Graze: "]

pygame.init()

fps = 		pygame.time.Clock()
overlay = 	pygame.Surface(OVERSIZE)
screen = 	pygame.display.set_mode(SCREEN_SIZE)
talks = 	open("thcut.dat",'r').read().split("NBOSS")
fontObj = 	pygame.font.Font(os.path.join(os.path.abspath(os.getcwd()),'Fonts','THSpatial.ttf'),29)
last_time = 0

pygame.display.set_caption('Dot Boss Battle')
overlay.fill(WHITE)

screen.blit(overlay,OVERPOS)

posx = (overlay.get_width()/2)-5

player = 		Player(x,y,[posx,overlay.get_height()-5],speed,"player.png",2)

#Set the boss's life to any positive integer, but I'm leaving it at 100 right now for testing
boss =			dot_boss(x,y,[posx,40],life=100,lives=2,speed=[-2,0])

playerBullet = 	pygame.sprite.Group()
bossBullet = 	pygame.sprite.Group()
bombBullet = 	pygame.sprite.Group()
all_bullets = 	pygame.sprite.Group()
scoreGroup = 	pygame.sprite.Group()
powerGroup =	pygame.sprite.Group()
lifeGroup = 	pygame.sprite.Group()
bombupGroup =	pygame.sprite.Group()
itemGroup = 	pygame.sprite.Group()
playerGroup = 	pygame.sprite.Group(player)
bossGroup = 	pygame.sprite.Group(boss)
all_sprites =	pygame.sprite.Group(player,boss)

player.setPower("max") #COMMENT THIS OUT LATER

playMusic("th00_01.ogg") #Music begins a bit delayed

boss.spellTimer.startTimer()

while True:
	all_bullets.add(x for x in playerBullet.sprites())
	all_bullets.add(x for x in bossBullet.sprites())
	all_bullets.add(x for x in bombBullet.sprites())

	itemGroup.add(x for x in scoreGroup.sprites())
	itemGroup.add(x for x in powerGroup.sprites())

	overlay.fill(WHITE)
	for event in pygame.event.get():
		if event.type == QUIT: shutdown()

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE: shutdown()

			if event.key == K_DOWN:   d_move = True
			if event.key == K_UP:     u_move = True
			if event.key == K_LEFT:   l_move = True
			if event.key == K_RIGHT:  r_move = True
			
			if event.key == K_z and not player.playerbomb:
				shoot = True
			if event.key == K_x:
				if player.bombs != 0 and not player.bombing:
					# bomb_name = player.bomb()
					player.playerbomb = True

			if event.key == K_LSHIFT or event.key == K_RSHIFT:
				focus = True

			if event.key == K_RETURN:
				#overlay technical information in the command prompt.
				print "PLAYER", player.life, ": ", player.bombing, ": ", player.god
				print "BOSS", boss.life, ": ", boss.lives
			
			if event.key == K_RCTRL or event.key == K_LCTRL:
				#Hold down and press a key to activate cheats
				ctrl_hold = True
				print "CTRL"
			if event.key == K_w and ctrl_hold:
				#Emergency shutdown
				shutdown()
			if event.key == K_h and ctrl_hold:
				#Toggle god mode
				if player.god: 	player.god = False
				else: 			player.god = True

				print "GOD",player.god

			collide = False
			
		if event.type == KEYUP:
			# if event.key == K_UP:		direction2[1] = 0
			# if event.key == K_DOWN:		direction2[1] = 0
			# if event.key == K_LEFT:		direction2[0] = 0
			# if event.key == K_RIGHT:	direction2[0] = 0

			if event.key == K_DOWN:   	d_move = False
			if event.key == K_UP:     	u_move = False
			if event.key == K_LEFT:   	l_move = False
			if event.key == K_RIGHT:  	r_move = False

			if event.key == K_z:		shoot = False

			if event.key == K_LSHIFT or event.key == K_RSHIFT:
				focus = False

			if event.key == K_LCTRL or event.key == K_RCTRL:
				ctrl_hold = False

	move()
						
	######Update positions of sprites######
	boss.rect.x -= DIRECTION1[0]
	boss.rect.y -= DIRECTION1[1]

	player.drawSprite()
	player.setFocus(focus)

	######Sprite collision detection######
	if (pygame.sprite.spritecollide(player,bossGroup,False) or pygame.sprite.spritecollide(player,bossBullet,True)) and not collide:
	 	collide = True
	 	if not player.god and not player.bombing: player.kill()

	if pygame.sprite.spritecollide(boss,playerBullet,True):
		boss.setLife(-1)
		# score += 10
		player.score += 10
	if pygame.sprite.spritecollide(boss,bombBullet,False):
		boss.setLife(-5)
		# score += 10
		player.score += 10

	for i in powerGroup.sprites():
		if player.getPower() != "MAX":
			if pygame.sprite.spritecollide(i,playerGroup,False):
				itemGroup.remove(i)
				powerGroup.remove(i)
				player.power += i.pscore

				del i

	for i in scoreGroup.sprites():
		if pygame.sprite.spritecollide(i,playerGroup,False):
			itemGroup.remove(i)
			scoreGroup.remove(i)
			# score += i.sscore
			player.score += i.sscore

			del i

	for b in bossBullet.sprites():
		if pygame.sprite.spritecollide(b,bombBullet,False):
			all_bullets.remove(b)
			bossBullet.remove(b)

	if float(pygame.time.get_ticks())/1000 - player.death_time >= 3:
		player.god = False

	if player.bombing and False: #Don't want this to run, but don't want to delete until we know it's obosolete
		# if not boss.life <= 0 and not boss.lives <= 1:
		# 	score += 10
		player.god = 	True
		focus = True
		bomb_fin = False
		messages[bomb_name] = (0, overlay.get_height()-(bomb_name.get_height()+5))

		######LASER######
		# start = surf_center(boss.image,loadImage('img_laser1.png'))
		# start[1] = OVERLAY-loadImage('img_laser1.png').get_height()
		# l = laser(x,y,start,-1,'img_laser1.png',[0,0],playerb=True)
		# bombBullet.add(l)

		if len(bombBullet.sprites()) <= 0:
			# start = surf_center(boss.image,loadImage('img_laser1.png'))
			# start[1] = OVERLAY-loadImage('img_laser1.png').get_height()
			# l = laser(x,y,start,4,'img_laser1.png',[0,0],playerb=True)
			# bombBullet.add(l)

			player.bombing = 	False
			player.god = 		False
			focus = 			False
			bomb_fin = 			False

			clear_b(bossBullet)
			clear_b(playerBullet)

		# for i in bombBullet: i.update()
	else:
		if bomb_name in messages:
			del messages[bomb_name]

	if boss.life <= 0 and not boss.lives <= 1:
		# clear_b(bossBullet)
		# boss.lives -= 1
		# boss.setLife(-(0-boss.life) + boss.maxLife)

		boss.kill()

	if boss.life <= 0 and boss.lives <= 1:
		all_bullets.remove(x for x in playerBullet.sprites())
		all_bullets.remove(x for x in bossBullet.sprites())
		playerBullet.empty()
		bossBullet.empty()
		all_sprites.remove(boss)

		boss.rect.x = overlay.get_width()+10
		boss.rect.y = overlay.get_height()+10

		x = fontObj.render('YOU WIN!',True,BLACK)
		# overlay.blit(x,surf_center(overlay,x))
		messages = {}

		messages[x] = surf_center(overlay,x)
		win = True

		pygame.mixer.music.fadeout(5)

	if player.life < 0:
		all_sprites.remove(x for x in playerBullet.sprites())
		all_sprites.remove(x for x in bossBullet.sprites())
		playerBullet.empty()
		bossBullet.empty()
		all_sprites.remove(player)
		player.life = 0

		x = fontObj.render('YOU LOSE!',True,BLACK)
		# overlay.blit(x,surf_center(overlay,x))
		messages[x] = surf_center(overlay,x)
		lose = True

	boss.update()
	player.update()

	offscreen(all_bullets,OVERSIZE)
	offscreen(powerGroup,OVERSIZE)
	offscreen(scoreGroup,OVERSIZE)

	if shoot and not lose and not player.playerbomb: player.shoot()

	if player.playerbomb: player.bomb()
	else: player.playerbomb = False

	# if player.bomb_flash:
	if False:
		flashc[3] -= 1
		flashs.fill(flashc)

		if flashc[3] <= 0:
			player.bomb_flash = False

	for b in all_bullets.sprites(): b.update()

	if not win and not lose:
		# if boss.spell == 1:		boss.shoot(5)
		# elif boss.spell == 2:	boss.spell1(5)
		# else:					boss.shoot(5)

		boss.attack(args=5)

		last_time = pygame.time.get_ticks()/1000

	if win: clear_b(bossBullet)

	all_sprites.draw(overlay)
	all_bullets.draw(overlay)
	itemGroup.draw(overlay)

	for i in all_bullets.sprites():
		i.drawSprite()
		if type(i) is laser: #This does run
			# print "IT'S A LASER!"
			i.kill(pygame.time.get_ticks())

	for i in itemGroup.sprites():
		i.update()

	for l in range(boss.lives-1):
		#display all health bars
		pygame.draw.line(overlay,BLUE,(5*l,5),(5+(5*l),5),3)

	for m in messages: overlay.blit(m,messages[m])
	
	#display boss health bar
	boss.dispLife()
	boss.spellTimer.dispTime((OVERLAX/2-20,5),overlay,fontObj,cutoff=1)

	# score += player.graze()
	player.graze()

	fps.tick(FPS)
	info = [HI,
			# score,
			player.score,
			"",
			"",
			player.grazep]

	updateScreen(S_BKG)

	pygame.display.update()

nuclear = u'\u2622'