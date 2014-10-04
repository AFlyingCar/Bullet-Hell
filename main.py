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
'Symbols for players[current_playr] lives and player bombs'				#COMPLETE
'Add music/sound effects'												#COMPLETE
'Add power up items and point items'									#COMPLETE
'Add logging'															#COMPLETE
'Add config file'														#COMPLETE
'Add launcher'															#COMPLETE
'Fix music delay'														#COMPLETE? (Still a small delay, but not as noticable as before)
'Fix order that sprites get rendered in'								#COMPLETE
'Fix game crashing when final spell timer runs out'						#COMPLETE
'Fix the order in which sprites get rendered first'						#COMPLETE
'Add custom boss idle methods'											#COMPLETE
'Bullet Patterns'														#COMPLETE
'Fix powerup items not being collected by the player.'					#COMPLETE

'Add grazing mechanics' 												#Nearly Complete (Still grazing when hit)
'Add spell-timer'														#Nearly Complete (Timer runs a bit slow for some reason: probably FPS)
'Modularize code and split code into separate files'					#Nearly Complete (Still moving some things around)

'Add point system' 														#Partially Complete (HI-Score and saving score not done)
'Make spell cards (Including player bomb) classes'						#Partially Complete (Player bomb still has to be rebuilt)

'Add replay system (save playthrough)'									#INCOMPLETE
'Add levels'															#INCOMPLETE
'Add menus for various things'											#INCOMPLETE
'Add manifest file'														#INCOMPLETE
'Add more bullet types'													#INCOMPLETE
'Add more comments to everything'										#INCOMPLETE
'Have characters "talk" (sprite cutins)'								#INCOMPLETE
'Create proper images/backgrounds'										#INCOMPLETE
'Fix Player bomb'														#INCOMPLETE (Bomb completely broken, will probably need to rework entirely)
'Clean-up/re-write boss and player code'								#INCOMPLETE (boss timer crashes game on last life, players[current_playr] bomb broken. Code for both is a mess and should just be re-written)
'Fix duplicate point and graze bug'										#INCOMPLETE (pointColl gets + 2, graze sometimes adds 2 instead of 1)
'Fix player hitbox appearing at the beginning of the game'				#INCOMPLETE

'Add system flags'														#Irrelavent

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

def updateScreen(BKG,bkg_override=None):
	screen.blit(BKG,(0,0))

	screen.blit(overlay,OVERPOS)

	infoPrint(def_info,info)
	fpsPrint(fps,OVERSIZE,fontObj,screen)

	pygame.display.update()

def renderSprites():
	players[current_playr].drawSprite(overlay)
	all_sprites.draw(overlay)
	itemGroup.draw(overlay)

	#Render bullet sprites last

	for i in all_bullets.sprites():
		i.drawSprite(overlay)
		if type(i) is laser: #This does run
			# print "IT'S A LASER!"
			i.kill(pygame.time.get_ticks())

		i.idle()

	all_bullets.draw(overlay)

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

	x = "POWER: " + str(players[current_playr].getPower())
	i = fontObj.render(x,True,WHITE)
	screen.blit(i,n)

	symbol(players[current_playr].life,LIFE_IMG,ppos,screen)
	symbol(players[current_playr].bombs,BOMB_IMG,bpos,screen)

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

prgname = getSetting('prg_name') + " " + getSetting('game_version')

pygame.display.set_caption(prgname)
overlay.fill(WHITE)

screen.blit(overlay,OVERPOS)

bosses = 	bossGroup.sprites()
players = 	playerGroup.sprites()

if getSetting('full_power'):
	# Give player max power
	players[current_playr].setPower("max")

if getSetting('full_life'):
	# Give player max life (10 hearts)
	players[current_playr].setLife(players[current_playr].maxLife)

# if getSetting('enable_music'):
mus = bosses[current_boss].getMusic()
playMusic(mus,getSetting("musicVolume"))

