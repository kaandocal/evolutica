class Entity:

    # x und y geben die Koordinaten des Objekt Entity an (Typ Integer)
    # wenn walkable == 1, kann man das Feld der Entity betreten. Wenn 0, dann nicht
    def __init__(self, world, x, y, type = None, walkable = 1):
            self.world = world
            self.type = type
            self.x = x
            self.y = y
            self.walkable = walkable
            self.dead = False

    # update function
    # should be implemented by each child class of Entity
    def update(self):
        pass

    def render(self, surface, tile_size):
        pass

    def touch(self, other):
        pass
