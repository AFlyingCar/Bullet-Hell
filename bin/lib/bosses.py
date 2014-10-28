# Tyler Robbins
# 10/4/14
# Bosses
# Store all bosses

from sprites import *
from spellcards import *
from dependencies import *

class VivianJames(boss):
	def __init__(self,num,life,lives):
		boss.__init__(self,num,BOSS11_IMG,"th00_02.ogg",life=life,lives=lives)
		self.speed = [0,0]

		spell1 = LargeEX(self,self.bulletGroup)

		self.spells.append(spell1)

	def uponDeath(self):
		if self.isDead:
			self.timesRun += 1
			for b in self.bulletGroup.sprites():
				b.kill()

			self.rect.x = overlay.get_width()+10
			self.rect.y = overlay.get_height()+10

			x =    FONT_THSPATIAL.render('YOU WIN!',True,BLACK)
			pos =  surf_center(overlay,x)

			overlay.blit(x,pos)

			if self.timesRun <= 1:
				stopMusic()

			if not isPlaying():
				mus = getSetting('enable_music')
				if mus: playMusic("th00_03.ogg")

			self.endBossFight()
