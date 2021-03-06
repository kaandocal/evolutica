from .agent import Agent
from .food import Food, Distributor
from .entity import Entity
from .gfx import load_image, get_image
import numpy as np
import pygame

#represents the world grid with all entities
class World:
    TILE_WALL = 1

    def __init__(self, filename):
        worldmap = load_image(filename, (0,0))
        worldmap = get_image(worldmap).convert(8)
        self.width, self.height = worldmap.get_size()

        # List containing: currently alive entities, entities that died in the current round, all entities that ever lived
        self.entities = []
        self.remove_list = []
        self.halloffame = []
        self.distributor = Distributor(self)
        self.tiles = np.zeros((self.width,self.height),dtype='uint32')

        #build wall around world
        self.tiles[0,:] = self.tiles[-1,:] = World.TILE_WALL
        self.tiles[:,0] = self.tiles[:,-1] = World.TILE_WALL

        self.round = 0

        self.sensor_cost = 0.09
        self.mutation_variance = 1

        # Fill in the tiles according to loaded world map file
        for i in range(self.width):
            for j in range(self.height):
                if worldmap.get_at((i,j)) != (0,0,0):
                    self.tiles[i,j] = World.TILE_WALL

    def walkable(self, x, y):
        return (x >= 0 and x < self.width) and (y >= 0 and y < self.height) and self.tiles[x,y] != World.TILE_WALL

    # Spawns entities
    def spawn(self, constructor, x, y, *args, **kwargs):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            print("Warning: Trying to spawn entity outside world")
            return

        #avoid spawning entities in walls
        if self.tiles[x,y] == World.TILE_WALL:
            pass
        
        ent = constructor(self,x,y,*args,**kwargs)
        self.entities.append(ent)
        if ent.type == Agent:
            self.halloffame.append(ent)
        return ent

    def remove_entity(self, ent):
        ent.deceased = self.round
        self.remove_list.append(ent)

    #updates all entities and the world grid
    def update(self):
        #call the update method of all entities in the world
        for entity in self.entities:
            entity.update()
            for e2 in self.entities:
                if e2 is not entity and entity.x == e2.x and entity.y == e2.y:
                    entity.touch(e2)

        for ent in self.remove_list:
            if ent in self.entities:
                self.entities.remove(ent) 
        self.remove_list = []
        self.distributor.update()
        self.round += 1
        return

