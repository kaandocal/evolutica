import numpy as np
from .food import Food
from .entity import Ghost
import pygame

class Sensor():
    def __init__(self, world, type, resolution = 0):
        self.world = world
        self.type = type
        self.resolution  = min(15,max(0,resolution))

    #return list of elements perceived, weighted by perception strength
    def sense(self, pos):
        pass

# The next three sensors are identical but for their names
class Nose(Sensor):
    name = "Nose"

    def __init__(self, world, resolution = 0):
        Sensor.__init__(self, world, Nose, resolution)

    def sense(self, x, y):
        entities = self.world.entities
        targets = []
        weights = []
        #(filter out odourless entities)
        for ent in entities:
            if ent.type == Food and ent.foodtype.smells:
                dist = np.sqrt((x - ent.x) ** 2 + (y - ent.y) ** 2)
                #strength of smell is dependent on the distance and the resolution of the sensor
                strength = self.resolution - dist
                if strength >= 1 and self.world.walkable(ent.x, ent.y):
                    targets.append(ent)
                    weights.append(strength)

        return targets, weights
 
class Ear(Sensor):
    name = "Ear"

    def __init__(self, world, resolution = 0):
        Sensor.__init__(self, world, Ear, resolution)

    def sense(self, x, y):
        entities = self.world.entities
        targets = []
        weights = []
        #(filter out odourless entities)
        for ent in entities:
            if ent.type == Food and ent.foodtype.sounds:
                dist = np.sqrt((x - ent.x) ** 2 + (y - ent.y) ** 2)
                #loudness is dependent on the distance and the resolution of the sensor
                strength = self.resolution - dist
                if strength >= 1 and self.world.walkable(ent.x, ent.y):
                    targets.append(ent)
                    weights.append(strength)

        return targets, weights 

class Eye(Sensor):
    name = "Eye"

    def __init__(self, world, resolution = 0):
        Sensor.__init__(self, world, Eye, resolution)

    def sense(self, x, y):
        entities = self.world.entities
        targets = []
        weights = []
        #(filter out odourless entities)
        for ent in entities:
            if ent.type == Food and ent.foodtype.visible:
                dist = np.sqrt((x - ent.x) ** 2 + (y - ent.y) ** 2)
                #clarity is dependent on the distance and the resolution of the sensor
                strength = self.resolution - dist
                if strength >= 1 and self.world.walkable(ent.x, ent.y):
                    targets.append(ent)
                    weights.append(strength)

        return targets, weights

# This is a bit different
class Brain(Sensor):
    name = "Brain"

    def __init__(self, world, resolution = 0):
        Sensor.__init__(self, world, Brain, resolution)
        self.target = Ghost(world, 0, 0)

    def sense(self, x, y):
        self.target.x = np.random.randint(0, self.world.width)
        self.target.y = np.random.randint(0, self.world.height)
        targets = [self.target]
        # Preference given to faraway targets (why?)
        weights = [self.resolution * 0.05 * (abs(x - self.target.x) + abs(y - self.target.y))/ (self.world.width + self.world.height)]
        return targets, weights


sensortypes = [ Nose, Eye, Ear, Brain ]
