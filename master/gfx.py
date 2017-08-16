import pygame

images = {}

default_size = None

def load_image(name, size = None):
    if not name in images.keys():
        img = pygame.image.load('img/{}.bmp'.format(name))
        images[name] = img

    img = images[name]
    if size == (0,0):
        return img
    elif size == None:
        size = default_size
    if size != None:
        img = pygame.transform.scale(img, size)

    return img
