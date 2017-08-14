#import modules
import pygame, sys, random

#import some useful constants
from pygame.locals import *

#import classes
from master.gfx import load_image
from master.entity import Entity
from master.world import World
from master.agent import Agent
from master.sensor import Smell
from master.food import Food
import master.gfx

#constants
speeds = { K_1: 2, K_2: 5, K_3: 10, K_4: 20, K_5 : 30, K_6 : 40 }
speed = speeds[K_3]
TILESIZE = 20

master.gfx.default_size = (TILESIZE,TILESIZE)

#colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200, 0, 0)
GREEN = (0,200,0)
BLUE = (0,0,200)

#start the pygame library and create a clock module
pygame.init()
fpsClock = pygame.time.Clock()

wall_image = load_image("wall")

#initialize world
world = World('world')
smart_one = world.spawn(Agent, 5, 5)
nose = Smell(resolution=5)
smart_one.addsensor(nose)
world.spawn(Agent, 5, 6)
world.spawn(Food, 7, 7)
world.spawn(Food, 10, 7)
world.spawn(Food, 15, 14)
world.spawn(Food, 14, 7)

#set up display
DISP_SURF = pygame.display.set_mode((world.width*TILESIZE, world.height*TILESIZE))
pygame.display.set_caption('World')

#draws the entities onto the grid
def render():
    for entity in world.entities:
        entity.render(DISP_SURF, TILESIZE)

#world loop
while True:
    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #user clicks on an entity or a tile
        elif event.type == MOUSEBUTTONUP:
            pass
        #key command
        elif event.type == KEYDOWN:
            key = event.key
            #pause game
            if key == K_SPACE:
                speed = 0
            #set game speed
            elif key in speeds.keys():
                speed = speeds[key]
            #dump game data
            elif key == K_s:
                world.dump()
    #draw grid
    DISP_SURF.fill(BLACK)
    for row in range(world.height):
        for column in range(world.width):
            if world.tiles[row,column] == World.TILE_WALL:
                DISP_SURF.blit(wall_image, (row * TILESIZE, column * TILESIZE))
            #add a white square (drawing surface, colour, coordinates, border thickness)
            pygame.draw.rect(DISP_SURF, WHITE, (column*TILESIZE, row*TILESIZE, TILESIZE,TILESIZE), 1)
    #update the display
    if speed != 0:
        fpsClock.tick(speed)
        world.update()
    else:
        fpsClock.tick(10)
    render()
    pygame.display.update()
