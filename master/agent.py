from .entity import Entity
from .actuator import Actuator
from .sensor import Sensor
# agent class
class Agent(Entity):
    #constructs an agent with x,y coordinates and instantiates an Actuator 
    def __init__(self, world, x, y):
        Entity.__init__(self, world, x, y, Agent, 0)
        self.actuator = Actuator(world)

    # updates agents
    # (should later call Sensor and Actuator
    def update(self):
        x, y = self.actuator.propose(self.x, self.y)
        if self.world.walkable(x,y):
            self.x = x
            self.y = y


