from .entity import Entity
from .entityType import EntityType
from .actuator import Actuator
from .sensor import Sensor
from .food import Food
from .gfx import load_image
# agent class
class Agent(Entity):
    #constructs an agent with x,y coordinates and instantiates an Actuator 
    def __init__(self, world, x, y):
        Entity.__init__(self, world, x, y, Agent, 0)
        self.sensors = []
        self.food_eaten = []
        self.actuator = Actuator(self)
        self.image = load_image("agent")

    def addsensor(self, sensor):
        self.sensors.append(sensor)

    # updates agents
    # (should later call Sensor and Actuator
    def update(self):
        x, y = self.actuator.propose(self.x, self.y)
        if self.world.walkable(x,y):
            self.x = x
            self.y = y

    def render(self, surf, tile_size):
        surf.blit(self.image, (self.x * tile_size, self.y * tile_size))
        for sensor in self.sensors:
            sensor.render(surf, tile_size, self.x, self.y)

    def touch(self, other):
        if other.type == Food:
            other.disappear()
            print("*munch munch*")
            self.food_eaten.append(other)
