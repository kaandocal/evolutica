import numpy as np
from .entity import Entity
from .gfx import load_image

class Food(Entity):
    # constructs Food with coords x,y and kind, which is 0 by default
    def __init__(self, world, x, y, shelflife, nutritional_value = 100, kind = 0):
        Entity.__init__(self, world, x, y, Food)
        self.bday = self.world.round
        self.shelflife = shelflife
        self.nutritional_value = nutritional_value
        self.kind = kind
        self.image = load_image("food")

    def disappear(self):
        self.world.remove_entity(self)

    def render(self, surf, tile_size):
        surf.blit(self.image, (self.x * tile_size, self.y * tile_size))

    def update(self):
        if self.world.round >= self.bday + self.shelflife:
            self.disappear()

rpf = 25

class Distributor:
    def __init__(self, world):
        self.world = world

    def update(self):
        if np.random.randint(0,rpf) == 0:
            shelflife = np.random.randint(50,100)
            x = np.random.randint(1,self.world.width - 1)
            y = np.random.randint(1,self.world.height - 1)
            food = self.world.spawn(Food,x,y,shelflife=shelflife)
