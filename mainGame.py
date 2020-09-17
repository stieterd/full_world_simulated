#-----------IMPORTING INTERNAL LIBRARIES-----------#
import players
import edibles
import tiles
import others
import weather
#-----------IMPORTING EXTERNAL LIBRARIES-----------#
import pygame
import random
import time
import numpy as np

pygame.init()


#-----------CONSTANTS FOR THE WINDOW AND THE GAME-----------#


FPS = 200 

class Win:

	BORDER = (-10000, 10000)

	WINSPECS = [(1280,720),(1920, 1080)]

	
	

	CLOCK = pygame.time.Clock()

	

	def __init__(self, biomenames, nPlants = 3000):

		self.pauseButtons = [
		[[True, False],"Press here to exit the application.", "exitApp"], 
		[[self.WINSPECS, 0],"Your current resolution:", "resChanger"], 
		[[[x[0] for x in biomenames], 0],"Teleport to biome:", "biomeTp"]
		]
		
		self.GAMEISRUNNING = self.get_pause_button_item("exitApp", "mainVar")

		self.windowResolutionIdx = self.get_pause_button_item("resChanger", "varChanger")

		#self.SCREEN = pygame.display.set_mode((self.WINSPECS[self.windowResolutionIdx][0], self.WINSPECS[self.windowResolutionIdx][1]), pygame.FULLSCREEN, )
		self.SCREEN = pygame.display.set_mode((self.WINSPECS[self.windowResolutionIdx][0], self.WINSPECS[self.windowResolutionIdx][1]), )
		self.DISPLAY = pygame.Rect(0,0,self.WINSPECS[self.windowResolutionIdx][0], self.WINSPECS[self.windowResolutionIdx][1])

		#-----------WINDOW MOVEMENT PROPERTIES-----------#
		self.winPosX = 0
		self.winPosY = 0
		self.zoom = 1.0

		self.showTile = False

		#-----------WEATHER MECHANICS-----------#

		self.rain = weather.Rain(self.WINSPECS[self.windowResolutionIdx][1], self.WINSPECS[self.windowResolutionIdx][0])
		self.sun = weather.Sun(self.WINSPECS[self.windowResolutionIdx][1],self.WINSPECS[self.windowResolutionIdx][0])
		self.fastestRaintick = 2.5

		#-----------OTHER GAME MECHANICS-----------#

		self.showMenu = True
		


		self.dayTime = 0
		self.daysPassed = 0

		self.debug = []

		#-----------PAUSE MENU-----------#
		self.pause = False

		self.pauseMenuOffsetWidth = 200
		self.pauseMenuOffsetHeight = 100

		
		
		#-----------CONFIGURING PLANTS-----------#
		
		self.plantsArr = np.zeros(nPlants, dtype=object)
		self.plantIterator = 0
		self.plantDivision = 10

		#-----------CONFIGURING TILES-----------#
		self.tileSize = 100
		nTiles = (self.BORDER[1] - self.BORDER[0]) // self.tileSize
		self.tilesArr = np.zeros((nTiles,nTiles), dtype=object)

		self.viewTileOffsetX = 0
		self.viewTileOffsetY = 0

		#-----------BIOMES-----------#

		self.biomeNames = biomenames
		self.currentBiome = self.biomeNames[5]

		self.change_pause_button_var("biomeTp", "varChanger", self.biomeNames.index(self.currentBiome))
		self.pauseBiomeNames = self.get_pause_button_item("biomeTp", "mainVar")
		

		self.biomeWettnessIterator = 0
		self.biomeSunlightIterator = 0
		self.biomeTime = 0

	def start_game(self):



		#-----------PUTTING TILES IN ARRAY BEFORE GAME LOOP-----------#	
		
		self.tile_array_placement()

				
		#-----------GENERATING BIOMES BEFORE GAME LOOP-----------#
		
		self.biome_generation(len(self.biomeNames))
		
		#-----------PLACE PLANTS IN ARRAY BEFORE GAME LOOP-----------#


		for idx in range(self.plantsArr.shape[0]):

			plantDna = edibles.DNA()
			plantDna.plant_dna_creation()
			self.plantsArr[idx] = edibles.Edible(plantDna,tilesArr=self.tilesArr)
			self.plantsArr[idx].myTile.myPlant = self.plantsArr[idx]
		
		#-----------STARTING CHECKPOINT FOR DELTATIME-----------#

		timeCheckpoint = time.time()

		#-----------DEFINING OLD RESOLUTION IDX-----------#
		windowOldResolutionIdx = self.windowResolutionIdx

		#-----------CONFIGURING ALL PAUSE BUTTONS-----------#
		
		changedBiomeIdxOld = self.get_pause_button_item("biomeTp", "varChanger")

		

		#-----------MAIN GAME LOOP-----------#
		while self.GAMEISRUNNING:

			#-----------DEFINING PAUSEMENU VARS-----------#
			self.GAMEISRUNNING = self.get_pause_button_item("exitApp", "mainVar")
			self.windowResolutionIdx = self.get_pause_button_item("resChanger", "varChanger")

			self.pauseWindow = pygame.Rect(self.pauseMenuOffsetWidth//2, self.pauseMenuOffsetHeight//2, self.WINSPECS[self.windowResolutionIdx][0]-self.pauseMenuOffsetWidth, self.WINSPECS[self.windowResolutionIdx][1]-self.pauseMenuOffsetHeight )
			#self.pauseWindow = pygame.Rect(self.pauseMenuOffsetWidth//2, self.pauseMenuOffsetHeight//2, self.WINSPECS[0][0]-self.pauseMenuOffsetWidth, self.WINSPECS[0][1]-self.pauseMenuOffsetHeight )

			#-----------CHECKING IF TELEPORTING TO BIOME-----------#
			if self.get_pause_button_item("biomeTp", "varChanger") != changedBiomeIdxOld:

				myBiome = self.biomes[self.get_pause_button_item("biomeTp", "varChanger")]
				teleportTile = self.tilesArr[myBiome[0][0]][myBiome[1][0]]

				self.currentBiome = self.biomeNames[self.get_pause_button_item("biomeTp", "varChanger")]
				
				self.winPosX = -teleportTile.posx
				self.winPosY = -teleportTile.posy 

			#-----------CHECKING IF HAVING TO CHANGE RESOLUTION SCREEN-----------#
			if windowOldResolutionIdx != self.windowResolutionIdx:

				
				self.SCREEN = pygame.display.set_mode((self.WINSPECS[self.windowResolutionIdx][0], self.WINSPECS[self.windowResolutionIdx][1]), pygame.FULLSCREEN)
				self.DISPLAY = pygame.Rect(0,0,self.WINSPECS[self.windowResolutionIdx][0], self.WINSPECS[self.windowResolutionIdx][1])
				print(self.DISPLAY)
				screenLst = []

				self.winPosX = 0
				self.winPosY = 0

				self.tile_array_placement(newTiles=False)


			windowOldResolutionIdx = self.windowResolutionIdx
			#-----------CONFIGURING DELTATIME-----------#

			self.deltaTime = time.time() - timeCheckpoint
			timeCheckpoint = time.time()

			

			#-----------IF IS PAUSED-----------#
			if self.pause:

				changedBiomeIdxOld = self.biomeNames.index(self.currentBiome)
				self.change_pause_button_var("biomeTp", "varChanger", changedBiomeIdxOld)


				self.pause_window()



			#-----------IF IS NOT PAUSED-----------#
			else:
				

				#-----------KEYS/BUTTON PROPERTIES-----------#
				for event in pygame.event.get():

					if event.type == pygame.QUIT:

						self.GAMEISRUNNING = False

					if event.type == pygame.KEYDOWN:

							if event.key == pygame.K_ESCAPE:

								self.pause = not self.pause

							if event.key == pygame.K_m:
								
								self.showMenu = not self.showMenu

							if event.key == pygame.K_e and self.showTile == True:

								self.planting_edible()




					if event.type == pygame.MOUSEBUTTONDOWN:

						if event.button == 1:
							self.showTile = not self.showTile

				self.mousePos = pygame.mouse.get_pos()

				self.keys = pygame.key.get_pressed()

				#-----------GETTING FRAMES PER SECOND-----------#
				self.fps = int(self.CLOCK.get_fps())
				
				
				#-----------FUNCTION THAT MOVES THE WINDOW-----------#
				self.change_win_pos()

				#-----------CONFIGURING FPS FOR THE GAME-----------#
				self.CLOCK.tick(FPS)

				#-----------START OF DRAWING OBJECTS ON SCREEN-----------#
				self.SCREEN.fill(others.Colors.white)

				#-----------CONFIGURATION OF TILES IN GAME LOOP-----------#
				self.changing_on_screen_tiles()
				self.draw_tiles_on_screen()
				
				

				#-----------DRAWING PLANTS ON THE SCREEN-----------#
				
				plantsToBeKilled = []
				plantsBirth = []

				for idx in range(int(self.plantsArr.shape[0]/self.plantDivision * self.plantIterator), int(self.plantsArr.shape[0]/self.plantDivision * (self.plantIterator+1))):

					kill = self.plantsArr[idx].growth(FPS, self.plantDivision)

					birth = self.plantsArr[idx].birth(self.tilesArr)

					if kill != None:

						plantsToBeKilled.append(idx)

					else:

						

						if birth != None:

							#print("yoooo")
							

							plantsBirth.append(birth)

						

				plantsToBeKilled.sort()
				
				if plantsToBeKilled != []:

					self.plantsArr = np.delete(self.plantsArr, plantsToBeKilled)
				
				if plantsBirth != []:

					#print("yeaaaaa!!")
					oldPlantsArr = self.plantsArr
					self.plantsArr = np.append([oldPlantsArr], np.zeros(len(plantsBirth), dtype=object))

					plantsBirthIterator = 0

					for idx in range(oldPlantsArr.shape[0], self.plantsArr.shape[0]):
					

						birth = plantsBirth[plantsBirthIterator]
						

						myPlantDna = edibles.DNA()
						myPlantDna.plant_dna_creation(parentDna=birth[1])
						#print("birth 1: ", birth[1])
						self.plantsArr[idx] = edibles.Edible(myPlantDna, myTile=self.tilesArr[birth[0][0]][birth[0][1]])
						self.plantsArr[idx].myTile.myPlant = self.plantsArr[idx]
						self.debug.append(self.tilesArr[birth[0][0]][birth[0][1]])
						
						self.plantsArr[idx].myTile.myPlant = self.plantsArr[idx]

						plantsBirthIterator += 1

					'''
					if birth != None:

						#print("yoooo")

						oldPlantsArr = self.plantsArr
						self.plantsArr = np.zeros(oldPlantsArr.shape[0]+1,dtype=object)
						for idx in range(oldPlantsArr.shape[0]):

							self.plantsArr[idx] = oldPlantsArr[idx]

						myPlantDna = edibles.DNA()
						myPlantDna.getting_dna_parents(birth[1])
						self.plantsArr[-1] = edibles.Edible(myPlantDna, myTile=self.tilesArr[birth[0][0]][birth[0][1]])
						self.plantsArr[-1].myTile.myPlant = self.plantsArr[-1]

						oldPlantsArr = None
					'''

				
				self.plantIterator += 1

				if self.plantIterator >= self.plantDivision:

					self.plantIterator = 0
				
				#-----------BIOMES-----------#
				
				self.draw_biome_border()

				self.biomeTime += self.deltaTime

				self.biome_sunlight()

				if self.biomeTime > 10/len(biomenames):

					self.biome_wettness_usage()

				
				
				#-----------GETTING WEATHER INFO-----------#

				

				if self.dayTime >= 24:

					self.dayTime = 0
					self.daysPassed += 1

				self.dayTime += self.deltaTime
				

				for mainIdx in range(self.biomes.shape[0]):

					

					firstXtile = self.biomes[mainIdx][0][0]
					lastXtile = self.biomes[mainIdx][0][1]

					firstYtile = self.biomes[mainIdx][1][0]
					lastYtile = self.biomes[mainIdx][1][1]

					raining = self.rain.check_for_rain(FPS, (firstXtile, lastXtile) , (firstYtile, lastYtile), int(self.fastestRaintick), self.biomeNames[mainIdx][1][1] )



					if raining != None:

						if raining[0]:

							maxHeight = raining[1] + self.rain.rainWidth
							minHeight = raining[1] - self.rain.rainWidth

							if maxHeight > lastYtile:

								maxHeight = lastYtile

							elif minHeight < firstYtile:

								minHeight = firstYtile


							for idx in range(firstXtile, lastXtile):

								for x in range(minHeight, maxHeight):

									
									self.tilesArr[idx][x].wettness += raining[2]
									if self.tilesArr[idx][x].wettness > 165:

										self.tilesArr[idx][x].wettness = 165

						else:

							maxWidth = raining[1] + self.rain.rainWidth
							minWidth = raining[1] - self.rain.rainWidth

							if maxWidth > lastXtile:

								maxWidth = lastXtile

							elif minWidth < firstXtile:

								minWidth = firstXtile
							
							for idx in range(minWidth, maxWidth):

								for x in range(firstYtile, lastYtile):

									
									self.tilesArr[idx][x].wettness += raining[2]
									if self.tilesArr[idx][x].wettness > 165:

										self.tilesArr[idx][x].wettness = 165

				#-----------DRAWING SELECTED TILE ON THE SCREEN-----------#					
				if self.showTile:

					self.draw_obj(others.Colors.white, self.selectedTile.posx, self.selectedTile.posy, self.tileSize, self.tileSize, width=7)
				

				#-----------DRAWING TEXT ON THE SCREEN-----------#
				self.draw_statistics_text()
				self.drawing_tile_menu()
				

				
				pygame.display.update(self.DISPLAY)


			

	def change_win_pos(self):

		moveSpeed = 1000 #movementspeed 10 is best



		#-----------MOVE THE WINDOW-----------#

		if self.keys[pygame.K_LEFT] and self.winPosX < self.BORDER[1] :

			self.winPosX += int(moveSpeed * self.deltaTime)

		if self.keys[pygame.K_RIGHT] and self.winPosX > self.BORDER[0] + self.WINSPECS[self.windowResolutionIdx][0]:

			self.winPosX -= int(moveSpeed * self.deltaTime)

		if self.keys[pygame.K_DOWN] and self.winPosY > self.BORDER[0] + self.WINSPECS[self.windowResolutionIdx][1]:

			self.winPosY -= int(moveSpeed * self.deltaTime)

		if self.keys[pygame.K_UP] and self.winPosY < self.BORDER[1]:

			self.winPosY += int(moveSpeed * self.deltaTime)

		if self.keys[pygame.K_o]:

			self.winPosY = 0
			self.winPosX = 0


		self.viewTileOffsetX = self.winPosX // self.tileSize
		self.viewTileOffsetY = self.winPosY // self.tileSize	

	def pause_window(self):

		mouseIsClicked = False

		#-----------KEYS/BUTTON PROPERTIES-----------#
		for event in pygame.event.get():

			if event.type == pygame.QUIT:

				self.GAMEISRUNNING = False

			if event.type == pygame.KEYDOWN:

					if event.key == pygame.K_ESCAPE:

						self.pause = not self.pause

			if event.type == pygame.MOUSEBUTTONDOWN:

						if event.button == 1:
							mouseIsClicked = True

		self.mousePos = pygame.mouse.get_pos()

		#-----------DRAWING MAINWINDOW-----------#
		pygame.draw.rect(self.SCREEN, (150,150,150), self.pauseWindow)

		width = 4
		pygame.draw.rect(self.SCREEN, others.Colors.black, (self.pauseMenuOffsetWidth//2, self.pauseMenuOffsetHeight//2, self.WINSPECS[self.windowResolutionIdx][0]-self.pauseMenuOffsetWidth - width//2, self.WINSPECS[self.windowResolutionIdx][1]-self.pauseMenuOffsetHeight - width//2), width)

		#-----------BUTTON CONFIG-----------#
		buttonsPositionX = 80
		buttonsStartingPositionY = 140
		buttonsWidth = 100
		buttonsHeight = 40
		buttonsSelectedOutlineWidth = 2
		buttonsPadding = 80

		#-----------BUTTONTEXT CONFIG-----------#
		textToButtonPadding = 120
		myFont = pygame.font.Font(None, 30)

		#-----------BUTTON ITERATION-----------#
		for idx, button in enumerate(self.pauseButtons):
			
			myButtonYpos = self.pauseMenuOffsetHeight//2 + buttonsStartingPositionY + buttonsPadding * idx

			myButton = pygame.draw.rect(self.SCREEN, others.Colors.darkred, (self.pauseMenuOffsetWidth//2 + buttonsPositionX, myButtonYpos, buttonsWidth, buttonsHeight))
			
			if type(button[0][0]) != list:

				text = myFont.render((button[1]), True, others.Colors.black)

			else:

				text = myFont.render(f"{button[1]} {(button[0][0][button[0][1]])}", True, others.Colors.black)

			self.SCREEN.blit(text, (self.pauseMenuOffsetWidth//2 + buttonsPositionX + textToButtonPadding, myButtonYpos + 10))

			if myButton.collidepoint(self.mousePos):
				
				
				myButtonOutline = pygame.draw.rect(self.SCREEN, others.Colors.white, (self.pauseMenuOffsetWidth//2 + buttonsPositionX, myButtonYpos, buttonsWidth - buttonsSelectedOutlineWidth//2, buttonsHeight - buttonsSelectedOutlineWidth//2), buttonsSelectedOutlineWidth)
				
				
				if mouseIsClicked == True:

					if type(button[0][0]) == bool:

						button[0][0] = button[0][1]


					elif type(button[0][0]) == int:

						
						button[0][0] += button[0][1]

					elif type(button[0][0] == list):

						
						button[0][1] += 1
						if button[0][1] >= len(button[0][0]):

							button[0][1] = 0
		
		closeButtonSize = 40
		closeButtonPositionX = 60

		closeButton = pygame.draw.rect(self.SCREEN, others.Colors.darkred, ((self.WINSPECS[self.windowResolutionIdx][0] - self.pauseMenuOffsetWidth//2) - closeButtonPositionX - closeButtonSize, self.pauseMenuOffsetHeight//2 + closeButtonSize, closeButtonSize, closeButtonSize))
		
		if closeButton.collidepoint(self.mousePos):
				
				
				closeButtonOutline = pygame.draw.rect(self.SCREEN, others.Colors.white, ((self.WINSPECS[self.windowResolutionIdx][0] - self.pauseMenuOffsetWidth//2) - closeButtonPositionX - closeButtonSize, self.pauseMenuOffsetHeight//2 + closeButtonSize, closeButtonSize - buttonsSelectedOutlineWidth//2, closeButtonSize - buttonsSelectedOutlineWidth//2), buttonsSelectedOutlineWidth)
				
				
				if mouseIsClicked == True:

					self.pause = not self.pause

		#-----------WRITING PAUSE MENU ON THE SCREEN-----------#

		PauseMenuFont = pygame.font.Font(None, 70)
		text = PauseMenuFont.render(("PAUSE MENU"), True, others.Colors.black)
		self.SCREEN.blit(text, (self.pauseMenuOffsetWidth//2 + (self.WINSPECS[self.windowResolutionIdx][0] - self.pauseMenuOffsetWidth)//2 - 150, self.pauseMenuOffsetHeight//2 + 50))

		#-----------FPS AND UPDATES-----------#
		self.CLOCK.tick(FPS)

		

		pygame.display.update(self.pauseWindow)

	def get_pause_button_item(self, name, vartype):

		for pauseBut in self.pauseButtons: 

			if pauseBut[2] == name:

				if vartype == 'mainVar':

					return pauseBut[0][0]

				elif vartype == 'varChanger':

					return pauseBut[0][1]

	def change_pause_button_var(self, name, vartype, value):

		for idx in range(len(self.pauseButtons)): 

			if self.pauseButtons[idx][2] == name:

				if vartype == 'mainVar':

					self.pauseButtons[idx][0][0] = value

				elif vartype == 'varChanger':

					self.pauseButtons[idx][0][1] = value



	def draw_obj(self, color, xpos, ypos, sizex, sizey, width=0):

		pygame.draw.rect(self.SCREEN, color,(int(xpos + self.winPosX), int(ypos + self.winPosY), int(sizex), int(sizey)), width)

	def draw_biome_border(self):

		for idx,biome in enumerate(self.biomes):

			
			windowCenterIndex = self.tilesOnScreen[self.tilesOnScreen.shape[0]//2]

			firstTileBiome = self.tilesArr[biome[0][0]][biome[1][0]]
			lastTileBiome = self.tilesArr[biome[0][1]][biome[1][1]]
			oldBiomeName = self.currentBiome
			

			if firstTileBiome.posx < self.tilesArr[windowCenterIndex[0]][windowCenterIndex[1]].posx < lastTileBiome.posx and firstTileBiome.posy < self.tilesArr[windowCenterIndex[0]][windowCenterIndex[1]].posy < lastTileBiome.posy:

				self.currentBiome = self.biomeNames[idx]
				self.currentBiomeIdx = idx

				


					

			self.draw_obj(others.Colors.darkred, firstTileBiome.posx, firstTileBiome.posy, lastTileBiome.posx - firstTileBiome.posx, lastTileBiome.posy - firstTileBiome.posy,width=10)

	def draw_tiles_on_screen(self):

		for idx in range(len(self.tilesOnScreen)):


			#-----------DRAWS THE RIGHT COLORS INSIDE THE TILE-----------#
			try:
				self.draw_obj((int(self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].sunlight) + 90 -1 ,100, int(self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].wettness)+ 90 -1) , self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].posx, self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].posy, self.tileSize, self.tileSize)
				self.draw_obj(others.Colors.black, self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].posx, self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].posy, self.tileSize, self.tileSize, width=1)
			
			#-----------DRAWS PLANT ON TILE IF TILE HAS PLANT-----------#	
				if self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].withPlant == True:

					plantObj = self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].myPlant
					try:
						self.draw_obj(others.Colors.green, plantObj.xpos, plantObj.ypos, plantObj.size, plantObj.size)
					except AttributeError:

						isBirth = False
						for x in self.debug:

							if self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].myPlant == plantObj:

								isBirth = True
								print(plantObj, " because birth is true")

			#-----------DETECTS IF TILE COLLIDES WITH MOUSE AND DRAWS BLACK BOX AROUND IT-----------#
				if self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].posx + self.winPosX < self.mousePos[0] < self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].posx + self.winPosX + self.tileSize:

						if self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].posy + self.winPosY < self.mousePos[1] < self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]].posy + self.winPosY + self.tileSize:

							if self.showTile:

								self.selectedTile = self.tilesArr[self.tilesOnScreen[idx][0]][self.tilesOnScreen[idx][1]]
								
			except IndexError:
				pass
			
	def drawing_tile_menu(self):

		if self.showTile:

			font = pygame.font.Font(None, 24)

			menuColor = others.Colors.orange

			allStatistics = self.selectedTile.tile_statistics()

			startingPixels = (self.WINSPECS[self.windowResolutionIdx][0]-200, 20)

			for i in range(len(allStatistics)):

				text = font.render((f"{allStatistics[i][1]}{allStatistics[i][0]}"), True, menuColor)
				self.SCREEN.blit(text, (startingPixels[0], i * 20 + startingPixels[1]))

	def draw_statistics_text(self):

			if self.showMenu == True:

				font = pygame.font.Font(None, 24)

				menuColor = others.Colors.darkred

				
				fpsText = font.render((f"FPS: {self.fps}"), True, menuColor)
				self.SCREEN.blit(fpsText, (20, 20))

				coordinateText = font.render((f"Coordinates (X: {self.winPosX}, Y: {self.winPosY})"), True, menuColor)
				self.SCREEN.blit(coordinateText, (20, 40))

				biomeText = font.render((f"BIOME: {self.currentBiome[0]}"), True, others.Colors.yellow)
				self.SCREEN.blit(biomeText, (20, 80))

				plantsLenText = font.render((f"PLANTS ALIVE: {self.plantsArr.shape[0]}"), True, others.Colors.yellow)
				self.SCREEN.blit(plantsLenText, (20, 100))

				dayTimeText = font.render((f"TIME: {int(self.dayTime)}"), True, others.Colors.yellow)
				self.SCREEN.blit(dayTimeText, (20, 120))

				dayTimeText = font.render((f"DAY: {int(self.daysPassed)}"), True, others.Colors.yellow)
				self.SCREEN.blit(dayTimeText, (20, 140))


	
	def tile_array_placement(self, newTiles=True):

		screenLst = []

		for d1Idx in range(self.tilesArr.shape[0]):

			for d2Idx in range(self.tilesArr.shape[1]):

				tileXpos = (self.tileSize * d1Idx + self.BORDER[0])
				tileYpos = (self.tileSize * d2Idx + self.BORDER[0])

				if newTiles == True:

					self.tilesArr[d1Idx][d2Idx] = tiles.Tile(tileXpos, tileYpos, self.tileSize, [d1Idx, d2Idx])
				

				if - 2 * self.tileSize < tileXpos < self.WINSPECS[self.windowResolutionIdx][0] + self.tileSize and - 2 * self.tileSize < tileYpos < self.WINSPECS[self.windowResolutionIdx][1] + self.tileSize:

					screenLst.append((d1Idx, d2Idx))

		self.tilesOnScreen = np.zeros(len(screenLst), dtype=tuple)			
					
		for idx,x in enumerate(screenLst):

			self.tilesOnScreen[idx] = x


		self.firstTileOnScrIdxX = self.tilesOnScreen[0][0]
		self.firstTileOnScrIdxY = self.tilesOnScreen[0][1]

		self.selectedTile = self.tilesArr[0][0]	

	def biome_generation(self, nBiomes):

		# nBiomes has to be the sqrt of an integer

		divider = int(nBiomes ** 0.5)
		idxX = (self.tilesArr.shape[0]-1)//divider
		idxY = (self.tilesArr.shape[1]-1)//divider

		self.biomes = np.zeros(nBiomes, dtype=tuple)

		idx = 0
		for xIndex in range(divider):

			for yIndex in range(divider):

				offsetY = (yIndex +1) * idxY
				offsetX = (xIndex +1) * idxX
				
				if yIndex + 1 == divider:

					offsetY = self.tilesArr.shape[1] - 1

				if xIndex + 1 == divider:

					offsetX = self.tilesArr.shape[0] - 1

				self.biomes[idx] = ((xIndex * idxX, offsetX), (yIndex * idxY, offsetY))
				idx += 1

	def biome_wettness_usage(self):

		self.biomeTime = 0

		

		thisBiomeX = self.biomes[self.biomeWettnessIterator][0]
		thisBiomeY = self.biomes[self.biomeWettnessIterator][1]

		wettnessUsage = self.biomeNames[self.biomeWettnessIterator][1][0] // 10

		

		for tileXidx in range(thisBiomeX[0], thisBiomeX[1]):

			for tileYidx in range(thisBiomeY[0], thisBiomeY[1]):

				myTile = self.tilesArr[tileXidx][tileYidx]

				

				if myTile.wettness >= wettnessUsage and myTile.sunlight >= 30:

					myTile.wettness -= wettnessUsage



		self.biomeWettnessIterator += 1

		if self.biomeWettnessIterator >= self.biomes.shape[0]:

			self.biomeWettnessIterator = 0

	def biome_sunlight(self):

		

		sunshineFactor = self.sun.sunshine_amount(self.dayTime)

		if sunshineFactor < 0:
			
			sunshineFactor = 0
		
		
		thisBiomeX = self.biomes[self.biomeSunlightIterator][0]
		thisBiomeY = self.biomes[self.biomeSunlightIterator][1]

		for tileXidx in range(thisBiomeX[0], thisBiomeX[1]):

			for tileYidx in range(thisBiomeY[0], thisBiomeY[1]):

				myTile = self.tilesArr[tileXidx][tileYidx]

				myTile.sunlight = self.biomeNames[self.biomeSunlightIterator][1][0] * sunshineFactor
				
				if myTile.sunlight == 0:
					myTile.sunlight = 1
				
		self.biomeSunlightIterator += 1

		if self.biomeSunlightIterator >= self.biomes.shape[0]:

			self.biomeSunlightIterator = 0

	def changing_on_screen_tiles(self):

		differenceX = self.firstTileOnScrIdxX - (self.tilesOnScreen[0][0] + self.viewTileOffsetX)
		differenceY = self.firstTileOnScrIdxY - (self.tilesOnScreen[0][1] + self.viewTileOffsetY)
		

		if differenceX != 0 or differenceY != 0:

			for idx in range(len(self.tilesOnScreen)):

				indexes = (self.tilesOnScreen[idx][0], self.tilesOnScreen[idx][1])
				self.tilesOnScreen[idx] = (indexes[0] + differenceX, indexes[1] + differenceY)

	def planting_edible(self):

		if self.selectedTile.withPlant == False:

			oldPlantsArr = self.plantsArr
			self.plantsArr = np.zeros(oldPlantsArr.shape[0]+1,dtype=object)
			for idx in range(oldPlantsArr.shape[0]):

				self.plantsArr[idx] = oldPlantsArr[idx]

			plantDna = edibles.DNA()
			plantDna.plant_dna_creation()
			self.plantsArr[-1] = edibles.Edible(plantDna, myTile=self.selectedTile)
			self.plantsArr[-1].myTile.myPlant = self.plantsArr[-1]
			


# FIRST YOU GIVE THE BIOME A NAME, THEN YOU FILL INSIDE THE ARRAY FIRST THE AMOUNT OF SUNLIGHT(0-165), AND SECOND THE RAINTICK (PER WHAT SECONDS IS IT RAINING)

biomenames = [('ANTARCTICA', [10, 80]), ('NORTH-AMERICA', [70, 60]),  ('SOUTH-AMERICA', [140, 110]), ('DYNAMICA', [80, 80]), ('EUROPE', [90, 80]),  ('AFRICA', [150, 35]), ('VERDIA', [130, 10]), ('ASIA', [60, 90]),  ('AUSTRALIA', [110, 100])]

mainwindow = Win(biomenames)
mainwindow.start_game()