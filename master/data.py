from .world import World
from .agent import Agent
import pickle

def dump(self):
    i = 0
    while True:
        filename = "saves/save{}".format(i)
        try:
            out = open(filename, "rb")
        except IOError:
            break
        i += 1

    out = open(filename, "wb")
    pickle.dump(self, out)
    print("Saved game data to file '{}'".format(filename))

def foodinfo(world):
    for ent in world.entities:
        if ent.type == Agent:
            ent.dumpfood()

def sensorinfo(world):
    for ent in world.entities:
        if ent.type == Agent:
                ent.dumpsensors()

def hof(world):
    for ent in world.halloffame:
        ent.dumpbio()

