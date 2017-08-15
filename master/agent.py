from .entity import Entity
from .actuator import Actuator
from .sensor import Sensor, Nose, Ear
from .food import Food
from .gfx import load_image
# agent class

import numpy as np

names = [ 'Larry', 'Patrick', 'Hannah', 'Angelina', 'Bert', 'Margaret', 'Bob', 'Vicky', 'Oliver', 'Emily', 'Lil\' Ron', 'Jackie', 'Katy P', 'Dieter', 'Elias', 'Alex', 'Mike', 'Gabe', 'Moe', 'Hazel', 'Bella', 'Aubrey', 'Penelope', 'Lizzie', 'Ed', 'Em']

class Agent(Entity):
    Emax = 500
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
        p_offspring = max(0, (self.energy - 350) / 4500.)
        if np.random.random_sample() <= p_offspring:
            self.circleoflife()

    def die(self):
        print("*{} didn't make it".format(self.name))
        self.world.remove_entity(self)

    def circleoflife(self):
        s = self.world.spawn(Agent, self.x, self.y)
        d = self.world.spawn(Agent, self.x, self.y)

        for sensor in self.sensors:
            sstr_s = sensor.resolution + np.random.normal(0, 1)
            sstr_d = sensor.resolution + np.random.normal(0, 1)

            s.addsensor(Nose(sstr_s))
            d.addsensor(Nose(sstr_d))

        energy = self.energy + np.random.randint(50,100)
        share_s = 0.3 + 0.4 * np.random.random_sample()
        s.energy = int(share_s * energy)
        d.energy = int((1 - share_s) * energy)

        print("*plop plop*")
        print("{}'s been busy it seems...*".format(self.name))
        print("Happy B-day, {} and {}!".format(s.name, d.name))
        self.world.remove_entity(self)

    def render(self, surf, tile_size):
        surf.blit(self.image, (self.x * tile_size, self.y * tile_size))
        for sensor in self.sensors:
            sensor.render(surf, tile_size, self.x, self.y)

    def touch(self, other):
        if other.dead:
            return

        if other.type == Food:
            other.disappear()
            print("{}: *munch munch*".format(self.name))
            self.food_eaten.append(other)
            self.energy = min(Agent.Emax, self.energy + other.nutritional_value)
            self.last_eaten = self.world.round

    def dumpfood(self):
        print("--------------------------------------")
        print("Food stats for {}:".format(self.name))
        print("Total Food Eaten: {}".format(len(self.food_eaten)))
        print("Last Food Eaten: Round {}/{}".format(self.last_eaten, self.world.round))
        print("Energy Reserves: {}".format(self.energy))
        print("--------------------------------------")

    def dumpsensors(self):
        print("--------------------------------------")
        print("Sensor stats for {}:".format(self.name))
        for s in self.sensors:
            print("{}: {}/15".format(s.name,s.resolution))
        print("--------------------------------------")
