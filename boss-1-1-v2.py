# WARNING! THIS FILE HAS BEEN DEPRECATED AND IS NO LONGER USED BY THE REST OF THE PROGRAM!
#  IT IS BEING LEFT HERE FOR REFERENCE ONLY!

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
'Add logging'															#COMPLETE
'Add config file'														#COMPLETE
'Fix music delay'														#COMPLETE? (Still a small delay, but not as noticable as before)

'Add grazing mechanics' 												#Nearly Complete (Still grazing when hit)
'Add spell-timer'														#Nearly Complete (Timer runs a bit slow for some reason: probably FPS)
'Modularize code and split code into separate files'					#Nearly Complete (Still moving some things around)

'Add point system' 														#Partially Complete (HI-Score and saving score not done)
'Add system flags'														#Partially Complete (the only system flag is for disabling music)

'Have characters "talk" (sprite cutins)'								#INCOMPLETE
'Create proper images/backgrounds'										#INCOMPLETE
'Add levels'															#INCOMPLETE
'More bullet types'														#INCOMPLETE
'Bullet Patterns'														#INCOMPLETE
'Make spell cards (Including player bomb) classes'						#INCOMPLETE
'Fix Player bomb'														#INCOMPLETE (Bomb completely broken, will probably need to rework entirely)
'Add menus for various things'											#INCOMPLETE
'Add manifest file and launcher script'									#INCOMPLETE

from bin.lib.debugger import *

#Initialize the debugging engine
# We must do this before anything else, so that other files have access to config.tmpcfg
# This won't be necessary once the config.cfg file has been implemented
debugInit()

import pygame,sys,random,os
from pygame.locals import *
from bin.lib.basic import *
from bin.lib.sprites import *

#Keep constants in a separate folder to make the code less cluttered
from bin.lib.constants import *

#Keep all global variables in a separate file so that any part of the program can access them
from bin.lib.globalVar import *
from bin.lib.dependencies import *

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
			logging("Invalid speach tag. " + i.split(":")[0] + " is not valid.","err")
			# print "TalkError: Invalid speach tag.", i.split(":")[0], "is not valid."
			return [False] + + [x for x in [None for y in range(5)]]

		text[text.index(i)] = i.split(":")[1]

	box = pygame.Surface((OVERLAX-20,OVERLAY-200))

	return ([True,box,text,bosst,playert,pygame.time.get_ticks()])

#EXPERIMENTAL CLASSES
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

	def Card(self):
		'''This will spawn bullets when SpellCard is called'''
		pass

	def isStart(self):
		return self.start

	def getName(self):
		return self.name

	def dispName(self,surf,pos,font,color=BLACK):
		namee = font.render(namee,True,color)
		surf.blit(namee,pos)

	def ChangeBKG(self,img,surf):
		'''Don't know how to successfully use this yet, so I'm leaving it blank for now'''
		pass

class LargeEX(SpellCard):
	def __init__(self,owner,ownerGroup):
		SpellCard.__init__(self,30000,"Large X: Generic Danmaku",owner,ownerGroup)

		self.spawn2 = [0,0]
		self.spawn3 = [OVERLAX-40,0]
		self.ctime = float(pygame.time.get_ticks())/1000 - float(self.last_time)/1000

	def Card(self):
		# self.shoot(5,group,surf)
		if self.start:
			self.ctime = float(pygame.time.get_ticks())/1000 - float(self.last_time)/1000

			if self.ctime >= 0.3:
				b2 = bullet(self.x,self.y,spawn2,'img-77.png',(5,5))
				b = bullet(self.x,self.y,spawn3,'img-77.png',(-5,5))

				self.last_time = pygame.time.get_ticks()

				self.ownerGroup.add(b)
				self.ownerGroup.add(b2)

#NOTE: I don't have a spot to put this right now, so I'm going to leave it here
START_POS_2 = 	((OVERLAX-1)-loadImage("player.png").get_width(),1) #<-- makes sure the image doesn't start offscreen

def_info = ["HI-Score: ",
		"Score: ",
		"Player",
		"Bomb",
		"Graze: ",
		"Point: "]

pygame.mixer.pre_init(frequency=22050, size=-16, buffer=512)
pygame.init()

pygame.display.set_caption('Dot Boss Battle')
overlay.fill(WHITE)

screen.blit(overlay,OVERPOS)

player = Player(x,y,[posx,OVERLAY-5],speed,"player.png",2)

#Set the boss's life to any positive integer, but I'm leaving it at 100 right now for testing
boss = dot_boss(fontObj,[posx,40],life=100,lives=2,speed=[-2,0])

playerGroup.add(player)
bossGroup.add(boss)
all_sprites.add(player,boss)

player.setPower("max") #COMMENT THIS OUT LATER

