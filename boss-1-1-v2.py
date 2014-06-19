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

'Add grazing mechanics' 												#Nearly Complete (Still grazing when hit)

'Add point system' 														#Partially Complete (HI-Score not done, power up items not impletmented)

'Add power up items and point items'									#INCOMPLETE
'Add music/sound effects'												#INCOMPLETE
'Create proper images/backgrounds'										#INCOMPLETE
'Add levels'															#INCOMPLETE
'Have characters talk (sprite cutins)'									#INCOMPLETE
'More bullet types'														#INCOMPLETE
'Bullet Patterns'														#INCOMPLETE

import pygame,sys,random,os
from pygame.locals import *

def loadImage(filename):
	loc = os.path.join(os.getcwd(),"Images",filename)

	pic = pygame.image.load(loc)

	return pic

BLACK = (0,0,0)
RED = 	(255,0,0)
BLUE = 	(0,0,255)
CLEAR = (0,0,0,0)
WHITE = (255,255,255)

IMG = 			('img-','.png')
SCREEN_SIZE = 	(640,480)
OVERSIZE =		(SCREEN_SIZE[0]-300,SCREEN_SIZE[1]-50)
OVERLAX = 		OVERSIZE[0]
OVERLAY =		OVERSIZE[1]
HEALTH_BAR = 	OVERLAX-30
OVERPOS = 		(10,20)
START_POS_2 = 	((OVERLAX-1)-loadImage("player.png").get_width(),1) #<-- makes sure the image doesn't start offscreen
START_POS_1 = 	(1,1)
DIRECTION1 = 	[0,0] #boss movement
FPS = 			50
S_BKG = 		loadImage("s_bkg".join(IMG))
LIFE_IMG = 		loadImage("79".join(IMG))
BOMB_IMG = 		loadImage("78".join(IMG))

HI = 0 #HI-Score

class Spritey(pygame.sprite.Sprite):
	def __init__(self,x,y,num,life=3):
		pygame.sprite.Sprite.__init__(self)

		if num is 1: 	self.pos = START_POS_1
		elif num is 0: 	self.pos = START_POS_2
		else:			self.pos = num

		print self.pos

		self.image = pygame.Surface((10,10),pygame.SRCALPHA,32)
		# self.image.fill(CLEAR)

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

		self.death_time = 0

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
		self.bombing = True
		self.bombs -= 1
		for b in range(5):
			x1 = random.randint(boss.rect.x-100,boss.rect.x+100)

			b = bullet(x,y,(x1,0),'76'.join(IMG),(0,5),playerb=True)
			bombBullet.add(b)

		return fontObj.render(name,True,BLACK)

	def setFocus(self,shift):
		if shift:
			self.speed = self.focus
			if not self.bombing: pygame.draw.circle(self.image,RED,(5,5),5)
		else:
			self.speed = self.default
			del self.image
			self.image = pygame.Surface((10,10),pygame.SRCALPHA,32)

	def drawSprite(self):
		pos = (self.rect.x-self.sprite.get_width()/2,self.rect.y-self.sprite.get_height()/2)
		overlay.blit(self.sprite,pos)

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
		for i in bossBullet.sprites():
			if i.gRect.colliderect(self.rect) and not i.rect.colliderect(self.rect):
				self.grazep += 1
				return 100

		return 0

class bullet(Spritey):
	def __init__(self,x,y,num,img,speed,playerb = False):
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

	def drawSprite(self):
		# pos = (self.rect.x-self.sprite.get_width()/2,self.rect.y-self.sprite.get_height()/2)

		pos = surf_center(self.sprite,self.image)
		pos[0] = self.rect.x - pos[0]
		pos[1] = self.rect.y - pos[1]

		self.gRect = pygame.Rect(pos,self.sprite.get_size())

		overlay.blit(self.sprite,pos)

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

	def shoot(self,atak):
		#Fire a bullet every second
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
		self.lives -= 1
		self.spell += 1
		clear_b(bossBullet)
		self.setLife(-(0-self.life) + self.maxLife)

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

	def spell1(self,speed):
		name = fontObj.render("EX Sign: Generic Danmaku",True,BLACK)
		pos = (overlay.get_width()-(name.get_width()+5),10)
		messages[name] = pos
		self.speed = [0,0]

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

class s_laser(Spritey):
	def __init__(self,x,y,num,time):
		Spritey.__init__(self,x,y,num,life=time)
		self.life = time
		self.image = loadImage('77'.join(IMG))

def offscreen(group):
	#For bullets only
	for b in group.sprites():
		delete = False

		if b.rect.x <= (0-b.image.get_width()):	
			group.remove(b)
			all_bullets.remove(b)
			delete = True

		if b.rect.x >= OVERLAX:
			group.remove(b)
			all_bullets.remove(b)
			delete = True

		if b.rect.y >= OVERLAY:
			group.remove(b)
			all_bullets.remove(b)
			delete = True

		if b.rect.y <= (0-b.image.get_height()):
			group.remove(b)
			all_bullets.remove(b)
			delete = True

		if delete: del b

def clear_b(group):
	for x in group.sprites():
		all_bullets.remove(x)
	group.empty()

