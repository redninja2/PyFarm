# Author: http://github.com/redninja2
# Project start date: July 9th, 2015
# A simple game I wanted to make to further my knowlege and experience
# with python and the concept of a moving camera. As far as the "game", 
# I do not intend on actually getting any where on the functionality. 
# My core goal was getting a moving camera.

import pygame  # game engine
import sys  # needed to quitWindow the program
import os  # to set the location of the GUI
import spritesheet  # needed to manipulate a spritesheet

# Camera: displays content on the screen and allows moving the camera
class Camera(object):
	def __init__(self, surface, dimensions):
		self.width = dimensions[0]
		self.height = dimensions[1]
		
		self.surface = surface

	# render(): Renders content on the screen
	def render(self, image, location):
		self.surface.blit(image, location)
	
	# draw(): Determines where the camera is looking in relation to 
	# the world location. It then calls the render method to render content.
	def draw(self, image, world_location):
		# Determines where on the screen the content should be rendered in 
		# relation to the world loction and camera location
		x = world_location[0] - cam_x_loc 
		y = world_location[1] - cam_y_loc
		
		# gets the image size
		image_size = image.get_rect().size
		
		# Makes sure that the image does not get drawn outside the camera boundries
		if x <= self.width and x + image_size[0] >= 1:
			if y + image_size[1] >= 1 and y <= self.width:
				self.render(image, (x, y))  # Sends the image to be rendered

# Moves camera in a (string) direction: left, up, right, and down.
def move_cam(direction):

	# uses the global cam x location and cam y location
	global cam_x_loc, cam_y_loc 
	
	# if the direction is left >> and cam x location isn't going over the 
	# world border, then move the camera location to the left 64px (1 tile)
	if direction == "left":
		if cam_x_loc > 0:
			cam_x_loc -= 64
			print("left X: {}".format(cam_x_loc))
		else:
			print(cam_x_loc)
	
	# same as for left, but going up. 
	elif direction == "up":
		if cam_y_loc > 0:
			cam_y_loc -= 64
			print("up Y: {}".format(cam_y_loc))
		else:
			print(cam_y_loc)
	# same as for left, but going right
	elif direction == "right":
		if cam_x_loc + window_x < world_x:
			cam_x_loc += 64
			print("right X: {}".format(cam_x_loc))
		else:
			print(cam_x_loc)
	
	# same as for left, but going down
	elif direction == "down":
		if cam_y_loc + window_y < world_y:
			cam_y_loc += 64
			print("down Y: {}".format(cam_y_loc))
		else:
			print(cam_y_loc)
	# if the direction passed into the method is not left, up, right, or down,
	# then it is invalid. 
	else:
		print("move_cam() invalid direction: {}".format(direction))
	
# quitWindow() will shutdown the program
def quitWindow():
	print("Exiting...")
	sys.exit()

# Draws a grid according to the requested dimensions, on the provided surface
def draw_grid(dimension, surface):
	for grid_x in range(dimension, window_x, dimension):
		pygame.draw.line(surface, (0, 0, 100), [grid_x, 0], [grid_x, window_y], 1)
	for grid_y in range(dimension, window_y, dimension):
		pygame.draw.line(surface, (100, 100, 100), [0, grid_y], [window_x, grid_y], 1)
		
# Gets coordinates according to which tile is requested
def get_coords(tile):
	coord = (tile[0] * 64, tile[1] * 64)
	return coord
	
# Gets the tile according to the coordinates requested
def get_tile(coord):
	devisor = 64
	tilex = int(coord[0] / devisor)
	tiley = int(coord[1] / devisor)
	tile = (tilex, tiley)
	return tile
	
# Selects a tile based on the mouse position
def select_tile(m_pos):
	global tile_selected, selected_tile
	tile_selected = True
	selected_tile = get_tile(m_pos)

