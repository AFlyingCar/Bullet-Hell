#Tyler Robbins
#7/13/14
#Basic
#Contains basic loading functions

import pygame,os,sys
from pygame.locals import *
from globalVar import *
from debugger import *
from settings import *
from color import *

s_init_check = False # <- Whether to check for an initialized mixer

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
def loadSound(filename):
	# path = os.path.join(os.getcwd(),"Sound",filename)
	path = os.path.join(getSetting('path_sound'),filename)

	if os.path.exists(path):
		if pygame.mixer.get_init():
			s = pygame.mixer.Sound(path)
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

def playSound(filename):
	if getSetting('enable_sound'):
		if pygame.mixer.get_init():
			if type(filename) is pygame.mixer.Sound:
				filename.play()

			elif type(filename) is str:
				s = loadSound(filename)

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

def loadMusic(filename):
	# path = os.path.join(os.getcwd(),"Music",filename)
	path = os.path.join(getSetting("path_music"),filename)

	if pygame.mixer.music.get_busy():
		pygame.mixer.music.fadeout(2)

	if os.path.exists(path):
		if pygame.mixer.get_init():
			pygame.mixer.music.load(path)
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

def playMusic(filename):
	s = loadMusic(filename)

	if s:
		pygame.mixer.music.play(-1)
	else:
		# print "ERROR"
		pass

def stopMusic():
	'''Will stop all music from playing.'''
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

#This old timer is no longer being used, but will be left here until it has been completely deprecated
class TimerOLD(object):
	def __init__(self,maxTime):
		"""Timer class that returns True when finished
		maxTime = time in milliseconds before ending
		"""
		self.clock = pygame.time.Clock()

		self.maxTime = 	maxTime
		self.timing = 	False
		self.pause = 	False
		self.lastTime = 0
		self.timed = 	0
		self.finished = False

	def startTimer(self):
		if not self.pause:
			self.reset()

		self.timing = 	True
		self.pause = 	False
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

	def dispTime(self,pos,surf,font,color=BLACK,cutoff=0,count=1):
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
		self.timing = 	False
		self.timed = 	0
		self.finished = False
		self.pause = 	False
		self.lastTime = pygame.time.get_ticks()
		print "RESET"

	def getTime(self):
		return self.timed

	def getTimePassed(self):
		passed = self.maxTime - self.timed
		return passed

	def isFinished(self):
		return self.finished

	def pauseTimer(self):
		self.timing = False
		self.pause = True

nuclear = u'\u2622'