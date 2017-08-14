from .entity import Entity
from .gfx import load_image
class Food(Entity):
    # constructs Food with coords x,y and kind, which is 0 by default
    def __init__(self, world, x, y, kind = 0):
        Entity.__init__(self, world, x, y, Food)
        self.kind = kind
        self.image = load_image("food")

    def disappear(self):
        self.world.remove_entity(self)

    def render(self, surf, tile_size):
        surf.blit(self.image, (self.x * tile_size, self.y * tile_size))
