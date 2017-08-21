import pygame

images = {}

default_size = None

# Since pygame images cannot be pickled, this returns a handle to the image loaded
def load_image(name, size = None):
    if not name in images.keys():
        img = pygame.image.load('img/{}.bmp'.format(name))
        images[name] = img

    return (name, size)

# Returns the actual image
def get_image(t):
    img = images[t[0]]
    size = t[1]
    if size == (0,0):
        return img
    elif size == None:
        size = default_size
    if size != None:
        img = pygame.transform.scale(img, size)

    return img
