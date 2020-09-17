import pygame
import random
import time
import numpy as np
import sys

class Edible:

	
	def __init__(self, dna, tilesArr=None, myTile=None):

		iterator = 0
		if type(tilesArr) != type(None):

			while True:

				randIdxX = random.randint(0, tilesArr.shape[0] -1)
				randIdxY = random.randint(0, tilesArr.shape[1] -1)

				

				if tilesArr[randIdxX][randIdxY].withPlant == False:

					tilesArr[randIdxX][randIdxY].withPlant = True
					break

				if iterator > 1000:

					print("Error, you've requested too much plants they dont fit in the world!")
					sys.exit()

				iterator += 1
			

			self.myTile = tilesArr[randIdxX][randIdxY]

		else:

			
			self.myTile = myTile
			self.myTile.withPlant = True
			
			
		self.dna = dna

		self.size = 1

		self.xpos = ((self.myTile.posx + self.myTile.size//2) -self.size/2) 
		self.ypos = ((self.myTile.posy + self.myTile.size //2) - self.size/2) 

		self.growthTime = 0
		self.dying = False

	def growth(self, fps, plantDivision):

		tick = 5

		avrgUsage = self.dna.allel[1]
		growthUsage = self.dna.allel[2]

		sunUsage = self.dna.allel[3]

		self.xpos = ((self.myTile.posx + self.myTile.size//2) -self.size/2) 
		self.ypos = ((self.myTile.posy + self.myTile.size //2) - self.size/2) 

		self.energy = self.myTile.sunlight + self.myTile.wettness

		if self.growthTime >= (tick*fps)//plantDivision:

			self.growthTime = 0

			if self.myTile.wettness >= avrgUsage:

				self.myTile.wettness = self.myTile.wettness - avrgUsage
				self.dying = False

				if self.size <= self.dna.allel[0] - 165 / self.energy and self.myTile.wettness >= growthUsage and self.myTile.sunlight >= sunUsage:

					self.myTile.wettness = self.myTile.wettness - growthUsage
					self.myTile.sunlight = self.myTile.sunlight - sunUsage
					self.size += 165 / self.energy



			else:

				if self.dying == True:

					self.myTile.withPlant = False
					self.myTile.myPlant = None

					return True

				elif self.dying == False:

					self.dying = True
						
					

		self.growthTime += 1

	def birth(self, tilesArr):

		tileSpread = 8
		self.energy = self.myTile.sunlight + self.myTile.wettness

		if self.size >= self.dna.allel[0] - self.dna.allel[0]/5:

			iteratorI = 0

			if self.energy > 80 and self.myTile.wettness > self.dna.allel[0]:

				while iteratorI < tileSpread * 2:

					iteratorI +=1

					xIdxPlant = self.myTile.indexX + random.randint(-tileSpread, tileSpread)
					yIdxPlant = self.myTile.indexY + random.randint(-tileSpread, tileSpread)

					if 0 <= xIdxPlant < tilesArr.shape[0] and 0 <= yIdxPlant < tilesArr.shape[1]:

						if tilesArr[xIdxPlant][yIdxPlant].withPlant == False:

								self.myTile.wettness -= self.dna.allel[0]
								return ((xIdxPlant, yIdxPlant ), self.dna)
								break




class DNA:

	def plant_dna_creation(self, parentDna=None):

		size = 4
		if parentDna == None:
			
			self.allel = [random.randint(10, 15) for element in range(size)]

		else:

			self.allel = [ x + random.randint(-1, 1) for x in parentDna.allel if x > 1]




if __name__ == "__main__":

	dna = DNA()
	dna.plant_dna_creation()
	print(dna.allel)