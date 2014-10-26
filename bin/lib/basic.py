#Tyler Robbins
#7/13/14
#Basic
#Contains basic loading functions

import pygame,os,sys,math
from pygame.locals import *
from globalVar import *
from debugger import *
from settings import *
from color import *

s_init_check = getSetting('checkMixerInit') # <- Whether to check for an initialized mixer

def takeScreenShot(surface,path=getSetting('path_screenshot')):
	# filename = genLogName(newName=)
	a = 1
	for i in os.listdir(path):
		if i.startswith("ScreenShot") and i.endswith(".bmp"): a += 1

	filename = "ScreenShot-(" + str(a) + ").bmp"
	filename = os.path.join(path,filename)

	pygame.image.save(surface,filename)

	logging("Screenshot saved in " + filename,"std")

######Load images from ./Images and return a blank Surface if the image couldn't be found
def loadImage(filename,path=getSetting('path_image'),fail_size=[10,10]):
	if type(filename) == pygame.Surface:
		return filename

	else:
		# loc = os.path.join(os.getcwd(),"Images",filename)
		loc = os.path.join(path,filename)

		if os.path.exists(loc):
			pic = pygame.image.load(loc)
			logging("Successfully loaded " + filename, "std")
			return pic

		else:
			msg1 = "Could not find " + filename + " in \\Images!"
			msg2 = "Loading blank image..."
			logging(msg1,"err",msg2)
			# print "ImageError: Could not find", filename, "in \\Images!"
			# print "Loading blank image..."

			pic = pygame.Surface(fail_size)
			pic.fill(PURPLE)
			return pic

def loadAnim(animName):
	path = os.path.join(getSetting('path_anim'),animName)
	frames = []

	if not os.path.exists(path):
		logging("Path: " + path + " does not exist!","err","Loading blank animation...")
		return frames

	for f in os.listdir(path):
		frames.append(loadImage(f,path))

	return frames

######Load sounds from ./Sound and returns an error if the file was not found,
###### or if pygame.mixer was not initialized
def loadSound(filename,volume=1.0):
	# path = os.path.join(os.getcwd(),"Sound",filename)
	path = os.path.join(getSetting('path_sound'),filename)

	if os.path.exists(path):
		if pygame.mixer.get_init():
			s = pygame.mixer.Sound(path)
			s.set_volume(volume)
			logging("Successfully loaded " + filename,"std")
			return s

		else:
			logging("Mixer not initialized!","warn")
			# print "Mixer not initialized!"

			if not s_init_check:
				while True:
					yn = raw_input("Initialize?(y/n) ")
					if yn is 'y':
						pygame.mixer.init()
						s_init_check = False
						break
					elif yn is 'n':
						# print "Warning: Mixer still not initialized!"
						# print "This could result in the program failing."
						logging("Warning: Mixer still not initialized!", "warn", "This could result in the program failing.")
						s_init_check = True
						break
					else:
						print "'y' or 'n' please!"

	else:
		# print "SoundError: Could not find", filename, "in \\Sound!"
		logging("Directory -> " + path + " does not exist!", "err")
		return "err"

def playSound(filename,volume=1.0):
	if getSetting('enable_sound'):
		if pygame.mixer.get_init():
			if type(filename) is pygame.mixer.Sound:
				filename.play()

			elif type(filename) is str:
				s = loadSound(filename,volume)

				if s == "err":
					pass

				if type(s) is pygame.mixer.Sound:
					s.play()

			else:
				# print "TypeError:", type(filename), "is not valid."
				logging("Invalid sound type " + type(filename),"err")
		else:
			logging("Unable to play sound. Mixer not initialized.","err")

	else:
		logging("Sound has not been enabled!","warn","Cannot play sound file: " + str(filename))

def stopSound(sound=None):
	'''Will stop a single sound from playing if a sound object is given. Otherwise, it will stop all sounds.'''
	if sound:
		sound.stop()
	else:
		pygame.mixer.stop()

def loadMusic(filename,volume=1.0):
	# path = os.path.join(os.getcwd(),"Music",filename)
	path = os.path.join(getSetting("path_music"),filename)

	if pygame.mixer.music.get_busy():
		pygame.mixer.music.fadeout(2)

	if os.path.exists(path):
		if pygame.mixer.get_init():
			pygame.mixer.music.load(path)
			pygame.mixer.music.set_volume(float(volume))
			return True
		else:
			# print "Mixer not initialized!"
			logging("Mixer not initialized!","warn")
			
			if not s_init_check:
				while True:
					yn = raw_input("Initialize?(y/n) ")
					if yn is 'y':
						pygame.mixer.init()
						s_init_check = False
						break
					elif yn is 'n':
						# print "Warning: Mixer still not initialized!"
						# print "This could result in the program failing."
						logging("Warning: Mixer still not initialized!", "warn", "This could result in the program failing.")
						s_init_check = True
						break
					else:
						print "'y' or 'n' please!"

	else:
		# print "Path:", path, "does not exist!"
		logging("Directory -> " + path + " does not exist!", "err")

