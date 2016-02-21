import pygame, sys
from pygame.locals import *

pygame.init()

# Set up the fpsClock object to control the pause time for animation
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# Set up window
# flags = 0, and depth = 32, which indicate it use 32 bit for color
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption("Animation")

# Loading and playing background music:
pygame.mixer.music.load("Green-fields.mp3")
pygame.mixer.music.play(-1, 0.0) # play forever and start from the begining of the song


WHITE = (255, 255, 255)
# Load the image in
catImg = pygame.image.load("cat.png")

# Set initial condion for class image for later animation
catx = 10
caty = 10
direction = "right"

while True:
    DISPLAYSURF.fill(WHITE)

    if direction == "right":
        catx += 5
        if catx == 200:
            direction = "down"
    elif direction == "down":
        caty += 5
        if caty == 220:
            direction = "left"
    elif direction == "left":
        catx -= 5
        if catx == 10:
            direction = "up"
    else: # direction is "up"
       caty -= 5
       if caty == 10:
           direction = "right"

    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
