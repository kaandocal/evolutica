class Entity:

    # x und y geben die Koordinaten des Objekt Entity an (Typ Integer)
    # wenn walkable == 1, kann man das Feld der Entity betreten. Wenn 0, dann nicht
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

class Ghost(Entity):
    def __init__(self, world, x, y):
        Entity.__init__(self, world, x, y, None)
