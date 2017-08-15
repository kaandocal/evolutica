#import modules
import pygame, sys, random

#import some useful constants
from pygame.locals import *

#import classes
from master.entity import Entity
from master.world import World
from master.agent import Agent
from master.sensor import Nose, Ear, Eye, Brain
from master.food import Food, FoodType
import master.food as food
import master.gfx as gfx
import master.data as data

#constants
speeds = { K_1: 2, K_2: 5, K_3: 10, K_4: 20, K_5 : 30, K_6 : 40 }
speed = speeds[K_1]
TILESIZE = 20

gfx.default_size = (TILESIZE,TILESIZE)

#colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200, 0, 0)
GREEN = (0,200,0)
BLUE = (0,0,200)

#start the pygame library and create a clock module
pygame.init()
fpsClock = pygame.time.Clock()

wall_image = gfx.load_image("wall")

#initialize world
world = World('world')
food.foodtypes.append(FoodType("burger", 60, 50, smells=True, sounds=False, visible=False))
food.foodtypes.append(FoodType("orb", 60, 50, smells=False, sounds=True, visible=False))
food.foodtypes.append(FoodType("blob", 60, 50, smells=False, sounds=False, visible=True))
smart_one = world.spawn(Agent, 5, 5)
nose = Nose(world,resolution=10)
smart_one.addsensor(nose)
smart_one = world.spawn(Agent, 5, 6)
eye = Eye(world,resolution=10)
smart_one.addsensor(eye)
smart_one = world.spawn(Agent, 20, 20)
ear = Ear(world,resolution=10)
smart_one.addsensor(ear)
brain = Brain(world,resolution=10)
smart_one.addsensor(brain)

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
                data.dump(world)
            elif key == K_i:
                data.sensorinfo(world)
            elif key == K_f:
                data.foodinfo(world)
            elif key == K_r:
                data.hof(world)
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
