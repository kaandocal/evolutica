import numpy as np
from .entity import Entity
from .gfx import load_image

class FoodType:
    def __init__(self, name, shelflife, nutritional_value, smells, sounds, visible):
        self.name = name
        self.image = load_image(name)
        self.shelflife = shelflife
        self.nutritional_value = nutritional_value
        self.smells = smells
        self.sounds = sounds
        self.visible = visible

class Food(Entity):
    # constructs Food with coords x,y and kind, which is 0 by default
    def __init__(self, world, x, y, foodtype):
        Entity.__init__(self, world, x, y, Food)
        self.foodtype = foodtype
        self.name = self.foodtype.name
        self.bday = self.world.round

    def disappear(self):
        self.world.remove_entity(self)

    def render(self, surf, tile_size):
        surf.blit(self.foodtype.image, (self.x * tile_size, self.y * tile_size))

    def update(self):
        if self.world.round >= self.bday + self.foodtype.shelflife:
            self.disappear()

rpf = 5
foodtypes = [ ]

class Distributor:
    def __init__(self, world):
        self.world = world

    def update(self):
        if np.random.randint(0,rpf) == 0:
            foodtype = np.random.choice(foodtypes)
            x = np.random.randint(1,self.world.width - 1)
            y = np.random.randint(1,self.world.height - 1)
            if self.world.walkable(x,y):
                food = self.world.spawn(Food,x,y,foodtype)