logging("Music has been " + ('enabled at ' + str(getSetting('musicVolume')) + ' volume.' if getSetting('enable_music') else 'disabled.'),"std")

bosses[current_boss].StartBossFight()

while True:
	all_bullets.add(x for x in players[current_playr].bulletGroup.sprites())
	all_bullets.add(x for x in bosses[current_boss].bulletGroup.sprites())
	all_bullets.add(x for x in bombBullet.sprites())

	itemGroup.add(x for x in scoreGroup.sprites())
	itemGroup.add(x for x in powerGroup.sprites())

	bosses[current_boss].getSpellBKG() #This may need to be moved later, as this is a terrible spot for this line

	for event in pygame.event.get():
		if event.type == QUIT: shutdown()

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE: shutdown()

			if event.key == K_DOWN:   d_move = True
			if event.key == K_UP:     u_move = True
			if event.key == K_LEFT:   l_move = True
			if event.key == K_RIGHT:  r_move = True
			
			if event.key == K_z:

				players[current_playr].shooting = True

			if event.key == K_x and False: #This is to prevent the bomb from working
				if players[current_playr].bombs != 0 and not players[current_playr].bombing:
					# bomb_name = players[current_playr].bomb()
					players[current_playr].playerbomb = True

			if event.key == K_LSHIFT or event.key == K_RSHIFT:
				# focus = True
				players[current_playr].setFocus(True)

			if event.key == K_RETURN:
				#overlay technical information in the command prompt.
				# print "PLAYER", players[current_playr].life, ": ", players[current_playr].bombing, ": ", players[current_playr].god
				# print "BOSS", bosses[current_boss].life, ": ", bosses[current_boss].lives

				# print type(str(pygame.mixer.music.get_volume()))
				log_string = (
					"PLAYER LIFE=" + str(players[current_playr].life) + ": BOMBING=" + str(players[current_playr].bombing) + ": GOD=" + 
					str(players[current_playr].god) + ": POSITION=" + str(players[current_playr].getPos()) + 
					"\nBOSS LIFE=" + str(bosses[current_boss].life) + ": LIVES=" + str(bosses[current_boss].lives) + 
					": POSITION=" + str(bosses[current_boss].getPos()) + "\nMUSIC VOLUME: " + str(pygame.mixer.music.get_volume()) + ":" + 
					("ON" if getSetting("enable_music") else "OFF"))

				print log_string

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
				# if players[current_playr].god: 	players[current_playr].god = False
				# else: 			players[current_playr].god = True

				players[current_playr].makeGod()

				print "GOD",players[current_playr].god

			if event.key == K_h and ctrl_hold:
				#Show bullet and enemy hitboxes
				for i in all_bullets.sprites():
					i.showHitBox(show=not i.showHB)

			if event.key == K_e and ctrl_hold:
				#Force error messages to occur. This is only to test debugging stuff and should be removed in released verisons.
				raise Exception("Error forced by user.")

			if event.key == (K_COMMA or K_LESS) and ctrl_hold:
				vol = pygame.mixer.music.get_volume() - 0.1
				pygame.mixer.music.set_volume(vol)

			if event.key == (K_PERIOD or K_GREATER) and ctrl_hold:
				vol = pygame.mixer.music.get_volume() + 0.1
				pygame.mixer.music.set_volume(vol)

			if event.key == K_s and ctrl_hold:
				takeScreenShot(screen)

			collide = False
			
		if event.type == KEYUP:
			if event.key == K_DOWN:   	d_move = False
			if event.key == K_UP:     	u_move = False
			if event.key == K_LEFT:   	l_move = False
			if event.key == K_RIGHT:  	r_move = False

			if event.key == K_z:		players[current_playr].shooting = False

			if event.key == K_LSHIFT or event.key == K_RSHIFT:
				# focus = False
				players[current_playr].setFocus(False)

			if event.key == K_LCTRL or event.key == K_RCTRL:
				ctrl_hold = False

	move([d_move,u_move,l_move,r_move],direction2,players[current_playr])

	######Sprite collision detection######
	if pygame.sprite.spritecollide(players[current_playr],bossGroup,False) and not collide:
		collide = True
		
		if not players[current_playr].isGod() and not players[current_playr].bombing:
			players[current_playr].addLife(-1)

	if not players[current_playr].getIsDead():
		if pygame.sprite.spritecollide(players[current_playr],bosses[current_boss].bulletGroup,True) and not collide:
			collide = True
			
			if not players[current_playr].isGod() and not players[current_playr].bombing:
				players[current_playr].addLife(-1)

	if pygame.sprite.spritecollide(bosses[current_boss],players[current_playr].bulletGroup,True):
		bosses[current_boss].addLife(-players[current_playr].damage)
		players[current_playr].score += 10
	if pygame.sprite.spritecollide(bosses[current_boss],bombBullet,False):
		bosses[current_boss].addLife(-5)
		# score += 10
		players[current_playr].score += 10

	for b in bosses[current_boss].bulletGroup.sprites():
		if pygame.sprite.spritecollide(b,bombBullet,False):
			# b.setLife(-1)
			pos = [b.rect.x,b.rect.y]
			b = StarPointItem(pos)

			players[current_playr].score += 10

	if float(pygame.time.get_ticks())/1000 - players[current_playr].death_time >= 3:
		# players[current_playr].makeGod()
		players[current_playr].god = False

	if players[current_playr].bombing and False: #Don't want this to run, but don't want to delete until we know it's obosolete
		# if not boss.life <= 0 and not boss.lives <= 1:
		# 	score += 10
		players[current_playr].god = 	True
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

			players[current_playr].bombing = 	False
			players[current_playr].god = 		False
			focus = 			False
			bomb_fin = 			False

			clear_b(boss.bulletGroup)
			clear_b(players[current_playr].bulletGroup)

		# for i in bombBullet: i.update()

	if False and players[current_playr].life < 0 or players[current_playr].lose:
		all_sprites.remove(x for x in players[current_playr].bulletGroup.sprites())
		all_sprites.remove(x for x in boss.bulletGroup.sprites())
		
		players[current_playr].bulletGroup.empty()
		boss.bulletGroup.empty()
		
		for i in players[current_playr].groups():
			i.remove(players[current_playr])

		# all_sprites.remove(players[current_playr])
		# playerGroup.remove(players[current_playr])

		players[current_playr].life = 0

		x = fontObj.render('YOU LOSE!',True,BLACK)
		overlay.blit(x,surf_center(overlay,x))
		# messages[x] = surf_center(overlay,x)

		stopMusic()

	renderSprites()

	if True:
		#Run all Player methods
		#NOTE: These need to be moved into the player class at some point
		players[current_playr].update(direction2)
		players[current_playr].graze(bosses[current_boss].bulletGroup)

		if players[current_playr].playerbomb:
			players[current_playr].bomb(fontObj,overlay,bombBullet,bosses[current_boss].bulletGroup)
		else:
			players[current_playr].playerbomb = False

	# bkg_override = boss.getSpellBKG()

	offscreen(OVERSIZE,groups=[all_bullets,powerGroup,scoreGroup])

	for b in all_bullets.sprites(): b.update()

	for i in itemGroup.sprites():
		i.idle(players[current_playr])
		i.update()

	info = [HI,
			players[current_playr].score,
			"",
			"",
			players[current_playr].grazep,
			"/".join([str(players[current_playr].pointColl),str(players[current_playr].maxPointColl)])]
	
	runIdle(sprites={players[current_playr]:[],bosses[current_boss]:[]})
	updateScreen(S_BKG,bkg_override=bkg_override)

	fps.tick(FPS)

nuclear = u'\u2622'