if "-no_music" in sys.argv:
	logging("Not playing music.","std")
else:
	playMusic("th00_02.ogg")

#This isn't going to be used for anything yet, but will be used as a way to quickly skip to stages
if "-stage=" in sys.argv:
	stage = sys.argv[sys.argv.index("-stage=") + 1]
	logging("Loading stage " + stage + "...","std")

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
			if event.key == K_DOWN:   	d_move = False
			if event.key == K_UP:     	u_move = False
			if event.key == K_LEFT:   	l_move = False
			if event.key == K_RIGHT:  	r_move = False

			if event.key == K_z:		shoot = False

			if event.key == K_LSHIFT or event.key == K_RSHIFT:
				focus = False

			if event.key == K_LCTRL or event.key == K_RCTRL:
				ctrl_hold = False

	move([d_move,u_move,l_move,r_move],direction2,player)
						
	######Update positions of sprites######
	boss.rect.x -= DIRECTION1[0]
	boss.rect.y -= DIRECTION1[1]

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

	for i in itemGroup.sprites():
		if pygame.sprite.spritecollide(i,playerGroup,False):
			collected = player.collect(i)

			if collected:
				for g in i.groups():
					g.remove(i)

				del i

	for b in bossBullet.sprites():
		if pygame.sprite.spritecollide(b,bombBullet,False):
			for g in b.groups():
				g.remove(b)

			player.score += 10
			# all_bullets.remove(b)
			# bossBullet.remove(b)

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
		drops = boss.kill()

		for d in drops:
			if type(d) == 	Powerup: 	powerGroup.add(d)
			elif type(d) == PointItem: 	scoreGroup.add(d)
			elif type(d) == Lifeup: 	lifeGroup.add(d)
			elif type(d) == Bombup: 	bombupGroup.add(d)

			else: logging("[Unknown item: "+ str(type(d)) +"]","err")

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
	else: boss.update()

	if player.life < 0 or lose:
		all_sprites.remove(x for x in playerBullet.sprites())
		all_sprites.remove(x for x in bossBullet.sprites())
		
		playerBullet.empty()
		bossBullet.empty()
		
		for i in player.groups():
			i.remove(player)

		# all_sprites.remove(player)
		# playerGroup.remove(player)

		player.life = 0

		x = fontObj.render('YOU LOSE!',True,BLACK)
		overlay.blit(x,surf_center(overlay,x))
		# messages[x] = surf_center(overlay,x)
		lose = True

		stopMusic()
	else:
		#Run all Player methods
		player.update(direction2)
		player.drawSprite(overlay)
		player.setFocus(focus)
		player.graze(bossBullet)
		if shoot and not player.playerbomb:
			player.shoot(playerBullet)

		if player.playerbomb:
			player.bomb(fontObj,overlay,bombBullet,bossBullet)
		else:
			player.playerbomb = False

		#Run all Boss methods
		boss.attack(bossBullet,overlay,args=5)
		last_time = pygame.time.get_ticks()/1000


	offscreen(all_bullets,OVERSIZE)
	offscreen(powerGroup,OVERSIZE)
	offscreen(scoreGroup,OVERSIZE)

	# if shoot and not lose and not player.playerbomb: player.shoot(playerBullet)

	# if player.playerbomb: player.bomb(fontObj,overlay,bombBullet,bossBullet)
	# else: player.playerbomb = False

	# if player.bomb_flash and False:
	if False:
		flashc[3] -= 1
		flashs.fill(flashc)

		if flashc[3] <= 0:
			player.bomb_flash = False

	for b in all_bullets.sprites(): b.update()

	# if not win and not lose:
	# 	boss.attack(bossBullet,overlay,args=5)

	# 	last_time = pygame.time.get_ticks()/1000

	if win: clear_b(bossBullet)

	all_sprites.draw(overlay)
	all_bullets.draw(overlay)
	itemGroup.draw(overlay)

	for i in all_bullets.sprites():
		i.drawSprite(overlay)
		if type(i) is laser: #This does run
			# print "IT'S A LASER!"
			i.kill(pygame.time.get_ticks())

	for i in itemGroup.sprites():
		i.update()

	for l in range(boss.lives-1):
		#display all health bars
		pygame.draw.line(overlay,BLUE,(5*l,5),(5+(5*l),5),3)

	#This may be deprecated soon
	for m in messages: overlay.blit(m,messages[m])
	
	#display boss health bar
	boss.dispLife(overlay)
	boss.spellTimer.dispTime((OVERLAX/2-20,5),overlay,fontObj,cutoff=1)

	# score += player.graze()

	fps.tick(FPS)

	info = [HI,
			# score,
			player.score,
			"",
			"",
			player.grazep,
			player.pointColl]

	updateScreen(S_BKG)

	pygame.display.update()

nuclear = u'\u2622'