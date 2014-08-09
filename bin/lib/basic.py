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
def loadImage(filename):
	if type(filename) == pygame.Surface:
		return filename

	else:
		# loc = os.path.join(os.getcwd(),"Images",filename)
		loc = os.path.join(getSetting('path_image'),filename)

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

			pic = pygame.Surface((10,10))
			return pic

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

def offscreen(group,maxSize):
	#For bullets only
	OVERLAX = maxSize[0]
	OVERLAY = maxSize[1]

	for b in group.sprites():
		delete = False

		if b.rect.x <= (0-b.image.get_width()):
			for g in b.groups():
				g.remove(b)
			delete = True

		if b.rect.x >= OVERLAX:
			for g in b.groups():
				g.remove(b)
			delete = True

		if b.rect.y >= OVERLAY:
			for g in b.groups():
				g.remove(b)
			delete = True

		if b.rect.y <= (0-b.image.get_height()):
			for g in b.groups():
				g.remove(b)
			delete = True

		if delete: del b

def clear_b(group):
	for x in group.sprites():
		for g in x.groups():
			g.remove(x)
	group.empty()

	logging("Clearing screen...","std")

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
	print "Shutting down pygame..."
	pygame.quit()
	logging("Pygame has shut down successfully!", "std")
	print "Pygame has shut down successfully!"

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

	ipos = img.get_width() + 5

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