import numpy as np
import heapq
# Actuator of an agent (incomplete) 
class Actuator:
    def __init__(self, agent):
        self.agent = agent
        self.goal = None
        self.steps = []

    #reorient and find a new goal
    def reflect(self):
        #check sensor inputs and create list of potential targets and weights
        targets = []
        weights = []

        for sensor in self.agent.sensors:
            ts, ws = sensor.sense(self.agent.world, self.agent.x, self.agent.y)
            targets += ts
            weights += ws

        #nothing found => stay idle
        if len(targets) == 0:
            self.goal = None
            self.steps = []
            return

        return
        #choose random target according to weight
        z = np.sum(weights)
        self.goal = np.random.choice(targets, p = np.asarray(weights) / z)

    def pathfind(self):
        dest= None
        fringe= []
        closed= []
        heapq.heappush(fringe,(self.estimateddistance(self.x, self.y),(self.x, self.y, 0, None)))
        while len(fringe)!=0:
            f, cell = heapq.heappop(fringe)
            closed.append((cell[0],cell[1]))
            if cell[0] == self.goal.x and cell[1] == self.goal.y:
                dest=cell
                break

            nbs= ((cell[0], cell[1]+1,cell[2]+1,cell),(cell[0]+1, cell[1],cell[2]+1,cell),(cell[0]-1, cell[1],cell[2]+1,cell),(cell[0], cell[1]-1,cell[2]+1,cell))
            for n in nbs:

                if self.agent.world.walkable(n[0], n[1]) == True and (n[0],n[1]) not in closed:
                    f=n[2]+estimateddistance(n[0], n[1])
                    heapq.heappush(fringe,(f,n))
            

        if dest == None:
            return None

        ret=[]
        while True:
            ret.append((dest[0],dest[1]))
            dest= dest[3]
            if dest== None:
                break
        return ret.reverse()


    def estimateddistance(self, xcur, ycur):
        manhattan=abs(self.goal.x-xcur)+abs(self.goal.y-ycur)
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
            step = self.steps[0]
            x = step[0]
            y = step[1]
            self.steps = self.steps[1:]
            #We have reached our goal
            if len(self.steps) == 0:   
                self.agent.touch(self.goal)
                self.goal = None
        return (x, y)
