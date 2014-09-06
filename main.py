#Tyler Robbins
#5/19/14
#Boss-1-1 v2
#Boss battle, using all of the pygame components I've learned up till this point.

#NOTE TO SELF: After the next commit, replace boss with Vivian James

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
'Add launcher'															#COMPLETE
'Fix music delay'														#COMPLETE? (Still a small delay, but not as noticable as before)
'Fix order that sprites get rendered in'								#COMPLETE
'Fix game crashing when final spell timer runs out'						#COMPLETE (fixed with permaKill())

'Add grazing mechanics' 												#Nearly Complete (Still grazing when hit)
'Add spell-timer'														#Nearly Complete (Timer runs a bit slow for some reason: probably FPS)
'Modularize code and split code into separate files'					#Nearly Complete (Still moving some things around)

'Add point system' 														#Partially Complete (HI-Score and saving score not done)
'Add system flags'														#Partially Complete (the only system flag is for disabling music)
'Make spell cards (Including player bomb) classes'						#Partially Complete (Some old style spell cards still exist)

'Add replay system (save playthrough)'									#INCOMPLETE
'Add levels'															#INCOMPLETE
'Add menus for various things'											#INCOMPLETE
'Add manifest file'														#INCOMPLETE
'Add custom boss idle methods'											#INCOMPLETE
'Add more bullet types'													#INCOMPLETE
'Have characters "talk" (sprite cutins)'								#INCOMPLETE
'Create proper images/backgrounds'										#INCOMPLETE
'Bullet Patterns'														#INCOMPLETE
'Fix Player bomb'														#INCOMPLETE (Bomb completely broken, will probably need to rework entirely)
'Clean-up/re-write boss and player code'								#INCOMPLETE (boss timer crashes game on last life, player bomb broken. Code for both is a mess and should just be re-written)
'Fix duplicate point and graze bug'										#INCOMPLETE (pointColl gets + 2, graze sometimes adds 2 instead of 1)
'Fix player hitbox appearing at the beginning of the game'				#INCOMPLETE

from bin.lib.debugger import *

#Initialize the debugging engine
# We must do this before anything else, so that other files have access to config.tmpcfg
if not isDebugInit():
	debugInit()

import pygame,sys,random,os
from pygame.locals import *
from bin.lib.basic import *
from bin.lib.sprites import *
from bin.lib.settings import *
from bin.lib.entities import *
from bin.lib.constants import * #Keep constants in a separate folder to make the code less cluttered
from bin.lib.globalVar import * #Keep all global variables in a separate file so that any part of the program can access them
from bin.lib.dependencies import *

class laser(Bullet):
	def __init__(self,x,y,num,life,img,speed,playerb=False):
		bullet.__init__(self,x,y,num,img,speed,playerb=playerb)
		self.life = life
		self.birth = pygame.time.get_ticks()

	def kill(self,ctime):
		if not self.life == -1:
			if (float(ctime)/1000) - (float(self.birth)/1000) >= self.life:
				if self.playerb:
					all_bullets.remove(self)
					player.bulletGroup.remove(self)

				else:
					all_bullets.remove(self)
					player.bulletGroup.remove(self)

				del self

def updateScreen(BKG,bkg_override=None):
	# if not bkg_override:
	screen.blit(BKG,(0,0))
	# else:
		# screen.blit(bkg_override,(0,0))

	screen.blit(overlay,OVERPOS)

	infoPrint(def_info,info)
	fpsPrint(fps,OVERSIZE,fontObj,screen)

	pygame.display.update()

def renderSprites():
	for i in all_bullets.sprites():
		i.drawSprite(overlay)
		if type(i) is laser: #This does run
			# print "IT'S A LASER!"
			i.kill(pygame.time.get_ticks())

		i.idle()

	player.drawSprite(overlay)
	all_sprites.draw(overlay)
	all_bullets.draw(overlay)
	itemGroup.draw(overlay)

def runIdle(sprites={}):
	'''{sprite:[args]}'''
	for sprite in sprites:
		args = sprites[sprite]
		sprite.idle(*args)

def infoPrint(str_info,data_info):
	new_info = []
	n = (OVERPOS[0] + 10 + OVERLAX, 50) #Y position of information

	for i in str_info:
		loc = str_info.index(i)

		x = i + str(data_info[loc])
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

def_info = ["HI-Score: ",
		"Score: ",
		"Player",
		"Bomb",
		"Graze: ",
		"Point: "]

bkg_override = None

pygame.mixer.pre_init(frequency=22050, size=-16, buffer=512)
pygame.init()

pygame.display.set_caption('Dot Boss Battle')
overlay.fill(WHITE)

screen.blit(overlay,OVERPOS)

bossGroup.add(boss)
playerGroup.add(player)
all_sprites.add(player,boss)

if getSetting('full_power'):
	player.setPower("max")

if getSetting('full_life'):
	player.setLife(player.maxLife)

if getSetting('enable_music'):
	playMusic("th00_02.ogg")
else:
	logging("Not playing music.","std")

#This isn't going to be used for anything yet, but will be used as a way to quickly skip to stages
if "-stage=" in sys.argv:
	stage = sys.argv[sys.argv.index("-stage=") + 1]
	logging("Loading stage " + stage + "...","std")

boss.spellTimer.startTimer()