def playMusic(filename,volume=1.0):
	if getSetting('enable_music'):
		s = loadMusic(filename,volume)

		if s:
			pygame.mixer.music.play(-1)
			logging("Successfully playing " + filename, "std")
		else:
			logging("An error has occurred when loading music: " + filename + ".", "err")
	else:
		logging("Music has not been enabled!","warn","Cannot play music file: " + str(filename))

def isPlaying(sound=None):
	'''Return whether or not sound is currently playing.'''
	if sound:
		return pygame.mixer.get_busy()
	else:
		return pygame.mixer.music.get_busy()

def stopMusic():
	'''Will stop all music from playing.'''
	if isPlaying():
		pygame.mixer.music.stop()

def offscreen(maxSize,groups=[]):
	#For bullets only
	OVERLAX = maxSize[0]
	OVERLAY = maxSize[1]

	for group in groups:
		for b in group.sprites():
			delete = False

			if b.rect.x <= (0-b.image.get_width()):
				b.addLife(-2)
				delete = True

			if b.rect.x >= OVERLAX:
				b.addLife(-2)
				delete = True

			if b.rect.y >= OVERLAY:
				b.addLife(-2)
				delete = True

			if b.rect.y <= (0-b.image.get_height()):
				b.addLife(-2)
				delete = True

			if delete: del b

def clear_b(groups=[],pointify=False):
	all_points = 0

	logging("Clearing screen...","std")

	for group in groups:
		for x in group.sprites():
			if pointify: # Give player points for every bullet left on-screen
				# player.score += 1000
				all_points += 1000

			for g in x.groups():
				g.remove(x)

			del x

		group.empty()

	return all_points

def changeSpeed(bullet,endPos,newSpeed=None):
	c_Speed = bullet.speed
	cPos = bullet.getPos()

	if newSpeed:
		newX = (c_Speed[0]/c_Speed[0]) * newSpeed
		newY = (c_Speed[1]/c_Speed[1]) * newSpeed
		c_Speed = [newX,newY]

	#Set X speed
	if cPos[0] > endPos[0] and (c_Speed[0]/c_Speed[0]) != -1:	c_Speed[0] *= -1
	elif cPos[0] < endPos[0] and (c_Speed[0]/c_Speed[0])*-1 != 1: c_Speed[0] *= -1
	
	#Set Y speed
	if cPos[1] > endPos[1] and (c_Speed[1]/c_Speed[1]) != -1:	c_Speed[1] *= -1
	elif cPos[1] < endPos[1] and (c_Speed[1]/c_Speed[1])*-1 != 1: c_Speed[1] *= -1

	return speed

def shutdown():
	logging("Shutting down pygame...", "std")
	# print "Shutting down pygame..."
	pygame.quit()
	logging("Pygame has shut down successfully!", "std")
	# print "Pygame has shut down successfully!"

	debugUnInit()

	sys.exit()

def surf_center(surface,newSurface=None):
	if newSurface:
		x = (surface.get_width()/2) - (newSurface.get_width()/2)
		y = (surface.get_height()/2) - (newSurface.get_height()/2)

		return [x,y]

	else:
		x = surface.get_width()/2
		y = surface.get_height()/2

		return [x,y]

def fpsPrint(fps,screenSize,fontObj,screen):
	OVERLAX = screenSize[0]
	OVERLAY = screenSize[1]

	x = 	str(fps.get_fps())[:5] + " fps"
	disp = 	fontObj.render(x,True,BLACK)
	pos = 	[OVERLAX-disp.get_width(),OVERLAY-disp.get_height()]

	screen.blit(disp,pos)

def symbol(integer,img,pos,screen):
	size = 		list(img.get_size())
	size[0] += 	5
	size[0] *= 	integer

	if size[0] < 0:
		size[0] = 0

	ipos = img.get_width() + 5
	
	try:
		x = pygame.Surface(size,pygame.SRCALPHA,32)

		for i in range(integer):
			x.blit(img,((ipos*i),0))

		screen.blit(x,pos)
	except BaseException as e:
		logging("An error occurred while trying to display GUI information.","err","\n".join([str(type(e)),str(e)]))

		size[0] = 0

		x = pygame.Surface(size,pygame.SRCALPHA,32)

		for i in range(integer):
			x.blit(img,((ipos*i),0))

		screen.blit(x,pos)

def dispText(text,surf,pos,fontObj,color=BLACK):
	f = fontObj.render(text,True,color)
	surf.blit(f,pos)

