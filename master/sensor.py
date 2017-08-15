import numpy as np
import pygame

class Sensor():
    def __init__(self, resolution = 0):
        self.resolution  = resolution

    #return list of elements perceived, weighted by perception strength
    def sense(self, world, pos):
        pass

class Smell(Sensor):
    def __init__(self, resolution = 0):
        Sensor.__init__(self, resolution)

    def sense(self, world, x, y):
        entities = world.entities
        targets = []
        weights = []
        #(filter out odourless entities)
        for ent in entities:
            dist = np.sqrt((x - ent.x) ** 2 + (y - ent.y) ** 2)
            #strength of smell is dependent on the distance and the resolution of the sensor
            strength = self.resolution - dist
            if strength >= 1:
                targets.append(ent)
                weights.append(np.floor(strength))

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