while True:
	all_bullets.add(x for x in player.bulletGroup.sprites())
	all_bullets.add(x for x in boss.bulletGroup.sprites())
	all_bullets.add(x for x in bombBullet.sprites())

	itemGroup.add(x for x in scoreGroup.sprites())
	itemGroup.add(x for x in powerGroup.sprites())

	if not bkg_override:
		overlay.fill(WHITE)
	else:
		overlay.blit(bkg_override,(0,0))

	for event in pygame.event.get():
		if event.type == QUIT: shutdown()

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE: shutdown()

			if event.key == K_DOWN:   d_move = True
			if event.key == K_UP:     u_move = True
			if event.key == K_LEFT:   l_move = True
			if event.key == K_RIGHT:  r_move = True
			
			if event.key == K_z and not player.playerbomb:
				# shoot = True
				player.shooting = True

			if event.key == K_x and False: #This is to prevent the bomb from working
				if player.bombs != 0 and not player.bombing:
					# bomb_name = player.bomb()
					player.playerbomb = True

			if event.key == K_LSHIFT or event.key == K_RSHIFT:
				# focus = True
				player.setFocus(True)

			if event.key == K_RETURN:
				#overlay technical information in the command prompt.
				print "PLAYER", player.life, ": ", player.bombing, ": ", player.god
				print "BOSS", boss.life, ": ", boss.lives

				log_string = "PLAYER " + str(player.life) + ": " + str(player.bombing) + ": " + str(player.god) + "\nBOSS " + str(boss.life) + ": " + str(boss.lives)

				logging("Overlay information:","test",log_string)
			
			if event.key == K_RCTRL or event.key == K_LCTRL:
				# Key-command activated cheats
				ctrl_hold = True
				print "CTRL"

			if event.key == K_w and ctrl_hold:
				#Emergency shutdown
				logging("Initiating emergency shutdown...","std")
				print "Initiating emergency shutdown..."
				shutdown()

			if event.key == K_g and ctrl_hold:
				#Toggle god mode
				# if player.god: 	player.god = False
				# else: 			player.god = True

				player.makeGod()

				print "GOD",player.god

			if event.key == K_h and ctrl_hold:
				#Show bullet and enemy hitboxes
				for i in all_bullets.sprites():
					i.showHitBox(show=not i.showHB)

			collide = False
			
		if event.type == KEYUP:
			if event.key == K_DOWN:   	d_move = False
			if event.key == K_UP:     	u_move = False
			if event.key == K_LEFT:   	l_move = False
			if event.key == K_RIGHT:  	r_move = False

			if event.key == K_z:		player.shooting = False

			if event.key == K_LSHIFT or event.key == K_RSHIFT:
				# focus = False
				player.setFocus(False)

			if event.key == K_LCTRL or event.key == K_RCTRL:
				ctrl_hold = False

	move([d_move,u_move,l_move,r_move],direction2,player)

	######Sprite collision detection######
	if (pygame.sprite.spritecollide(player,bossGroup,False) or pygame.sprite.spritecollide(player,boss.bulletGroup,True)) and not collide:
	 	collide = True
	 	if not player.isGod and not player.bombing: player.kill()

	if pygame.sprite.spritecollide(boss,player.bulletGroup,True):
		boss.addLife(-1)
		player.score += 10
	if pygame.sprite.spritecollide(boss,bombBullet,False):
		boss.addLife(-5)
		# score += 10
		player.score += 10

	for b in boss.bulletGroup.sprites():
		if pygame.sprite.spritecollide(b,bombBullet,False):
			# b.setLife(-1)
			pos = [b.rect.x,b.rect.y]
			b = StarPointItem(pos)

			player.score += 10

	if float(pygame.time.get_ticks())/1000 - player.death_time >= 3:
		# player.makeGod()
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

			clear_b(boss.bulletGroup)
			clear_b(player.bulletGroup)

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
		all_bullets.remove(x for x in player.bulletGroup.sprites())
		all_bullets.remove(x for x in boss.bulletGroup.sprites())
		player.bulletGroup.empty()
		boss.bulletGroup.empty()
		all_sprites.remove(boss)

		boss.rect.x = overlay.get_width()+10
		boss.rect.y = overlay.get_height()+10

		x = fontObj.render('YOU WIN!',True,BLACK)
		# overlay.blit(x,surf_center(overlay,x))
		messages = {}

		messages[x] = surf_center(overlay,x)
		win = True

		pygame.mixer.music.fadeout(5)

		boss.spellTimer.pauseTimer()

	if False and player.life < 0 or player.lose:
		all_sprites.remove(x for x in player.bulletGroup.sprites())
		all_sprites.remove(x for x in boss.bulletGroup.sprites())
		
		player.bulletGroup.empty()
		boss.bulletGroup.empty()
		
		for i in player.groups():
			i.remove(player)

		# all_sprites.remove(player)
		# playerGroup.remove(player)

		player.life = 0

		x = fontObj.render('YOU LOSE!',True,BLACK)
		overlay.blit(x,surf_center(overlay,x))
		# messages[x] = surf_center(overlay,x)

		stopMusic()

	renderSprites()

	if player.getIsDead():
		x = fontObj.render('YOU LOSE!',True,BLACK)
		overlay.blit(x,surf_center(overlay,x))
	else:
		#Run all Player methods
		player.update(direction2)
		player.graze(boss.bulletGroup)

		if player.shooting and not player.playerbomb:
			player.shoot(player.bulletGroup)

		if player.playerbomb:
			player.bomb(fontObj,overlay,bombBullet,boss.bulletGroup)
		else:
			player.playerbomb = False

		#Run all Boss methods
		bkg_override = boss.attack(overlay,args=5)

	offscreen(OVERSIZE,groups=[all_bullets,powerGroup,scoreGroup])

	for b in all_bullets.sprites(): b.update()

	for i in itemGroup.sprites():
		i.idle(player)
		i.update()

	info = [HI,
			# score,
			player.score,
			"",
			"",
			player.grazep,
			"/".join([str(player.pointColl),str(player.maxPointColl)])]
	
	runIdle(sprites={player:[],boss:[]})
	updateScreen(S_BKG,bkg_override=bkg_override)

	fps.tick(FPS)

nuclear = u'\u2622'