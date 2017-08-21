class Entity:

    # x und y geben die Koordinaten des Objekt Entity an (Typ Integer)
    def __init__(self, world, x, y, type = None):
            self.name = None
            self.world = world
            self.type = type
            self.x = x
            self.y = y
            self.deceased = None

    # update function
    # should be implemented by each child class of Entity
    def update(self):
        pass

    def render(self, surface, tile_size):
        pass

    def touch(self, other):
        pass

# Imaginary targets used by the brain
class Ghost(Entity):
    def __init__(self, world, x, y):
        Entity.__init__(self, world, x, y, None)
