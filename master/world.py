from .agent import Agent
from .food import Food, Distributor
from .entity import Entity
from .gfx import load_image
import pickle
import numpy as np
import pygame

#represents the world grid with all entities
class World:
    TILE_WALL = 1

    def __init__(self, filename):
        worldmap = load_image(filename, (0,0))
        worldmap = worldmap.convert(8)
        self.width, self.height = worldmap.get_size()

        #world array which contains the entities and its copy
        self.entities = []
        self.remove_list = []
        self.distributor = Distributor(self)
        self.tiles = np.zeros((self.width,self.height),dtype='uint32')

        #build wall around world
        self.tiles[0,:] = self.tiles[-1,:] = World.TILE_WALL
        self.tiles[:,0] = self.tiles[:,-1] = World.TILE_WALL

        self.round = 0

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
        return ent

    def remove_entity(self, ent):
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

    def dump(self):
        i = 0
        while True:
            filename = "saves/save{}".format(i)
            try:
                out = file(filename, "rb")
            except IOError:
                break
            i += 1

        out = file(filename, "wb")
        pickle.dump(self, out)
        print("Saved game data to file '{}'".format(filename))

    def foodinfo(self):
        for ent in self.entities:
            if ent.type == Agent:
                ent.dumpfood()
