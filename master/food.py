from .entity import Entity
class Food(Entity):
    # constructs Food with coords x,y and kind, which is 0 by default
    def __init__(self, world, x, y, kind = 0):
        Entity.__init__(self, world, x, y, Food)
        self.kind = kind
