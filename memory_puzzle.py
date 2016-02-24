import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height and width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BROADWIDTH = 10 # number of columns of icons
BROADHEIGHT = 7 # number of rows of icons

assert (BROADWIDTH * BROADHEIGHT) % 2 == 0, 'Board needs to have an even nummber of boxes ' + \
                                           'for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BROADWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BROADHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHPAES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALLCOLORS) * len(ALLSHPAES) * 2 >= BROADWIDTH * BROADHEIGHT, 'Board is too big' + \
        ' for the numbers of color/shape difined' 

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Memory Game')

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event

    main_board = getRandomizedBoard()
    revealed_boxes = generateRevealedBoxesData(False)

    first_selection = None # store the (x, y) of the first box clicked.

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(main_board)

    while True:
        mouse_clicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(main_board, revealed_boxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouse_clicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box
            if not revealed_boxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy) # Draw a blue highlight around the box to let user know he/she has select
            if not revealed_boxes[boxx][boxy] and mouse_clicked:
                revealBoxAnimation(main_board, [(boxx, boxy)])
                revealed_boxes[boxx][boxy] = True # set the box as "revealed"
                if first_selection == None: # The current box was the first box clicked
                    first_selection = (boxx, boxy)
                else: # The current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(main_board, first_selection[0], first_selection[1])
                    icon2shape, icon2color = getShapeAndColor(main_board, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both sections
                        pygame.time.wait(1000) # 1000ms = 1s
                        coverBoxAnimation(main_board, [(first_selection[0], first_selection[1]), (boxx, boxy)])
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[boxx][boxy] = False

                    elif hasWon(revealed_boxes): # check if all pairs found
                        gameWonAnimation(main_board)
                        pygame.time.wait(2000)

                        # Reset the board
                        main_board = getRandomizedBoard()
                        revealed_boxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(main_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation
                        startGameAnimation(main_board)
                    first_selection = None # Reset firstselection variable

        # Redraw the screen and wait a clock tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateRevealedBoxesData(val):
    revealed_boxes = []
    for i in range(BROADWIDTH):
        revealed_boxes.append([val] * BROADHEIGHT)
    return revealed_boxes

def getRandomizedBoard():
    # Get a list of every possible shape in every possible color
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHPAES:
            icons.append((shape, color))

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BROADWIDTH * BROADHEIGHT / 2) # Calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each icon
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons
    board = []
    for x in range(BROADWIDTH):
        column = []
        for y in range(BROADHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board

def getBoxAtPixel(x, y):
    for boxx in range(BROADWIDTH):
        for boxy in range(BROADHEIGHT):
            left, top = leftTopCoordsofBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def leftTopCoordsofBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half = int(BOXSIZE * 0.5) # syntactic sugar

    left, top = leftTopCoordsofBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shape
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, 
                (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, 
        ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter,BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/reavealed. "boxes" is a list
    # of two-item lists, which have the x and y position
    for box in boxes:
        left, top = leftTopCoordsofBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    # This function do not call in main while loop, so need to update itself
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxAnimation(board, boxesToReveal):
    # Do the "box reveal" animation
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxAnimation(board, boxesToCover):
    # Do the "box cover" animation
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    # Draw all of the boxes in their covered or revealed state
    for boxx in range(BROADWIDTH):
        for boxy in range(BROADHEIGHT):
            left, top = leftTopCoordsofBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsofBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def startGameAnimation(board):
    # randomly reveal the boxes 8 at a time
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BROADWIDTH):
        for y in range(BROADHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxAnimation(board, boxGroup)
        coverBoxAnimation(board, boxGroup)

def splitIntoGroupOf(groupSize, theList):
    # splits a list into list of lists, where the inner lists have 
    # at most groupSize number of items
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered
    return True

if __name__ == '__main__':
    main()
