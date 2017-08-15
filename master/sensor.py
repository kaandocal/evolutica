import numpy as np
from .food import Food
import pygame

class Sensor():
    def __init__(self, resolution = 0):
        self.resolution  = min(15,max(0,resolution))

    #return list of elements perceived, weighted by perception strength
    def sense(self, world, pos):
        pass

class Nose(Sensor):
    def __init__(self, resolution = 0):
        Sensor.__init__(self, resolution)
        self.name = "Nose"

    def sense(self, world, x, y):
        entities = world.entities
        targets = []
        weights = []
        #(filter out odourless entities)
        for ent in entities:
            if ent.type == Food and ent.smells:
                dist = np.sqrt((x - ent.x) ** 2 + (y - ent.y) ** 2)
                #strength of smell is dependent on the distance and the resolution of the sensor
                strength = self.resolution - dist
                if strength >= 1 and world.walkable(ent.x, ent.y):
                    targets.append(ent)
                    weights.append(strength)

        return targets, weights

    def render(self, surf, tile_size, x, y):
        return
        temp_surf = pygame.Surface(surf.get_size())
        xpos = int((x + 0.5) * tile_size)
        ypos = int((y + 0.5) * tile_size)
        temp_surf.set_alpha(128)
        colors = [pygame.Color(255, 0, 0), pygame.Color(255,100,100), pygame.Color(255,200,200) ]
        for r, c in zip(np.linspace(0, self.resolution * tile_size,4)[:0:-1], colors):
            pygame.draw.circle(temp_surf, c, (xpos, ypos), int(r))
        surf.blit(temp_surf, (0,0))
 
class Ear(Sensor):
    def __init__(self, resolution = 0):
        Sensor.__init__(self, resolution)
        self.name = "Ear"

    def sense(self, world, x, y):
        entities = world.entities
        targets = []
        weights = []
        #(filter out odourless entities)
        for ent in entities:
            if ent.type == Food and ent.sounds:
                dist = np.sqrt((x - ent.x) ** 2 + (y - ent.y) ** 2)
                #loudnes is dependent on the distance and the resolution of the sensor
                strength = self.resolution - dist
                if strength >= 1 and world.walkable(ent.x, ent.y):
                    targets.append(ent)
                    weights.append(strength)

        return targets, weights

    def render(self, surf, tile_size, x, y):
        temp_surf = pygame.Surface(surf.get_size())
        xpos = int((x + 0.5) * tile_size)
        ypos = int((y + 0.5) * tile_size)
        temp_surf.set_alpha(128)
        colors = [pygame.Color(255, 0, 0), pygame.Color(255,100,100), pygame.Color(255,200,200) ]
        for r, c in zip(np.linspace(0, self.resolution * tile_size,4)[:0:-1], colors):
            pygame.draw.circle(temp_surf, c, (xpos, ypos), int(r))

        surf.blit(temp_surf, (0,0))
