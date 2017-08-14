from .agent import Agent
from .food import Food
from .entityType import EntityType
from .entity import Entity
import pickle
import numpy as np

#represents the world grid with all entities
class World:
    TILE_WALL = 1

    def __init__(self, w, h):
        self.width = w
        self.height = h

        #world array which contains the entities and its copy
        self.entities = []
        self.tiles = np.zeros((self.width,self.height),dtype='uint32')

        #build wall around world
        self.tiles[0,:] = self.tiles[-1,:] = World.TILE_WALL
        self.tiles[:,0] = self.tiles[:,-1] = World.TILE_WALL

        print(self.tiles)

    def walkable(self, x, y):
        return self.tiles[x,y] != World.TILE_WALL

    # Spawns entities
    def spawn(self, type, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            print("Warning: Trying to spawn entity outside world")
            return

        #avoid spawning entities in walls
        if self.tiles[x,y] == World.TILE_WALL:
            pass

        if type == EntityType.Agent:
            self.entities.append(Agent(self, x,y))
        elif type == EntityType.Food:
            self.entities.append(Food(self,x,y))
        else:
            print("ERROR: Entity could not be spawned, type '{}' doesn't exist".format(type))

    #updates all entities and the world grid
    def update(self):
        #call the update method of all entities in the world
        for entity in self.entities:
            entity.update()

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
