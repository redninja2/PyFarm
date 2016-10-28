# Original author's comment (Not original, but author I got this from):
# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

# http://githum.com/redninja2 's comment:
# edited original class to fit my needs, to properly 
# load spritesheets according to my standards. The 
# class I got was flawed and was difficult to use.

import pygame

class spritesheet(object):

	def __init__(self, filename):
		try:
			self.sheet = pygame.image.load(filename).convert_alpha()
		except (pygame.error):
			print ('Unable to load spritesheet image:', filename)
			raise (SystemExit)
			
	# Load a specific image from a specific rectangle
	def image_at(self, rectangle):
		"Loads image from x,y,x+offset,y+offset"
		rect = pygame.Rect(rectangle)
		self.sheet.set_clip(rect)
		image = self.sheet.subsurface(self.sheet.get_clip())
		return image