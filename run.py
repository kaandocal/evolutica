#import modules
import pygame, sys, random

#import some useful constants
from pygame.locals import *

#import classes
from master.entity import Entity
from master.world import World
from master.entityType import EntityType
from master.agent import Agent
from master.food import Food

#constants
FPS = 10
TILESIZE = 20
MAP_WIDTH = 20
MAP_HEIGHT = 20

#colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200, 0, 0)
GREEN = (0,200,0)
BLUE = (0,0,200)

#start the pygame library and create a clock module
pygame.init()
fpsClock = pygame.time.Clock()

#load the images
AGENT  = pygame.image.load('img/agent.bmp')
FOOD = pygame.image.load('img/food.bmp')
WALL = pygame.image.load('img/obstacle.bmp')

AGENT = pygame.transform.scale(AGENT, (TILESIZE,TILESIZE))
FOOD = pygame.transform.scale(FOOD, (TILESIZE,TILESIZE))
WALL = pygame.transform.scale(WALL, (TILESIZE,TILESIZE))

#this dictionary allows to get the image for a known type
images = {Agent:AGENT, Food:FOOD, "Wall":WALL}

#set up display
DISP_SURF = pygame.display.set_mode((MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE))
pygame.display.set_caption('World')

#initialize world
world = World(MAP_WIDTH, MAP_HEIGHT)
world.spawn(EntityType.Agent, 5, 5)
world.spawn(EntityType.Agent, 5, 6)
world.spawn(EntityType.Food, 7, 7)

#draws the entities onto the grid
def render():
    for entity in world.entities:
        if (entity.type != None):
            DISP_SURF.blit(images[entity.type], (entity.x * TILESIZE, entity.y * TILESIZE))

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
                pass
            #set game speed
            elif key in [ K_1, K_2, K_3, K_4 ]:
                pass
            #dump game data
            elif key == K_s:
                world.dump()
    #draw grid
    DISP_SURF.fill(BLACK)
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            if world.tiles[row,column] == World.TILE_WALL:
                DISP_SURF.blit(images["Wall"], (row * TILESIZE, column * TILESIZE))
            #add a white square (drawing surface, colour, coordinates, border thickness)
            pygame.draw.rect(DISP_SURF, WHITE, (column*TILESIZE, row*TILESIZE, TILESIZE,TILESIZE), 1)
    #update the display
    fpsClock.tick(FPS)
    world.update()
    render()
    pygame.display.update()
