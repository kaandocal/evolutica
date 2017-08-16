from .entity import Entity
from .actuator import Actuator
from .sensor import Sensor, Nose, Ear
from .food import Food, foodtypes
from .gfx import load_image
# agent class

import numpy as np

names = [ 'Larry', 'Patrick', 'Hannah', 'Angelina', 'Bert', 'Margaret', 'Bob', 'Vicky', 'Oliver', 'Emily', 'Lil\' Ron', 'Jackie', 'Katy P', 'Dieter', 'Elias', 'Alex', 'Mike', 'Gabe', 'Moe', 'Hazel', 'Bella', 'Aubrey', 'Penelope', 'Lizzie', 'Ed', 'Em']

class Agent(Entity):
    Emax = 500
    #constructs an agent with x,y coordinates and instantiates an Actuator 
    def __init__(self, world, x, y):
        Entity.__init__(self, world, x, y, Agent)
        self.sensors = []
        self.name = np.random.choice(names)
        self.food_eaten = {}
        for ft in foodtypes:
            self.food_eaten[ft] = 0
        self.last_eaten = -1
        self.birthday = world.round
        self.energy = int((0.4 + 0.6 * np.random.random_sample())* Agent.Emax)
        self.actuator = Actuator(self)
        self.children = []
        self.image = load_image("agent")

    def addsensor(self, type, resolution):
        self.sensors.append(type(self.world, resolution))

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
        self.deceased = self.world.round
        self.world.remove_entity(self)

    def circleoflife(self):
        s = self.world.spawn(Agent, self.x, self.y)
        d = self.world.spawn(Agent, self.x, self.y)

        for sensor in self.sensors:
            sstr_s = sensor.resolution + np.random.normal(0, 1.5)
            sstr_d = sensor.resolution + np.random.normal(0, 1.5)

            s.addsensor(sensor.type, sstr_s)
            d.addsensor(sensor.type, sstr_d)

        energy = self.energy + np.random.randint(50,100)
        share_s = 0.3 + 0.4 * np.random.random_sample()
        s.energy = int(share_s * energy)
        d.energy = int((1 - share_s) * energy)

        print("*plop plop*")
        print("{}'s been busy it seems...*".format(self.name))
        print("Happy B-day, {} and {}!".format(s.name, d.name))

        self.children.append(s)
        self.children.append(d)

        self.deceased = self.world.round
        self.world.remove_entity(self)

    def render(self, surf, tile_size):
        surf.blit(self.image, (self.x * tile_size, self.y * tile_size))

    def touch(self, other):
        if other.deceased:
            return

        if other.type == Food:
            other.disappear()
            print("{}: *munch munch*".format(self.name))
            self.food_eaten[other.foodtype] += 1
            self.energy = min(Agent.Emax, self.energy + other.foodtype.nutritional_value)
            self.last_eaten = self.world.round

    def dumpfood(self):
        print("--------------------------------------")
        print("Food stats for {}:".format(self.name))
        total_food = sum([v for v in self.food_eaten.values()])
        print("Total Food Eaten: {}".format(total_food))
        print("Last Food Eaten: Round {}/{}".format(self.last_eaten, self.world.round))
        print("Energy Reserves: {}".format(self.energy))
        for ft in foodtypes:
            print("Amount of {} eaten: {}".format(ft.name, self.food_eaten[ft]))
        print("--------------------------------------")

    def dumpsensors(self):
        print("--------------------------------------")
        print("Sensor stats for {}:".format(self.name))
        for s in self.sensors:
            print("{}: {}/15".format(s.name,s.resolution))
        print("--------------------------------------")