def move(moveList,direction,sprite):
	d_move,u_move,l_move,r_move = [i for i in moveList]
	# d_move = moveList[0]
	# u_move = moveList[1]
	# l_move = moveList[2]
	# r_move = moveList[3]

	#Change player direction based on pressed keys
	if r_move and not l_move: 	direction[0] =  sprite.speed
	elif l_move and not r_move: direction[0] = -sprite.speed
	elif r_move and l_move: 	direction[0] =  0
	else: 						direction[0] =  0
	
	if u_move and not d_move: 	direction[1] = -sprite.speed
	elif d_move and not u_move: direction[1] =  sprite.speed
	elif d_move and u_move: 	direction[1] =  0
	else: 						direction[1] =  0

	return [d_move,u_move,l_move,r_move]

def sprite_sheet(size,filename,pos=(0,0),path=getSetting('path_anim')):
    #Initial Values
    len_sprt_x,len_sprt_y = size #sprite size
    sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet

    # sheet = pygame.image.load(filename).convert_alpha() #Load the sheet
    sheet = loadImage(filename,path=path)

    # len_sprt_x = sheet.get_width()/size[0]
    # len_sprt_y = sheet.get_height()/size[1]

    sheet_rect = sheet.get_rect()
    sprites = []
    # print sheet_rect.height, sheet_rect.width
    for i in range(0,sheet_rect.height-len_sprt_y,size[1]):#rows
        # print "row"
        for i in range(0,sheet_rect.width-len_sprt_x,size[0]):#columns
            # print "column"
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x

        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    # print sprites

    logging("Successfully loaded spritesheet " + filename, "std")
    return sprites

def infoPrint(str_info,data_info):
	new_info = []
	pos = (OVERPOS[0] + 10 + OVERLAX, 50) #Y position of information

	for i in str_info:
		loc = str_info.index(i)

		x = i + str(data_info[loc])
		font_data = fontObj.render(x,True,WHITE)

		if i == "Player":
			ppos = list(pos)
			ppos[0] += font_data.get_width() + 10
			ploc = loc
		elif i == "Bomb":
			bpos = list(pos)
			bpos[0] += font_data.get_width() + 10
			bloc = loc

		new_info.append(font_data)

	for i in new_info:
		screen.blit(i,pos)
		if new_info.index(i) == ploc:
			ppos[1] = pos[1]
		elif new_info.index(i) == bloc:
			bpos[1] = pos[1]

		pos = (pos[0],pos[1]+new_info[1].get_height() + 10)

	x = "POWER: " + str(players[current_playr].getPower())
	i = fontObj.render(x,True,WHITE)
	screen.blit(i,pos)

	symbol(players[current_playr].life,LIFE_IMG,ppos,screen)
	symbol(players[current_playr].bombs,BOMB_IMG,bpos,screen)

def spriteWallCollide(sprite):
	'''Reverse sprite speed if it collides with the wall.'''

	posx = sprite.rect.x
	posy = sprite.rect.y

	speed = sprite.speed

	if posx <= 0:
		speed[0] *= -1
	if posx >= (OVERLAX-sprite.image.get_width()): 
		speed[0] *= -1
	if posy >= (OVERLAY-sprite.image.get_width()):
		speed[1] *= -1
	if posy <= 0:
		speed[1] *= -1

	return speed

def runIdle(sprites={}):
	'''{sprite:[args]}'''
	for sprite in sprites:
		args = sprites[sprite]
		sprite.idle(*args)

def pointOnSquare(center,deg,radius=1):
	x = center[0]
	y = center[1]

	cos = math.cos(math.radians(deg))
	sin = math.sin(math.radians(deg))

	x2 = (radius*cos)+x
	y2 = (radius*sin)+y

	return [x2,y2]

def pointOnCircle(deg,center):
	x = math.sin(math.radians(deg))
	y = math.cos(math.radians(deg))

	return [x,y]

def pointsOnCircle(amount,center,degShift=1):
	points = []

	degs = [(360/amount)*i for i in range(amount)]

	for d in degs:
		points.append(pointOnCircle(d*degShift,center))

	return points

def newSpeed(start, end):
	dx = float(start[0]) - float(end[0])
	dy = float(start[1]) - float(end[1])

	return [dx, dy]

def verify_files():
	master_url = getSetting('MASTER_URL')
	logging("Downloading file list...","std")
	print master_url + "MANIFEST.MF"
	files = urllib2.urlopen(master_url + "MANIFEST.MF").read()
	logging("Writing file list to MANIFEST.MF...","std")
	open("MANIFEST.MF","w").write(files)

	files = files.split("\n")

	for i in files:
		index = files.index(i)
		files[index] = os.path.join(os.getcwd(),i)

	for path,name,filename in os.walk(os.getcwd()):
		if os.path.join(os.getcwd(),filename) in files:
			files.remove(filename)

	logging("Writing ")
	for f in files:
		url = master_url + f.split(os.getcwd())[1]
		print url
		data = urllib.urlopen(url).read()
		open(f,'wb').write(data)

	print files

nuclear = u'\u2622'
