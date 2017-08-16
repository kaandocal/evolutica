import heapq
cimport numpy as np

cdef int estimateddistance(act, int xcur, int ycur):
    cdef int manhattan = abs(act.goal.x-xcur)+abs(act.goal.y-ycur)
    return manhattan

def pathfind(act):
    dest = None
    fringe = []
    closed = set()
    pathdata = {}
    cdef int world_w = act.agent.world.width
    cdef int world_h = act.agent.world.height
    cdef np.ndarray[unsigned int,ndim=2] tiles = act.agent.world.tiles

    heapq.heappush(fringe,(estimateddistance(act, act.agent.x, act.agent.y),(act.agent.x, act.agent.y)))
    pathdata[(act.agent.x,act.agent.y)] = (0,None)
    while len(fringe) != 0:
        f, cell = heapq.heappop(fringe)
        closed.add(cell)
        if cell[0] == act.goal.x and cell[1] == act.goal.y:
            dest=cell
            break

        nbs = ((cell[0], cell[1]+1),\
               (cell[0]+1, cell[1]),\
               (cell[0]-1, cell[1]),\
               (cell[0], cell[1]-1))

        for n in nbs:
            if (n[0] >= 0 and n[0] < world_w) and (n[1] >= 0 and n[1] < world_h) and tiles[n[0],n[1]] == 0 and (n[0],n[1]) not in closed:
                if (f,cell) in fringe:
                    continue

                g = pathdata[cell][0] + 1
                h = estimateddistance(act, n[0], n[1])
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


