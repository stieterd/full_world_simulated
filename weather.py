import pygame
import random
import time
import numpy as np

class Sun:

	def __init__(self, WINHEIGHT, WINWIDTH):

		self.starttime = time.time()
		self.daytime = 24


	def sunshine_amount(self, daytime):

		sunlightFactor = 1/5 * -((daytime - 12)**2) + 15

		amountOfSunshine = sunlightFactor/10

		return amountOfSunshine

class Rain:

	def __init__(self, WINHEIGHT, WINWIDTH):

		 #Once a minute there should be rain
		self.isRaining = False

		self.WINWIDTH = WINWIDTH
		self.WINHEIGHT = WINHEIGHT
		
		self.rainWidth = 8
		


	def check_for_rain(self, fps, tileShapeX, tileShapeY, raintick, heaviness):


		
		#raintick = 4
		x = random.randint(1, raintick * fps)
			
		if x == 3:

			b = self.raining(tileShapeX, tileShapeY, heaviness)
			
			return b

		else:

			return None

	def raining(self, tileShapeX, tileShapeY, heaviness):

		if random.randint(0, 1) == 0: #rain goes horizontally

			beginningTiley = random.randint(tileShapeY[0], tileShapeY[1])

			heaviness1 = random.randint(0, heaviness//2)

			return [True, beginningTiley, heaviness1]

		else:						  #rain goes vertically
			
			beginningTilex = random.randint(tileShapeX[0], tileShapeX[1])
			heaviness2 = random.randint(0, heaviness//2)

			return [False, beginningTilex, heaviness2]