def init():
	global clock, screen, window_x, window_y, world_x, world_y, tiles_x, tiles_y, tile_selected, selected_tile, cam, cam_x_loc, cam_y_loc
	
	print ("Starting...")
	
	# Sets the location of the window so nothing is hidden from the user
	os.environ['SDL_VIDEO_WINDOW_POS'] = "{0}, {1}".format(7, 31)
	
	pygame.init()  # initializes pygame

	# Sets game variables
	window_x = 1280
	window_y = 768
	world_x = window_x * 2  # makes the world twice as large as the window size
	world_y = window_y * 2
	clock = pygame.time.Clock()  # allows for ticking

	screen = pygame.display.set_mode([window_x, window_y], pygame.RESIZABLE)
	
	tile_selected = False  # Game starts without selected tile
	selected_tile = ()  # slected_tile starts with an empty tuple, because there is no selected tile yet.
	
	# Starts the camera at location (0, 0) in relation to the world
	cam_x_loc = 0 
	cam_y_loc = 0 
	
	# creates an Camera object for the purpose of drawing images to the screen
	cam = Camera(screen, (window_x, window_y))
	
	# Hides the system cursor so we can draw our own
	pygame.mouse.set_visible(False)
	
	# Allows the cycling through of the sprite sheet images
	tiles_x = []
	tiles_y = []
	for x in range(0, 8, 1):
		for y in range(0, 8, 1):
			tiles_x.append(x)
			tiles_y.append(y)
	
	# prep images for use
	load_images(os.path.join('images', 'spritesheet.png'))
	scale_images()

# Loads all sprites from the spritesheet into a list, image[]
def load_images(sheet):
	global image, cursor
	image = []
	ss = spritesheet.spritesheet(sheet)
	
	# cycles through the pixels in the spritesheet. not very
	# good method as I don't check if there is any more pixels, 
	# I just assume that the sheet is 128x128. 
	# Order of for y and for x is important: We want to load the images
	# from row to row (left to right), not column to column (up and down).
	for y in range(0, 128, 16):  # cycle through the rows
		for x in range(0, 128, 16):  # cycle through tiles in the row 
			image.append(ss.image_at((x, y, 16, 16)))
	
	# Set our custom cursor to an image in the spritesheet
	cursor = pygame.transform.scale(image[2], (16, 16))

# cycle though all the images and scale them up to 64x64, the size of a tile
def scale_images():
	global image
	temp_imgs = image
	image = []
	for i in range(0, 64):
		image.append(pygame.transform.scale(temp_imgs[i], (64, 64)))

# animation(): redraws the content to the screen. 
def animate():

	# Give the GUI a solid background and draw a grid.
	screen.fill([0, 200, 0])
	draw_grid(64, screen)
	
	# Draws images to the screen. All this does is redraw my spritesheet to the scree,
	# but instead of just drawing the spritesheet, I draw the scaled tiles.
	for i in range(0, 64, 1):
		cam.draw(image[i], get_coords((tiles_y[i], tiles_x[i])))
	
	# Draws a rectangle around the selected tile
	if tile_selected:
		pygame.draw.rect(screen, (180, 0, 0), pygame.Rect(get_coords(selected_tile), (64, 64)), 5)
		
	# Draws our cursor image to the screen at the position of the actual mouse
	screen.blit(cursor, mouse_pos)

	# Publishes our screen updates to the window
	pygame.display.flip()
	
init()  # initialize the program.

# Game loop
while 1:
	global mouse_pos
	mouse_pos = pygame.mouse.get_pos()
	
	# if the mouse is within 20px of the border, the camera moves
	if mouse_pos[0] <= 20:
		move_cam("left")
	elif mouse_pos[0] >= window_x - 20:
		move_cam("right")
	if mouse_pos[1] <= 20:
		move_cam("up")
	elif mouse_pos[1] >= window_y - 20:
		move_cam("down")
	
	clock.tick(60)  # the game fps. The higher the tick, the faster the gametime is.
	
	animate()  # refresh the screen 

	# Check for events so we can respond to them.
	for event in pygame.event.get():
	
		# If the event type is QUIT
		if event.type == pygame.QUIT:
			quitWindow()
		
		# If the event is a key down event
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quitWindow()  # escape will quitWindow the game
			elif event.key == pygame.K_LEFT:
				move_cam("left")  # left arrow moves the camera left one tile
			elif event.key == pygame.K_UP:
				move_cam("up")  # up arrow moves camera up one tile
			elif event.key == pygame.K_RIGHT:
				move_cam("right")  # right arrow moves camera right one tile
			elif event.key == pygame.K_DOWN:
				move_cam("down")  # down arrow moves camera down one tile
				
		# If the event is a mouse click
		elif event.type == pygame.MOUSEBUTTONDOWN:
			
			# Left click
			if event.button == 1:
				print("Left click")
				select_tile(mouse_pos)
			
			# Right click or double click
			elif event.button == 3:
				print("Right click")
