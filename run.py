#import modules
import pygame, sys, random

#import some useful constants
from pygame.locals import *

#import classes
from master.entity import Entity
from master.world import World
from master.agent import Agent
from master.sensor import Nose, Ear, Eye, Brain, sensortypes
from master.food import Food, FoodType
import master.food as food
import master.gfx as gfx
import master.data as data

#constants
speeds = { K_1: 2, K_2: 5, K_3: 10, K_4: 20, K_5 : 30, K_6 : 40, K_7 : 80 }
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

def init_world(filename):
    inp = open(filename, "r")
    world = World('world')
    for l in inp.readlines():
        words = l.split(' ')
        if len(words) == 0:
            continue

        if words[0] == "Agent":
            if len(words) < 3:
                print("Warning: Cannot parse line '{}'".format(l))

            x = int(words[1])
            y = int(words[2])

            world.spawn(Agent, x, y)
        elif words[0] == "Sensor":
            if len(world.entities) == 0:
                print("Warning: Adding sensors to non-entity")

            if len(words) < 3:
                print("Warning: Cannot parse line '{}'".format(l))

            res = float(words[2])

            ent = world.entities[-1]
            
            success = False
            for st in sensortypes:
                if words[1] == st.name:
                    ent.addsensor(st, resolution=res)
                    success = True
                    break

            if not success:
                print("Warning: Cannot parse line '{}'".format(l))

        elif words[0] == "Food":
            if len(words) < 2:
                print("Warning: Cannot parse line '{}'".format(l))

            world.distributor.fpr = float(words[1])

        else:
            print("Warning: Cannot parse line '{}'".format(l))

    return world

food.foodtypes.append(FoodType("burger", 300, 50, smells=True, sounds=False, visible=False))
food.foodtypes.append(FoodType("orb", 300, 50, smells=False, sounds=True, visible=False))
food.foodtypes.append(FoodType("blob", 300, 50, smells=False, sounds=False, visible=True))

world = init_world("brainvsnone")

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
            if world.tiles[column,row] == World.TILE_WALL:
                DISP_SURF.blit(wall_image, (column * TILESIZE, row * TILESIZE))
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
