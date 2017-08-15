from .world import World
from .agent import Agent
import pickle

def dump(self):
    return
    i = 0
    while True:
        filename = "saves/save{}".format(i)
        try:
            out = file(filename, "rb")
        except IOError:
            break
        i += 1

    out = file(filename, "wb")
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
        if ent.deceased:
            print("--------------------------------------")
            print("Fondly remembering {}".format(ent.name))
            print("(Round {} - Round {})".format(ent.birthday, ent.deceased))
            if len(ent.children) != 0:
                print("{} gave us two beautiful children: {} and {}".format(ent.name, ent.children[0].name, ent.children[1].name))
            else:
                print("Poor {} starved to death in a cruel world...".format(ent.name))

            print("--------------------------------------")
        else:
            print("--------------------------------------")
            print("Proudly presenting {}".format(ent.name))
            print("Born in Round {}".format(ent.birthday))
            print("We all wish the best for {}".format(ent.name))
            print("--------------------------------------")
