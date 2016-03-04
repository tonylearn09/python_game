import pygame
import sys
from pygame.locals import *  # noqa

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Hello world program")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHTBLUE = (0, 0, 128)

# Call the constructor to create font object to use
# This pass the font file(freesansbold.ttf came with pygame)
# And the size of the font
fontObj = pygame.font.Font("freesansbold.ttf", 32)
# Create the words and draw it on a surface object
# Parameter to render: texts to write, anti-aliasing or not,
#                      text color, background(leave out if transparent)
textSurfaceObj = fontObj.render("Hello world", True, GREEN, LIGHTBLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)


while True:  # main game loop for event handling
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
