import numpy as np
from .entity import Entity
from .gfx import load_image, get_image

class FoodType:
    def __init__(self, name, shelflife, nutritional_value, smells, sounds, visible):
        self.name = name
        self.image = load_image(name)
        self.shelflife = shelflife
        self.nutritional_value = nutritional_value

        # whether this type of food can be smelled, heard or seen
        self.smells = smells
        self.sounds = sounds
        self.visible = visible

class Food(Entity):
    def __init__(self, world, x, y, foodtype):
        Entity.__init__(self, world, x, y, Food)
        self.foodtype = foodtype
        self.name = self.foodtype.name
        self.bday = self.world.round

    def disappear(self):
        self.world.remove_entity(self)

    def render(self, surf, tile_size):
        surf.blit(get_image(self.foodtype.image), (self.x * tile_size, self.y * tile_size))

    def update(self):
        # For food safety purposes
        if self.world.round >= self.bday + self.foodtype.shelflife:
            self.disappear()

foodtypes = [ ]

# Class responsible for spawning food at random
class Distributor:
    def __init__(self, world, fpr = 0.5):
        self.world = world
        # fpr = Food per round
        self.fpr = fpr

    def update(self):
        if np.random.random_sample() <= self.fpr:
            foodtype = np.random.choice(foodtypes)
            x = np.random.randint(1,self.world.width - 1)
            y = np.random.randint(1,self.world.height - 1)
            if self.world.walkable(x,y):
                food = self.world.spawn(Food,x,y,foodtype)
