import master.world
import master.food
import master.sensor
import matplotlib.pyplot as plt
import pickle
import sys

filename = sys.argv[1]

inp = open(filename, "rb")
world = pickle.load(inp)

living = []
extinct = []
multiplied = []

for ent in world.halloffame:
    if not ent.deceased:
        living.append(ent)
    elif len(ent.children) == 0:
        extinct.append(ent)
    else:
        multiplied.append(ent)

print("{} living, {} extinct, {} passed on their genes".format(len(living),len(extinct),len(multiplied)))

def descendants(ent):
    return sum([1 + descendants(c) for c in ent.children])

def hunger_sort(ent):
    return sum([ ent.food_eaten[k] for k in master.food.foodtypes ])

def life_sort(ent):
    return ent.deceased - ent.birthday

def sensorstrength(ent, st):
    ret = 0
    for s in ent.sensors:
        if s.type == st:
            ret += s.resolution

    return ret

living_s = sorted(living, key=hunger_sort)
for ent in living_s:
    ent.dumpbio()
    ent.dumpsensors()

extinct_s = sorted(extinct, key=life_sort)
for ent in extinct_s:
    ent.dumpbio()
    ent.dumpsensors()


multiplied_s = sorted(multiplied, key=descendants)
for ent in multiplied_s:
    ent.dumpbio()
    ent.dumpsensors()

for st in master.sensor.sensortypes:
    fig = plt.figure()
    fig.suptitle(st.name)
    ax = plt.subplot()

    xlist = [ sensorstrength(ent, st) for ent in multiplied ]
    ylist = [ descendants(ent) for ent in multiplied ]

    ax.scatter(xlist, ylist)
    ax.set_ylabel("Number of descendants")
    ax.set_xlabel("Sensor strength")

plt.show()
