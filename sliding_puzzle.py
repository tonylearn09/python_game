import pygame
import sys
import random
from pygame.locals import *  # noqa

# number of columns and rows in the board
BOARDWIDTH = 4
BOARDHEIGHT = 4

TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BOARDCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT -
               (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, \
        RESET_SURF, RESET_RECT, NEW_SURF,\
        NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # store the option buttons and their rectangles in OPTIONS
    RESET_SURF, RESET_RECT = makeText('Reset',
                                      TEXTCOLOR, TILECOLOR,
                                      WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF, NEW_RECT = makeText('New Game',
                                  TEXTCOLOR, TILECOLOR,
                                  WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',
                                      TEXTCOLOR, TILECOLOR,
                                      WINDOWWIDTH - 120, WINDOWWIDTH - 90)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    # a solved board is the same as the board in the start state
    SOLVEDBOARD = getStartingBoard()
    allMoves = []  # list of moves made from the solved configuration

    while True:
        slideTo = None  # the direction
        # contains message to show in upper left corner
        msg = 'Click tile or press arrow key to slide.'
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard,
                                              event.pos[0],
                                              event.pos[1])

                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        # clicked on Reset button
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        # clicked on new game button
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                    else:
                        # check if the clicked tile was next to the blank spot
                        blankx, blanky = getBlankPosition(mainBoard)
                        if (spotx, spoty) == (blankx + 1, blanky):
                            slideTo = LEFT
                        elif (spotx, spoty) == (blankx - 1, blanky):
                            slideTo = RIGHT
                        elif (spotx, spoty) == (blanx, blanky + 1):
                            slideTo = UP
                        elif (spotx, spoty) == (blankx, blanky - 1):
                            slideTo = DOWN
                        elif event.type == KEYUP:
                            # check if the user pressed a key to slid a tile
                            if (event.key in (K_LEFT, K_a) and
                                    isValidMove(mainBoard, LEFT)):
                                slideTo = LEFT
                            elif (event.key in (K_RIGHT, K_d) and
                                  isValidMove(mainBoard, RIGHT)):
                                slideTo = RIGHT
                            elif (event.key in (K_UP, K_w) and
                                  isValidMove(mainBoard, UP)):
                                slideTo = UP
                            elif (event.key in (K_DOWN, K_s) and
                                  isValidMove(mainBoard, DOWN)):
                                slideTo = DOWN
                                if slideTo:
                                    slideAnimation(mainBoard, slideTo,
                                                   'Click tile or press'
                                                   'arrow keys to slide.',
                                                   8)  # show slide on screen
                                    makeMove(mainBoard, slideTo)
                                    # record the slide
                                    allMoves.append(slideTo)
                                    pygame.display.update()
                                    FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                terminate()
                # put the other KEYUP event objects back
                pygame.event.post(event)


def getStartingBoard():
    # Return a board data structure with tiles in the solved state
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
            board.append(column)
            counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = BLANK
    return board


def getBlankPosition(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = \
            board[blankx + 1][blanky], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = \
            board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = \
            board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = \
            board[blank - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0] - 1)) or \
            (move == DOWN and blanky != 0) or \
            (move == LEFT and blankx != len(board) - 1) or \
            (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
        if lastMove == DOWN or not isValidMove(board, UP):
            validMoves.remove(UP)
            if lastMove == LEFT or not isValidMove(board, RIGHT):
                validMoves.remove(RIGHT)
                if lastMove == RIGHT or not isValidMove(board, LEFT):
                    validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)

def 

