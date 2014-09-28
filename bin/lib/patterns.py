# Tyler Robbins
# 7/21/14
# Patterns
# Define basic bullet patterns

from sprites import *
from constants import *
from bullets import *
from basic import *
import math

def circleSpawn(spawnpos,amount,speed,newBullet,playerb=False):
	'''Spawn a newBullet in an evenly spaced circular, radiating pattern whose speed is the list speed.'''
	bulls = []
	for b in range(amount):
		deg = 360*((1.0/amount)*(b+1))

		nextLoc =       pointOnCircle(spawnpos,deg)
		direction =     newSpeed(spawnpos,nextLoc)

		for i in direction:
			index = direction.index(i)
			direction[index] *= speed

		bulls.append(newBullet(spawnpos,direction,playerb))

		# print bulls

	return bulls

def aimedShotSpawn(spawnpos,pos,speed,newBullet,playerb=False):
	'''Shoot a shot specifically aimed at the list pos'''
	direction = newSpeed(spawnPos,pos)
	direction[0] = (direction[0]/math.fabs(direction[0]))*speed
	direction[1] = (direction[1]/math.fabs(direction[1]))*speed

	b = newBullet(spawnpos,direction,playerb)
	return b

nuclear = u'\u2622'
