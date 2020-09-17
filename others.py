import pygame
import random
import time


class Colors:
    
	white = (255, 255, 255)
	blue  = (0,0,255)
	red = (255,0,0)
	darkred = (225, 0, 20)
	lime = (0,255,0)
	yellow = (255,215,0)
	orange = (255,165,0)
	turquasie = (0, 255,255)
	purple = (255,0,255)
	black = (0,0,0)
	magenta = (255,0,255)
	maroon = (128,0,0)
	olive = (128,128,0)
	green = (0,128,0)
	navy = (0,0,128)
	teal = (0,128,128)
	purple = (128,0,128)
	silver = (192,192,192)
	pink  = (200, 40, 130)

	def random_color():

		return (random.randint(0,255), random.randint(0,255), random.randint(0,255))