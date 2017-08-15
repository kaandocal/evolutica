from .entity import Entity
from .actuator import Actuator
from .sensor import Sensor
from .food import Food
from .gfx import load_image
# agent class

import numpy as np

names = [ 'Larry', 'Patrick', 'Hannah', 'Angelina', 'Bert', 'Margaret', 'Bob', 'Vicky', 'Oliver', 'Emily', 'Lil\' Ron', 'Jackie', 'Katy P', 'Dieter', 'Elias', 'Alex', 'Mike', 'Gabe', 'Moe', 'Hazel', 'Bella', 'Aubrey', 'Penelope', 'Lizzie', 'Ed', 'Em']

class Agent(Entity):
    Emax = 400
    #constructs an agent with x,y coordinates and instantiates an Actuator 
    def __init__(self, world, x, y):
        Entity.__init__(self, world, x, y, Agent, 0)
        self.sensors = []
        self.name = np.random.choice(names)
        self.food_eaten = []
        self.last_eaten = -1
        self.energy = int((0.4 + 0.6 * np.random.random_sample())* Agent.Emax)
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

        self.energy -= 1
        if self.energy <= 0:
            self.die()

    def die(self):
        print("*{} didn't make it".format(self.name))
        self.world.remove_entity(self)

    def render(self, surf, tile_size):
        surf.blit(self.image, (self.x * tile_size, self.y * tile_size))
        for sensor in self.sensors:
            sensor.render(surf, tile_size, self.x, self.y)

    def touch(self, other):
        if other.type == Food:
            other.disappear()
            print("{}: *munch munch*".format(self.name))
            self.food_eaten.append(other)
            self.energy = np.min((Agent.Emax, self.energy + other.nutritional_value))
            self.last_eaten = self.world.round

    def dumpfood(self):
        print("--------------------------------------")
        print("Food stats for {}:".format(self.name))
        print("Total Food Eaten: {}".format(len(self.food_eaten)))
        print("Last Food Eaten: Round {}/{}".format(self.last_eaten, self.world.round))
        print("Energy Reserves: {}".format(self.energy))
        print("--------------------------------------")
