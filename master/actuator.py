#import pyximport
#pyximport.install()
#from . import cylib

import numpy as np
import heapq
# Actuator of an agent (incomplete) 
class Actuator:
    def __init__(self, agent):
        self.agent = agent
        self.goal = None
        self.steps = []

    #reorient and find a new goal
    def doubt(self):
        print("{} is starting to have some doubts...".format(self.agent.name))
        #check sensor inputs and create list of potential targets and weights
        targets = []
        weights = []

        for sensor in self.agent.sensors:
            if sensor.type.name == "Brain":
                continue

            ts, ws = sensor.sense(self.agent.x, self.agent.y)
            targets += ts
            weights += ws

        #nothing found => stay idle
        if len(targets) == 0:
            return

        #choose random target according to weight
        z = np.sum(weights)
        self.goal = np.random.choice(targets, p = np.asarray(weights) / z)
        self.steps = self.pathfind()
        print("{} found {}!".format(self.agent.name, self.goal.name))


    #reorient and find a new goal
    def reflect(self):
        #check sensor inputs and create list of potential targets and weights
        targets = []
        weights = []

        for sensor in self.agent.sensors:
            ts, ws = sensor.sense(self.agent.x, self.agent.y)
            targets += ts
            weights += ws

        #nothing found => stay idle
        if len(targets) == 0:
            self.goal = None
            self.steps = []
            return

        #choose random target according to weight
        z = np.sum(weights)
        self.goal = np.random.choice(targets, p = np.asarray(weights) / z)
        self.steps = self.pathfind()
        if self.goal.type == None:
            print("{} wonders what's at ({},{})...".format(self.agent.name, self.goal.x,self.goal.y))
        else:
            print("{} found {}!".format(self.agent.name, self.goal.name))

    def pathfind(self):
        dest = None
        fringe = []
        closed = set()
        pathdata = {}
        heapq.heappush(fringe,(self.estimateddistance(self.agent.x, self.agent.y),(self.agent.x, self.agent.y)))
        pathdata[(self.agent.x,self.agent.y)] = (0,None)
        while len(fringe) != 0:
            f, cell = heapq.heappop(fringe)
            closed.add(cell)
            if cell[0] == self.goal.x and cell[1] == self.goal.y:
                dest=cell
                break

            nbs = ((cell[0], cell[1]+1),\
                   (cell[0]+1, cell[1]),\
                   (cell[0]-1, cell[1]),\
                   (cell[0], cell[1]-1))

            for n in nbs:
                if self.agent.world.walkable(n[0], n[1]) == True and (n[0],n[1]) not in closed:
                    if (f,cell) in fringe:
                        continue

                    g = pathdata[cell][0] + 1
                    h = self.estimateddistance(n[0], n[1])
                    f = g + h
                    heapq.heappush(fringe,(f,n))
                    pathdata[n] = (g,cell)
            

        if dest == None:
            return []

        ret=[]
        while True:
            ret.append((dest[0],dest[1]))
            dest = pathdata[dest][1]
            if dest == None:
                break

        ret.reverse()
        return ret

    def estimateddistance(self, xcur, ycur):
        manhattan = abs(self.goal.x-xcur)+abs(self.goal.y-ycur)
        return manhattan

            
# act function. Randomly moves agent in one direction.
# receives x,y, the current coordinates of the agent
# returns new coordinates
    def propose(self, x, y):
        if self.goal == None or len(self.steps) == 0:
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
        else:   
            if self.goal.type == None:
                a = min(0, 300 - self.agent.energy) / 300.0
                if np.random.random_sample() <= a:
                    self.doubt()
            step = self.steps[0]
            x = step[0]
            y = step[1]
            self.steps = self.steps[1:]
            #We have reached our goal
            if len(self.steps) == 0:   
                self.agent.touch(self.goal)
                self.goal = None
        return (x, y)
