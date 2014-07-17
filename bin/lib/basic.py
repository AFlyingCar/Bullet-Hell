#Tyler Robbins
#7/13/14
#Basic
#Contains basic loading functions

import pygame,os,sys
from pygame.locals import *
from color import *

######Load images from ./Images and return a blank Surface if the image couldn't be found
def loadImage(filename):
	loc = os.path.join(os.getcwd(),"Images",filename)

	if os.path.exists(loc):
		pic = pygame.image.load(loc)
		return pic

	else:
		print "ImageError: Could not find", filename, "in \\Images!"
		print "Loading blank image..."

		pic = pygame.Surface((10,10))
		return pic

######Load sounds from ./Sound and return an error if the file was not found,
###### or if pygame.mixer was not initialized
def loadSound(filename):
	path = os.path.join(os.getcwd(),"Sound",filename)

	if os.path.exists(path):
		if pygame.mixer.get_init():
			s = pygame.mixer.Sound(path)
			return s

		else:
			print "Mixer not initialized!"

			while True:
				yn = raw_input("Initialize?(y/n) ")
				if yn is 'y':
					pygame.mixer.init()
					break
				elif yn is 'n':
					print "Warning: Mixer still not initialized!"
					print "This could result in the program failing."
					break
				else:
					print "'y' or 'n' please!"

	else:
		print "SoundError: Could not find", filename, "in \\Sound!"
		return "err"

def playSound(filename):
	if type(filename) is pygame.mixer.Sound:
		filename.play()

	elif type(filename) is str:
		s = loadSound(filename)

		if s == "err":
			print "An error occurred!"

		elif type(s) is pygame.mixer.Sound:
			s.play()

		else:
			print type(s)
			print "Error: Generic Error"

	else:
		print "TypeError:", type(filename), "is not valid."

def loadMusic(filename):
	path = os.path.join(os.getcwd(),"Music",filename)

	if pygame.mixer.music.get_busy():
		pygame.mixer.music.fadeout(2)

	if os.path.exists(path):
		if pygame.mixer.get_init():
			pygame.mixer.music.load(path)
			return True
		else:
			print "Mixer not initialized!"
	else:
		print "Path:", path, "does not exist!"

def playMusic(filename):
	s = loadMusic(filename)

	if s:
		pygame.mixer.music.play(-1)
	else:
		print "ERROR"

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

def shutdown():
	pygame.quit()
	sys.exit()

def surf_center(surface,newSurface):
	x = (surface.get_width()/2) - (newSurface.get_width()/2)
	y = (surface.get_height()/2) - (newSurface.get_height()/2)

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

def dispText(text,surf,pos,color=BLACK):
	f = fontObj.render(text,True,color)
	surf.blit(f,pos)

nuclear = u'\u2622'