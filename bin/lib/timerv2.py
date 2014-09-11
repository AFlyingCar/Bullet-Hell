#Tyler Robbins
#9/5/14
#Timer v2
#A new timer class, utilizing threading to replace the old one

import pygame,threading
from pygame.locals import *
from debugger import *

BLACK = (0,0,0)
WHITE = (255,255,255)

class Timer(object):
	def __init__(self,maxTime):
		self.timed = 0.0
		self.maxTime = maxTime
		self.timing = False
		self.finished = False
		self.lastTime = 0.0
		self.ctime = pygame.time.get_ticks()
		self.time_thread = threading.Thread(target = self._timer)
		self.time_thread.daemon = True
		self.time_thread.start()
		
	def _timer(self):
		'''Count time'''
		while True:
			self.ctime = pygame.time.get_ticks()

			if self.timing:
				#Count time
				if self.ctime-self.lastTime >= 1:
					self.timed += 1
					self.lastTime = self.ctime

				#Check if time is up
				if self.timed >= self.maxTime:
					self.finished = True

	def startTimer(self,reset=True):
		'''Begin running the timer'''
		if reset: self.reset()
		self.timing = True

	def reset(self):
		'''Reset and end the timer'''
		self.timed = 0
		self.timing = False
		self.ctime = pygame.time.get_ticks()

	def dispTime(self,pos,surf,font,color=BLACK,cutoff=0,count=1):
		''' pos      <- list render position
			font     <- font to render text in
			surf     <- surface  to render to
			cutoff=0 <- integer to cut off the last cutoff numbers
			color=BLACK <- color to render text in
			count=1 <- direction to count in (eg: 1=up,0=down)
		'''
		if count: 
			s_time = str(float(self.timed)/1000)
		else:
			s_time = str(float(self.maxTime-self.timed)/1000)
			#print self.maxTime - self.timed
		if cutoff: s_time = s_time[:-cutoff]
		f_time = font.render(s_time,True,color)
		surf.blit(f_time,pos)

	def stopTimer(self):
		if self.finished:
			self.timing = False

	def setMax(self,newMax):
		self.maxTime = newMax

	def getTimePassed(self):
		return float(self.timed)

	def getTimeLeft(self):
		passed = self.maxTime - self.timed
		return float(passed)

	def isFinished(self):
		return self.finished

	def getTimeFont(self,font,color=BLACK,cutoff=0,count=0):
		if count:   time = str(self.getTime()/1000)
		else:       time = str(self.getTimePassed()/1000)

		if cutoff: 	time = time[:-cutoff]

		return font.render(time,True,color)

	def pauseTimer(self):
		self.timing = False
		self.pause = True

	def forceStop(self):
		if self.timing:
			self.finished = True
			self.reset()
			logging("Forcing timer to stop!","warn")

if __name__ == "__main__":
	import sys

	def shutdown():
		pygame.quit()
		sys.exit()

	pygame.init()
	display = pygame.display.set_mode((640,480))
	pygame.display.set_caption("timer")

	display.fill(WHITE)
	fontObj = pygame.font.Font('freesansbold.ttf',29)

	myTimer = Timer(30000)
	myTimer.startTimer()
	
	fps = pygame.time.Clock()

	pos = [0,0]

	while True:
		display.fill(WHITE)

		for event in pygame.event.get():
			if event.type == QUIT:
				shutdown()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					shutdown()

				if event.key == K_DOWN:   pos[1] += 1
				if event.key == K_UP:     pos[1] -= 1
				if event.key == K_LEFT:   pos[0] -= 1
				if event.key == K_RIGHT:  pos[0] += 1

		myTimer.dispTime((0,0),fontObj,display,cutoff=1)
		myTimer.dispTime((640/2,480/2),fontObj,display,cutoff=1,count=0)
		myTimer.stopTimer()

		pygame.draw.circle(display,BLACK,pos,5)

		fps.tick(60)
		pygame.display.update()
