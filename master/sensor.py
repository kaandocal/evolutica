class Sensor():
    def __init__(self, resolution = 0):
        self.resolution  = resolution

    #return list of elements perceived, weighted by perception strength
    def sense(self, world, pos):
        pass

class Smell():
    def __init__(self, resolution = 0):
        Sensor.__init__(self, resolution)

    def sense(self, world, x, y):
        entities = world.entities
        targets = []
        weights = []
        #(filter out odourless entities)
        for ent in entities:
            dist = np.sqrt((x - ent.x) ** 2 + (y - ent.y) ** 2)
            #strength of smell is dependent on the distance and the resolution of the sensor
            strength = self.resolution - dist
            if strengh >= 1:
                targets.append(ent)
                weights.append(np.floor(strength))

        return targets, weights