def shutdown():
	pygame.quit()
	sys.exit()

def surf_center(surface,newSurface):
	x = (surface.get_width()/2) - (newSurface.get_width()/2)
	y = (surface.get_height()/2) - (newSurface.get_height()/2)

	return [x,y]

def reverse(binary,val):
	if binary: 	return False
	else:		return True

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
	fpsPrint()

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

	symbol(player.life,LIFE_IMG,ppos)
	symbol(player.bombs,BOMB_IMG,bpos)

def fpsPrint():
	x = 	str(fps.get_fps())[:5] + " fps"
	disp = 	fontObj.render(x,True,BLACK)
	pos = 	[OVERLAX-disp.get_width(),OVERLAY-disp.get_height()]

	screen.blit(disp,pos)

def playSound(filename):
	sound = loadSound(filename)

def loadSound(filename):
	loc = os.path.join(os.getcwd(),"Sound",filename)


def symbol(integer,img,pos):
	size = list(img.get_size())
	overlay.blit(img,(0,0))

	size[0] += 5
	size[0] *= integer

	ipos = img.get_width() + 5

	x = pygame.Surface(size,pygame.SRCALPHA,32)

	for i in range(integer):
		x.blit(img,((ipos*i),0))

	screen.blit(x,pos)

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
score = 		0
cooldown = 		0
messages = 		{} #{<fontObj>:<pos>}
bomb_name = 	""

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
fontObj = 	pygame.font.Font(os.path.join(os.path.abspath(os.getcwd()),'Fonts','THSpatial.ttf'),29)
last_time = 0

pygame.display.set_caption('Dot Boss Battle')
overlay.fill(WHITE)

screen.blit(overlay,OVERPOS)

posx = (overlay.get_width()/2)-5

player = 		Player(x,y,[posx,overlay.get_height()-5],speed,"player.png",2)
boss =			dot_boss(x,y,[posx,40],life=1000,lives=2,speed=[-2,0])

playerBullet = 	pygame.sprite.Group()
bossBullet = 	pygame.sprite.Group()
bombBullet = 	pygame.sprite.Group()
all_bullets = 	pygame.sprite.Group()
playerGroup = 	pygame.sprite.Group(player)
bossGroup = 	pygame.sprite.Group(boss)
all_sprites =	pygame.sprite.Group(player,boss)

######COMMENT THIS OUT LATER######
player.setPower("max")

while True:
	all_bullets.add(x for x in playerBullet.sprites())
	all_bullets.add(x for x in bossBullet.sprites())
	all_bullets.add(x for x in bombBullet.sprites())

	overlay.fill(WHITE)
	for event in pygame.event.get():
		if event.type == QUIT: shutdown()

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE: shutdown()

			# if event.key == K_DOWN:   direction2[1] =  player.speed
			# if event.key == K_UP:     direction2[1] = -player.speed
			# if event.key == K_LEFT:   direction2[0] = -player.speed
			# if event.key == K_RIGHT:  direction2[0] =  player.speed

			if event.key == K_DOWN:   d_move = True
			if event.key == K_UP:     u_move = True
			if event.key == K_LEFT:   l_move = True
			if event.key == K_RIGHT:  r_move = True
			
			if event.key == K_z and not player.bombing:
				shoot = True
			if event.key == K_x:
				if player.bombs != 0 and not player.bombing:
					bomb_name = player.bomb()

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
	 	if not player.god: player.kill()

	if pygame.sprite.spritecollide(boss,playerBullet,True):
		boss.setLife(-1)
		score += 10
	if pygame.sprite.spritecollide(boss,bombBullet,False):
		boss.setLife(-5)

	for b in bossBullet.sprites():
		if pygame.sprite.spritecollide(b,bombBullet,False):
			all_bullets.remove(b)
			bossBullet.remove(b)

	if float(pygame.time.get_ticks())/1000 - player.death_time >= 3:
		player.god = False

	if player.bombing:
		if not boss.life <= 0 and not boss.lives <= 1:
			score += 10
		player.god = 	True
		focus = True
		bomb_fin = False
		messages[bomb_name] = (0, overlay.get_height()-(bomb_name.get_height()+5))
		#laser 	{
		#		insert code here
		#		}
		if len(bombBullet.sprites()) <= 0:
			player.bombing = 	False
			player.god = 		False
			focus = 			False
			bomb_fin = 			False

			clear_b(bossBullet)
			clear_b(playerBullet)
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

	offscreen(playerBullet)
	offscreen(bossBullet)
	offscreen(bombBullet)

	if shoot and not lose and not player.bombing: player.shoot()
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

	for i in all_bullets.sprites():
		i.drawSprite()

	for l in range(boss.lives-1):
		#display all health bars
		pygame.draw.line(overlay,BLUE,(5*l,5),(5+(5*l),5),3)

	for m in messages: overlay.blit(m,messages[m])
	
	#display boss health bar
	boss.dispLife()

	score += player.graze()

	fps.tick(FPS)
	info = [HI,
			score,
			"",
			"",
			player.grazep]

	updateScreen(S_BKG)

	pygame.display.update()

nuclear = u'\u2622'