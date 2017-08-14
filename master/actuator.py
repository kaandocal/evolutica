import numpy as np

# Actuator of an agent (incomplete) 
class Actuator:
    def __init__(self, world):
        self.world = world
        self.sensors = []
        self.goal = None

    def addsensor(self, sensor):
        self.sensors.append(sensor)

    #reorient and find a new goal
    def reflect(self):
        #check sensor inputs and create list of potential targets and weights
        targets = []
        weights = []

        for sensor in self.sensors:
            ts, ws = sensor.sense(world, self.x, self.y)
            targets += ts
            weights += ws

        #nothing found => stay idle
        if len(targets) == 0:
            self.goal = None
            return

        #choose random target according to weight
        z = np.sum(weights)
        self.goal = np.random.choice(targets, p = np.asarray(weights) / z)

            
# act function. Randomly moves agent in one direction.
# receives x,y, the current coordinates of the agent
# returns new coordinates
    def propose(self, x, y):
        if self.goal == None:
            r = np.random.randint(0, 5)
            # North
            if r == 1:
                x = x
                y = y + 1
            # South
            elif r == 2:
                x = x
                y = y - 1
            # East
            elif r == 3:
                x = x + 1
                y = y
            # West
            elif r == 4:
                x = x - 1
                y = y
            self.reflect()
            return (x, y)
