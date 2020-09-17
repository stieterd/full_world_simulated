import pygame
import random
import time
import numpy as np

class Tile:

	def __init__(self, posx, posy, size, index):

		self.posx = posx
		self.posy = posy
		self.size = size
		self.indexY = index[0]
		self.indexX = index[1]

		self.withPlant = False
		self.myPlant = None

		self.sunlight = 0 #max 165
		self.wettness = 0 #max 165

	def tile_statistics(self):

		if self.withPlant == False:

			myTileStats = [(self.withPlant, "Tile has plant: "), (int(self.sunlight), "Tile sunlight: "), (int(self.wettness), "Tile rain: ")]
		else:

			myTileStats = [(self.withPlant, "Tile has plant: "), (int(self.sunlight), "Tile sunlight: "), (int(self.wettness), "Tile rain: "), (int(self.myPlant.size), "Tile plantsize: "), (int(self.myPlant.dna.allel[0]), "Tile plantMaxSize: ")]

		return myTileStats