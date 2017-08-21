import numpy as np
import heapq
# Actuator of an agent (incomplete) 
class Actuator:
    def __init__(self, agent):
        self.agent = agent
        self.goal = None
        self.steps = []


    # reorient and find a new goal
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


    # As reflect, but ignores any inputs by the brain
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

    # Implementation of the A* pathfinding algorithm
    def pathfind(self):
        dest = None
        fringe = []
        closed = set()
        # Save the cost and the shortest route to each cell in a dictionary
        pathdata = {}
        world_w = self.agent.world.width
        world_h = self.agent.world.height

        # Start with the current cell
        heapq.heappush(fringe,(self.estimateddistance(self.agent.x, self.agent.y),(self.agent.x, self.agent.y)))
        pathdata[(self.agent.x,self.agent.y)] = (0,None)

        while len(fringe) != 0:
            # Check the best-looking cell in the set of unvisited tiles
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
                # Consider adding n to the list of cells to be visited
                if (n[0] >= 0 and n[0] < world_w) and (n[1] >= 0 and n[1] < world_h) and self.agent.world.tiles[n[0],n[1]] == 0 and (n[0],n[1]) not in closed:
                    if (f,cell) in fringe:
                        continue

                    g = pathdata[cell][0] + 1
                    h = self.estimateddistance(n[0], n[1])
                    f = g + h

                    heapq.heappush(fringe,(f,n))
                    pathdata[n] = (g,cell)
            

        if dest == None:
            return []

        # Recursively fill the list with the ancestors of the cell
        ret=[]
        while True:
            ret.append((dest[0],dest[1]))
            dest = pathdata[dest][1]
            if dest == None:
                break

        ret.reverse()
        return ret

    # Heuristic for the A* algorithm
    def estimateddistance(self, xcur, ycur):
        manhattan = abs(self.goal.x-xcur)+abs(self.goal.y-ycur)
        return manhattan

            
# Proposal function. Returns tuple of the next position.
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
            # Consider reorienting the agent if it is just wandering about
            if self.goal.type == None:
                a = min(0, 500 - self.agent.energy) / 400.0
                if np.random.random_sample() <= a:
                    self.doubt()

            # Perform the next step in the list of steps
            step = self.steps[0]
            x = step[0]
            y = step[1]
            self.steps = self.steps[1:]
            # We have reached our goal
            if len(self.steps) == 0:   
                self.agent.touch(self.goal)
                self.goal = None

        return (x, y)
