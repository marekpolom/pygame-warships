import pygame, sys, random, time
from threading import Timer
from random import randrange
from pygame.locals import *

def shipsCount(fB, f):
    j = 0
    x = list(f)
    x.reverse()
    ships = 0

    for i in fB:
        a = i*x[j]
        j+=1
        ships += a
    
    return ships

#variables !!don't change without permission, pls!!
boardWidth = 1280
boardHeight = 720
FPS = 60
sizeOfBox = 50
sizeOfGap = 2
boardSize = 10
pBMarginX = 658
pBMarginY = 99
leftBarMargin = 50
leftBarWidth = 558
pWH = 458
mBeforeButton = 15

leftPlayerBoardBox = 44
leftPlayerBoardGap = 1

gameFeedH = 135

pBoardWH = (boardSize*sizeOfBox) + ((boardSize+1)*sizeOfGap)

#fleet variables (also don't change)
fleetBSize = {
    "w": 226,
    "h": 45,
    "bM": 6,
    "bIM": 2
}

five = 1
four = 1
three = 2
two = 2
one = 2

buttonText = {
    1: "x statek 1-masztowy",
    2: "x statek 2-masztowy",
    3: "x statek 3-masztowy",
    4: "x statek 4-masztowy",
    5: "x statek 5-masztowy"
}

fleet = (five, four, three, two, one)

#stores information about ships 
fleetShipTypes = []

#keeps track of how many ships of certain type are in play
howMuchShips = []

#stores information about blocked boxes
bBArray = []

for i in range(len(fleet)):  
    fleetShipTypes.append(i+1)
    howMuchShips.append(0)

gameStatus = "menu"

playerShipsLeft = shipsCount(fleetShipTypes, fleet)

shotShips = ["p", "t", "n"]

dif = "hard"

#menu button properties
menuButtons = ("PLAY", "SCOREBOARD", "EXIT")

menuButtonW = 400
menuButtonH = 90
menuButtonM = 25
menuButtonB = 3

menuTMargin = 30
menuBetweenM = 80

#end game button properties
eGameButtons = ("REPLAY", "MENU")

eGameButtonW = 400
eGameButtonH = 90
eGameButtonM = 25
eGameButtonB = 3

eGameTMargin = 60
eGameBetweenM = 100

#end game button properties
difButtons = ("EASY", "NORMAL", "HARD")

difButtonW = 350
difButtonH = 70
difButtonM = 15

difTMargin = 100
difBetweenM = 160

#ok you can change that atleast
#COLOR    R    G    B    A
black = (  0,   0,   0)
red =   (219,  39,  39)
redH =  (240,  62,  62)
redES = (145,  28,  28)
blue =  (134, 192, 240)
lBule = (150, 205, 250)
sBlue = (130, 173, 209)
dBlue =  ( 36, 134, 214)
green = ( 70, 176,  72)
greenH =( 88, 184,  90)
yellow =(227, 202,  64)
yellowH =(235, 212,  89)
gray =  ( 46,  46,  46)
lgrayH =(133, 133, 133)
lgray = (107, 107, 107)
white = (255, 255, 255)
endBg = (  0,   0,   0, 150)
difBg = (  0,   0,   0, 180)

feedLength = 5

class pBox:
    def __init__(self, startX, startY, k, click = False):
        self.x = startX
        self.y = startY
        self.kind = k
        self.clicked = click

class fBPic:
    def __init__(self, startX, startY, size, click = False):
        self.x = startX
        self.y = startY
        self.size = size
        self.clicked = click


def main():
    # global fpsClock, displaySurf
    global gameStatus
    global howMuchShips
    global bBArray
    global fleetShipTypes
    global dif

    gameFeed = []
    
    isClicked = False
    pWNext = []
    
    nCount = True
    canHe = False

    fBT = list(fleet)
    fBT.reverse()

    pygame.init()

    fpsClock = pygame.time.Clock()
    displaySurf = pygame.display.set_mode((boardWidth, boardHeight))

    mouseX = 0
    mouseY = 0
    pygame.display.set_caption("WarShips Game")
    enemyBoard = generateEnemyBoard()

    playerBoard = generateBlankBoard(boardSize)
    displaySurf.fill(blue)

    fleetButton = 0

    pSLeft = playerShipsLeft
    eSLeft = 0

    boxes = []

    menuButtonsArray = menu(displaySurf, menuButtons)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE and gameStatus != "menu":
                    gameStatus = "menu"

                    howMuchShips = []

                    bBArray = []

                    for i in range(len(fleet)):  
                        howMuchShips.append(0)

                    isClicked = False
                    pWNext = []
                    
                    nCount = True
                    canHe = False

                    fBT = list(fleet)
                    fBT.reverse()

                    enemyBoard = generateEnemyBoard()

                    playerBoard = generateBlankBoard(boardSize)
                    displaySurf.fill(blue)

                    fleetButton = 0

                    pSLeft = playerShipsLeft
                    eSLeft = 0

                    boxes = []

                    menuButtonsArray = menu(displaySurf, menuButtons)
                elif event.key == K_ESCAPE and gameStatus == "menu":
                    pygame.quit()
                    sys.exit()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()

        #game menu
        if gameStatus == "menu":
            menuButtonsHover(displaySurf, menuButtonsArray, mouse)

            #if player clicks in menu
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and isClicked == False:
                menuClick = menuButtonsClick(menuButtonsArray, mouse)

                if menuClick == "PLAY":
                    gameStatus = "difficulty"
                    
                    displaySurf.fill(blue)
                    difB = difScreen(displaySurf, boardWidth, boardHeight)

                elif menuClick == "SCOREBOARD":
                    gameStatus = "scoreBoard"
                    scoreboard(displaySurf)
                
                elif menuClick == "EXIT":
                    pygame.quit()
                    sys.exit()

                isClicked = True
            elif event.type == MOUSEBUTTONUP and isClicked == True:
                isClicked = False

        #player chooses difficulty (easy/normal/hard)
        elif gameStatus == "difficulty":
            points = 0
            eGameButtonsHover(displaySurf, difB, mouse, 50, difBetweenM, difButtonW, difButtonH, True)

            #if player clicks in end game screen
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and isClicked == False:
                eGameClick = eGameButtonsClick(difB, mouse, difButtonW, difButtonH)
                gameFeed = []

                if eGameClick == "EASY":
                    dif = "easy"

                    gameStatus = "shipPlacement"

                    displaySurf.fill(blue)

                    displayPlayerBoard(playerBoard, boardSize, sizeOfBox, sizeOfGap, pBMarginX, pBMarginY, displaySurf)
                    fleetB = leftBar(displaySurf, leftBarWidth, boardHeight, leftBarMargin, pWH, mBeforeButton)
                elif eGameClick == "NORMAL":
                    dif = "normal"

                    gameStatus = "shipPlacement"

                    displaySurf.fill(blue)

                    displayPlayerBoard(playerBoard, boardSize, sizeOfBox, sizeOfGap, pBMarginX, pBMarginY, displaySurf)
                    fleetB = leftBar(displaySurf, leftBarWidth, boardHeight, leftBarMargin, pWH, mBeforeButton)
                elif eGameClick == "HARD":
                    dif = "hard"

                    gameStatus = "shipPlacement"

                    displaySurf.fill(blue)

                    displayPlayerBoard(playerBoard, boardSize, sizeOfBox, sizeOfGap, pBMarginX, pBMarginY, displaySurf)
                    fleetB = leftBar(displaySurf, leftBarWidth, boardHeight, leftBarMargin, pWH, mBeforeButton)

                isClicked = True
            elif event.type == MOUSEBUTTONUP and isClicked == True:
                isClicked = False

            

        #player picks where he wants his ships to be placed
        elif gameStatus == "shipPlacement":

            # startButtonPos = displayStartButton(displaySurf, pBMarginX, boardSize, sizeOfGap, sizeOfBox)

            fleetButtons(displaySurf, fleetB, mouse)
            fleetButtonsPic(displaySurf, fleetShipTypes, fleetB, fleetBSize, fBT)
            
            playerBoardHover(playerBoard, displaySurf, mouse, sizeOfBox, gameStatus, fleetShipTypes, pWNext)

            if canHe:
                startButtonPos = displayStartButton(displaySurf, pBMarginX, boardSize, sizeOfGap, sizeOfBox)

            # print(mouse)
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and isClicked == False:

                #if player clicks on board
                if pBMarginX+pBoardWH > mouse[0] >= pBMarginX and pBMarginY+pBoardWH > mouse[1] >= pBMarginY:

                    playerBoardClick(playerBoard, displaySurf, mouse, sizeOfBox, fleetButton, pWNext, nCount)

                    bBArray = blockedBoxes(playerBoard, fleetShipTypes)
                    fBT = displayBlockade(playerBoard, bBArray, fleet)

                    pWNext = playerWhereNext(playerBoard, fleetButton, fleetShipTypes)

                    nCount = neighbourCount(bBArray, fleetButton)

                    canHe = canPFSAFGFFS(bBArray, fleetShipTypes)
                    
                #if player clicks on fleet buttons
                elif leftBarWidth > mouse[0] >= 0 and boardHeight > mouse[1] >= 0:
                    fleetButton = fleetButtonsClickable(fleetB, mouse, fleetBSize["w"], fleetBSize["h"], fleetButton)
                    pWNext = playerWhereNext(playerBoard, fleetButton, fleetShipTypes)
                
                #if player clicks on start button that shows up when he fills his board with ships
                elif canHe:
                    if startButtonPos[0]+startButtonPos[2] > mouse[0] >= startButtonPos[0] and startButtonPos[1]+startButtonPos[3] > mouse[1] >= startButtonPos[1]:
                        gameStatus = "start"

                        timePassed = pygame.time.get_ticks()

                        displaySurf.fill(blue)
                        pygame.draw.rect(displaySurf, black, (pBMarginX, pBMarginY, pBoardWH, pBoardWH))

                        leftBar(displaySurf, leftBarWidth, boardHeight, leftBarMargin, pWH, mBeforeButton, playerBoard)
                        displayLeftPlayerBoard(playerBoard, displaySurf, leftPlayerBoardBox, shotShips)

                        enemyBoardPlayer = generateBlankBoard(boardSize)
                        displayPlayerBoard(enemyBoardPlayer, boardSize, sizeOfBox, sizeOfGap, pBMarginX, pBMarginY, displaySurf)

                        eTurn = coinToss()
                        feedUpdate = True

                        if eTurn:
                            pSLeft, boxes, eTrun, cords, mType = enemyTurn(playerBoard, pSLeft, [], dif)
                            eTurn = False
                        
                            gameFeed = createMessage(True, cords, mType, gameFeed)

                            # if feedUpdate:
                            #     feedUpdate = False
                            #     message = "Enemy is thinking"

                            #     gameFeed = feedAdd(gameFeed, message)

                            # thinking = Timer(3, botThinkingLol(playerBoard, displaySurf, leftPlayerBoardBox, shotShips, eTurn, cords, mType, gameFeed))
                            # eTurn, FeedUpdate, gameFeed = thinking.start()

                            displayLeftPlayerBoard(playerBoard, displaySurf, leftPlayerBoardBox, shotShips)

                isClicked = True
            elif event.type == MOUSEBUTTONUP and isClicked == True:
                isClicked = False

        #game starts
        elif gameStatus == "start":

            currentTime = pygame.time.get_ticks() - timePassed

            displayTimer(displaySurf, currentTime)
            
            playerBoardHover(enemyBoardPlayer, displaySurf, mouse, sizeOfBox, gameStatus)
            feedRead(displaySurf, gameFeed)

            if event.type == MOUSEBUTTONDOWN and event.button == 1 and isClicked == False:
                #if player clicks on board
                if pBMarginX+pBoardWH > mouse[0] >= pBMarginX and pBMarginY+pBoardWH > mouse[1] >= pBMarginY:
                    if not eTurn:
                        eTurn, eSLeft, cords, mType, points = playerBoardClick(enemyBoardPlayer, displaySurf, mouse, sizeOfBox, 0, pWNext, nCount, gameStatus, enemyBoard, eSLeft, points, dif)
                        
                        if eTurn and mType == "z":
                            gameFeed = createMessage(False, cords, mType, gameFeed)

                        if eSLeft == playerShipsLeft:
                            eTurn = False
                            playerBoardHover(enemyBoardPlayer, displaySurf, mouse, sizeOfBox, gameStatus)
                            feedRead(displaySurf, gameFeed)
                            eGameB = gameEnd(displaySurf, boardWidth, boardHeight, True)
                            finalScore(displaySurf, points, currentTime, True)
                            gameStatus = "gameEnd"

                    
                    if eTurn:
                        pSLeft, boxes, eTurn, cords, mType = enemyTurn(playerBoard, pSLeft, boxes, dif)
                        feedUpdate = True

                        gameFeed = createMessage(True, cords, mType, gameFeed)

                        # if feedUpdate:
                        #     feedUpdate = False
                        #     message = "Enemy is thinking"

                        #     gameFeed = feedAdd(gameFeed, message)

                        # thinking = Timer(3, botThinkingLol(playerBoard, displaySurf, leftPlayerBoardBox, shotShips, eTurn, cords, mType, gFeed))
                        # eTurn, FeedUpdate, gameFeed = thinking.start()

                        displayLeftPlayerBoard(playerBoard, displaySurf, leftPlayerBoardBox, shotShips)

                        if pSLeft == 0:
                            eGameB = gameEnd(displaySurf, boardWidth, boardHeight, False)
                            finalScore(displaySurf, points, currentTime, False)
                            gameStatus = "gameEnd"

                isClicked = True
            elif event.type == MOUSEBUTTONUP and isClicked == True:
                isClicked = False
        elif gameStatus == "gameEnd":
            eGameButtonsHover(displaySurf, eGameB, mouse)

            #if player clicks in end game screen
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and isClicked == False:
                eGameClick = eGameButtonsClick(eGameB, mouse)

                if eGameClick == "MENU":
                    gameStatus = "menu"

                    howMuchShips = []

                    bBArray = []

                    for i in range(len(fleet)):  
                        howMuchShips.append(0)

                    isClicked = False
                    pWNext = []
                    
                    nCount = True
                    canHe = False

                    fBT = list(fleet)
                    fBT.reverse()

                    enemyBoard = generateEnemyBoard()

                    playerBoard = generateBlankBoard(boardSize)
                    displaySurf.fill(blue)

                    fleetButton = 0

                    pSLeft = playerShipsLeft
                    eSLeft = 0

                    boxes = []

                    menuButtonsArray = menu(displaySurf, menuButtons)

                elif eGameClick == "REPLAY":
                    gameStatus = "difficulty"

                    displaySurf.fill(blue)
                    difB = difScreen(displaySurf, boardWidth, boardHeight)

                    howMuchShips = []

                    bBArray = []

                    for i in range(len(fleet)):  
                        howMuchShips.append(0)

                    isClicked = False
                    pWNext = []
                    
                    nCount = True
                    canHe = False

                    fBT = list(fleet)
                    fBT.reverse()

                    enemyBoard = generateEnemyBoard()

                    playerBoard = generateBlankBoard(boardSize)

                    fleetButton = 0

                    pSLeft = playerShipsLeft
                    eSLeft = 0

                    boxes = []

                    menuButtonsArray = menu(displaySurf, menuButtons)

                isClicked = True
            elif event.type == MOUSEBUTTONUP and isClicked == True:
                isClicked = False

        elif gameStatus == "scoreBoard":
            scoreBButton(displaySurf, mouse)

            if event.type == MOUSEBUTTONDOWN and event.button == 1 and isClicked == False:
                #if player clicks on button
                if int(boardWidth/2) - 150 < mouse[0] <  int(boardWidth/2) - 150 + 300 and 586+35 < mouse[1] < 586+35+70:
                    gameStatus = "menu"

                    howMuchShips = []

                    bBArray = []

                    for i in range(len(fleet)):  
                        howMuchShips.append(0)

                    isClicked = False
                    pWNext = []
                    
                    nCount = True
                    canHe = False

                    fBT = list(fleet)
                    fBT.reverse()

                    enemyBoard = generateEnemyBoard()

                    playerBoard = generateBlankBoard(boardSize)
                    displaySurf.fill(blue)

                    fleetButton = 0

                    pSLeft = playerShipsLeft
                    eSLeft = 0

                    boxes = []

                    menuButtonsArray = menu(displaySurf, menuButtons)
                isClicked = True
            elif event.type == MOUSEBUTTONUP and isClicked == True:
                isClicked = False

        pygame.display.update()

#generates random arrangement of enemy ships on board
def generateEnemyBoard():
    enemyBoard = []

    #generates blank board
    for i in range(boardSize):
        t = []
        for j in range(boardSize):
            t.append("w")
        enemyBoard.append(t)

    shipType = len(fleet)

    #generates ships on board
    for i in fleet:
        for j in range(i*shipType):
            if j%shipType == 0:
                enemyBoard = notHere(enemyBoard)
                where = []
                r = False
                
                while not r:
                    ship = (random.randint(0, boardSize-1), random.randint(0, boardSize-1))

                    if enemyBoard[ship[0]][ship[1]] == "w":
                        r = True
                        enemyBoard[ship[0]][ship[1]] = "s"

                        where = whereNext(enemyBoard, ship[0], ship[1], where)
                        enemyBoard = where[0]
                        where = where[1]
            else:
                if len(where) == 1:
                    ship = 0
                else:
                    try:
                        ship = random.randint(0, len(where)-1)
                    except ValueError:
                        return generateEnemyBoard()

                x = where[ship][0]
                y = where[ship][1]
                enemyBoard[x][y] = "s"
                where.remove((x, y))

                if j%shipType != 1:
                    where = whereNotNext(enemyBoard, x, y, where)

                where = whereNext(enemyBoard, x, y, where)
                enemyBoard = where[0]
                where = where[1]
        enemyBoard = notHere(enemyBoard)
        shipType -= 1

    return enemyBoard

#checks where the next element of a ship can be placed
def whereNext(board, x, y, where):

    #up
    if x-1 >= 0:
        if board[x-1][y] == "w":
            board[x-1][y] = "+"
            where.append((x-1, y))
        elif board[x-1][y] == "+":
            board[x-1][y] = "-"
            where.remove((x-1, y))
    #right
    if y+1 < len(board[x]):
        if board[x][y+1] == "w":
            board[x][y+1] = "+"
            where.append((x, y+1))
        elif board[x][y+1] == "+":
            board[x][y+1] = "-"
            where.remove((x, y+1))
    #down
    if x+1 < len(board):
        if board[x+1][y] == "w":
            board[x+1][y] = "+"
            where.append((x+1, y))
        elif board[x+1][y] == "+":
            board[x+1][y] = "-"
            where.remove((x+1, y))
    #left
    if y-1 >= 0:
        if board[x][y-1] == "w":
            board[x][y-1] = "+"
            where.append((x, y-1))
        elif board[x][y-1] == "+":
            board[x][y-1] = "-"
            where.remove((x, y-1))

    return board, where

#marks where the new ship can't be placed
def notHere(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "s":
                #up
                if i-1 >= 0:
                    if board[i-1][j] == "+" or board[i-1][j] == "-":
                        board[i-1][j] = "o"
                #upper right
                if i-1 >= 0 and j+1 < len(board):
                    if board[i-1][j+1] == "w":
                        board[i-1][j+1] = "o"
                #right
                if j+1 < len(board):
                    if board[i][j+1] == "+" or board[i][j+1] == "-":
                        board[i][j+1] = "o"
                #lower right
                if i+1 < len(board) and j+1 < len(board):
                    if board[i+1][j+1] == "w":
                        board[i+1][j+1] = "o"
                #down
                if i+1 < len(board):
                    if board[i+1][j] == "+" or board[i+1][j] == "-":
                        board[i+1][j] = "o"
                #lower left
                if i+1 < len(board) and j-1 >= 0:
                    if board[i+1][j-1] == "w":
                        board[i+1][j-1] = "o"
                #left
                if j-1 >= 0:
                    if board[i][j-1] == "+" or board[i][j-1] == "-":
                        board[i][j-1] = "o"
                #upper left
                if i-1 >= 0 and j-1 >= 0:
                    if board[i-1][j-1] == "w":
                        board[i-1][j-1] = "o"

    return board

#corrects next ship's element placement
def whereNotNext(board, x, y, where):
    #up
    if x-1 >= 0:
        if board[x-1][y] == "s":
            x-=1
            where = whereNext(board, x, y, where)
            return where[1]
    #right
    if y+1 < len(board[x]):
        if board[x][y+1] == "s":
            y+=1
            where = whereNext(board, x, y, where)
            return where[1]
    #down
    if x+1 < len(board):
        if board[x+1][y] == "s":
            x+=1
            where = whereNext(board, x, y, where)
            return where[1]
    #left
    if y-1 >= 0:
        if board[x][y-1] == "s":
            y-=1
            where = whereNext(board, x, y, where)
            return where[1]

#generates player board (array)
def generateBlankBoard(boardSize):
    board = []

    for i in range(boardSize):
        t = []
        for j in range(boardSize):
            t.append(pBox(0, 0, "w"))
        board.append(t)

    return board

#displays player board
def displayPlayerBoard(board, bSize, box, gap, marginX, marginY, surf):

    wh = (bSize*box) + ((bSize+1)*gap)

    pygame.draw.rect(surf, black, (marginX, marginY, wh, wh))

    x = 0
    for i in board:
        y = 0
        for j in i:
            color = lgray

            j.x = marginX+gap+x
            j.y = marginY+gap+y
            y += (box+gap)
        x += (box+gap)

#changes x and y values of player board boxes
def positionLeftPlayerBoard(board, bSize, box, gap, marginX, marginY, surf):
    wh = (bSize*box)+((bSize+1)*gap)
    c = pWH - wh

    cY = int(c/2)
    cX = int(c - cY)

    u = int(cY/2)
    r = int(cX/2)
    d = int(cY - u)
    l = int(cX - r)

    pygame.draw.rect(surf, black, (marginX, marginY, wh+c, wh+c))

    x = 0
    for i in board:
        y = 0
        for j in i:         
            j.x = marginX+r+u+gap+x
            j.y = marginY+r+u+gap+y
            
            y+= box+gap
        x += box+gap

#displays player board inside left bar
def displayLeftPlayerBoard(board,  surf, box, t, fB = fleetShipTypes):
    for i in board:
        for j in i:
            if j.kind in fB:
                color = red
            elif j.kind in t:
                if j.kind == "t":
                    color = redES
                elif j.kind == "p":
                    color = lgrayH
                elif j.kind == "n":
                    color = lgray
            else:
                color = lgray
        
            pygame.draw.rect(surf, color, (j.x, j.y, box, box))

#change button color on hover
def playerBoardHover(board, surf, mouse, box, gStatus, fB = [], pWNext = []):
    for i in board:
        for j in i:
            if j.x+box > mouse[0] >= j.x and j.y+box > mouse[1] > j.y:
                if j.kind == "w":
                    if j.clicked or j.kind == "p":
                        pygame.draw.rect(surf, gray, (j.x, j.y, box, box))
                    elif j in pWNext:
                        pygame.draw.rect(surf, greenH, (j.x, j.y, box, box))
                    else:
                        pygame.draw.rect(surf, lgrayH, (j.x, j.y, box, box))
                elif j.kind in fB:
                    pygame.draw.rect(surf, redH, (j.x, j.y, box, box))
                elif j.kind == "t":
                    pygame.draw.rect(surf, redH, (j.x, j.y, box, box))
            else:
                if j.kind == "w":
                    if j.clicked or j.kind == "p":
                        pygame.draw.rect(surf, gray, (j.x, j.y, box, box))
                    elif j in pWNext:
                        pygame.draw.rect(surf, green, (j.x, j.y, box, box))
                    else:
                        pygame.draw.rect(surf, lgray, (j.x, j.y, box, box))
                elif j.kind in fB:
                    pygame.draw.rect(surf, red, (j.x, j.y, box, box))
                elif j.kind == "t":
                    pygame.draw.rect(surf, red, (j.x, j.y, box, box))
                
#change button color on click
def playerBoardClick(board, surf, mouse, box, fB = 0, pWNext = [], nC = [], gStatus = "shipPlacement", enemyBoard = [], countLeft = 0, points = 0, difficulty = 0):
    x = 0
    for i in board:
        y = 0
        for j in i:
            if j.x+box > mouse[0] >= j.x and j.y+box > mouse[1] > j.y:
                if not j.clicked:
                    if j.kind == "w" and fB != 0:
                        if howMuchShips[fB-1] < fleet[-(fB)]*fB:
                            if howMuchShips[fB-1]%fleetShipTypes[fB-1] == 0 and nC:
                                j.kind = fB
                                howMuchShips[fB-1] += 1
                            elif j in pWNext:
                                j.kind = fB
                                howMuchShips[fB-1] += 1
                    elif j.kind == fB:
                        temp = plsBeFinalNextFix(board, x, y, fB)
                        if temp:
                            j.kind = "w"
                            howMuchShips[fB-1] -= 1
                    elif gStatus == "start":
                        if (enemyBoard[x][y] == "w" or enemyBoard[x][y] == "o"):
                            j.kind = "p"

                            sunk = False

                        elif enemyBoard[x][y] == "s":
                            j.kind = "t"
                            countLeft += 1

                            tempArray = didSunkPlayer(board, enemyBoard, x, y, True, [])
                            sunk = searchInSunkPlayer(tempArray)

                            points = gPoints(difficulty, points, sunk)

                        mType = j.kind

                        if sunk:
                            mType = "z"

                        j.clicked = True

                        return True, countLeft, [x, y], mType, points
            y+=1
        x+=1
    return False, countLeft , 0, 0, points

#generates left bar of the game interface
def leftBar(surf, w, h, margin, pWH, mBeforeButton, board = False):

    pygame.draw.rect(surf, gray, (0, 0, w, h))
    pygame.draw.rect(surf, lgray, (margin, margin, pWH, pWH))

    if not board:
        fleetB = whichShipButtons(margin, mBeforeButton+margin+pWH)

        return fleetB
    else:
        positionLeftPlayerBoard(board, boardSize, leftPlayerBoardBox, leftPlayerBoardGap, leftBarMargin, leftBarMargin, surf)
        
        

#creates table that contains information about fleet buttons (left bar)
def whichShipButtons(x, y, l = len(fleet)):
    bM = fleetBSize["bM"]
    bH = fleetBSize["h"]
    bW = fleetBSize["w"]

    #x for last button
    customX = x+116

    t = []

    for i in range(l):
        if i%2 == 0:
            if i == l-1:
                t.append(pBox(customX, y, i+1))
            else:
                t.append(pBox(x, y, i+1))
        else:
            t.append(pBox(x+bW+bM, y, i+1))
            y += bH+bM

    return t

#generates fleet buttons on the left bar
def fleetButtons(surf, fleetB, mouse):
    h = fleetBSize["h"]
    w = fleetBSize["w"]
    bIM = fleetBSize["bIM"]

    for i in fleetB:
        if i.x+w > mouse[0] >= i.x and i.y+h > mouse[1] > i.y:
            if not i.clicked:
                pygame.draw.rect(surf, black, (i.x, i.y, w, h))
                pygame.draw.rect(surf, lgrayH, (i.x+bIM, i.y+bIM, w-(2*bIM), h-(2*bIM)))
            elif i.clicked:
                pygame.draw.rect(surf, lgrayH, (i.x, i.y, w, h))
                pygame.draw.rect(surf, black, (i.x+bIM, i.y+bIM, w-(2*bIM), h-(2*bIM)))
        else:
            if not i.clicked:
                pygame.draw.rect(surf, black, (i.x, i.y, w, h))
                pygame.draw.rect(surf, lgray, (i.x+bIM, i.y+bIM, w-(2*bIM), h-(2*bIM)))
            elif i.clicked:
                pygame.draw.rect(surf, lgray, (i.x, i.y, w, h))
                pygame.draw.rect(surf, black, (i.x+bIM, i.y+bIM, w-(2*bIM), h-(2*bIM)))

#fleet buttons clickable, returns value of clicked fleet button (0-5, 0 means none is clicked)
def fleetButtonsClickable(fleetB, mouse, w, h, x):
    for i in fleetB:
        if i.x+w > mouse[0] >= i.x and i.y+h > mouse[1] > i.y:
            if not i.clicked:
                fleetButtonsClickableReset(fleetB)
                i.clicked = True
                return i.kind
            elif i.clicked:
                i.clicked = False
                return 0
        
    return x

#resets fleet buttons
def fleetButtonsClickableReset(fleetB):
    for i in fleetB:
        i.clicked = False

def fleetButtonsText(surf, bText, bFleet, bW, bH, fontS = 25):
    smallText = pygame.font.SysFont('Sans', fontS)

    for j in bFleet:

        text, textRect = textObjects(bText, smallText, white)

        textRect.center = ( int(bW), int(bH) )
        surf.blit(text, textRect)

#shows pics on fleet buttons (left bar)
def fleetButtonsPic(surf, fType, fleetB, fBSize, fBT):
    size = 25
    border = 1

    cY = 2

    j = 0

    for i in fType:
        picW = int(((i*size) + ((i+1)*border))/2)

        x = int(fleetB[j].x + fBSize["w"]/2 - picW + 0.5)
        y = int((fleetB[j].y +(size/2)) - cY)

        c = 15

        marginY = int(fleetB[j].y+fBSize["h"]/2+cY)
        marginX = int(fleetB[j].x+fBSize["w"]/2)

        fleetButtonsText(surf, str(fBT[i-1])+" x", fleetB, marginX-(c*i), marginY)

        if i == 1:
            pygame.draw.rect(surf, black, (x+c, y, size, size))
            pygame.draw.rect(surf, red, (x+1+c, y+1, size-(border*2), size-(border*2)))

        elif i == 2:
            for k in range(i):
                pygame.draw.rect(surf, black, (x+c, y, size, size))
                pygame.draw.rect(surf, red, (x+1+c, y+1, size-(border*2), size-(border*2)))

                x += (size-border)

        elif i == 3:
            for k in range(i):
                pygame.draw.rect(surf, black, (x+c, y, size, size))
                pygame.draw.rect(surf, red, (x+1+c, y+1, size-(border*2), size-(border*2)))

                x += (size-border)

        elif i == 4:
            for k in range(i):
                pygame.draw.rect(surf, black, (x+c, y, size, size))
                pygame.draw.rect(surf, red, (x+1+c, y+1, size-(border*2), size-(border*2)))

                x += (size-border)

        elif i == 5:
            for k in range(i):
                pygame.draw.rect(surf, black, (x+c, y, size, size))
                pygame.draw.rect(surf, red, (x+1+c, y+1, size-(border*2), size-(border*2)))

                x += (size-border)

        j += 1


#text function that returns area of text and type (color, font etc.)
def textObjects(text, font, color):
    textSurf = font.render(text, True, color)

    return textSurf, textSurf.get_rect()

#creates array that contains next possible move that player can do
def playerWhereNext(board, fType, fB):
    pWNext = []

    for x in range(len(board)):
        for y in range(len(board[x])):
            t = []
            if board[x][y].kind == fType:
                i = 0
                #up
                if x-1 >= 0:
                    if board[x-1][y].kind in fB:
                        i+=1
                    elif board[x-1][y].kind == "w":
                        k = playerWhereNextFix(board, x-1, y, fB)
                        if len(k) <= 1:
                            t.append(board[x-1][y])
                #right
                if y+1 < len(board):
                    if board[x][y+1].kind in fB:
                        i+=1
                    elif board[x][y+1].kind == "w":
                        k = playerWhereNextFix(board, x, y+1, fB)
                        if len(k) <= 1:
                            t.append(board[x][y+1])
                #down
                if x+1 < len(board):
                    if board[x+1][y].kind in fB:
                        i+=1
                    elif board[x+1][y].kind == "w":
                        k = playerWhereNextFix(board, x+1, y, fB)
                        if len(k) <= 1:
                            t.append(board[x+1][y])
                #left
                if y-1 >= 0:
                    if board[x][y-1].kind in fB:
                        i+=1
                    elif board[x][y-1].kind == "w":
                        k = playerWhereNextFix(board, x, y-1, fB)
                        if len(k) <= 1:
                            t.append(board[x][y-1])

                if i <= 1:
                    for j in t:
                        if j in pWNext:
                            pWNext.remove(j)
                        pWNext.append(j)

    return pWNext

#deletes moves that are forbbiden for player to do
def playerWhereNextFix(board, x, y, fB):
    i = []

    #up
    if x-1 >= 0:
        if board[x-1][y].kind in fB:
            i.append('up')
    #right
    if y+1 < len(board):
        if board[x][y+1].kind in fB:
            i.append('right')
    #down
    if x+1 < len(board):
        if board[x+1][y].kind in fB:
            i.append('down')
    #left
    if y-1 >= 0:
        if board[x][y-1].kind in fB:
            i.append('left')

    return i

#creates array that has information about blocked boxes on player board
def blockedBoxes(board, shipType):
    t = []

    for x in range(len(board)):
        for y in range(len(board[x])):
            k = False
            for i in t:
                if board[x][y] in i:
                    k = True
            b = board[x][y].kind in shipType
            if b and not k:
                if board[x][y].kind == 1:
                    temp = [board[x][y]]
                    t.append(temp)
                else:
                    num = board[x][y].kind
                    i = []
                    temp = blockedBoxesFix(board, num, x, y, i)
                    t.append(temp)

    return t

#fix for blockedBoxes()
def blockedBoxesFix(board, num, x, y, array):
    for i in array:
        if i.kind not in fleetShipTypes:
            array.remove(i)
            
    #up
    if x-1 >= 0:
        if board[x-1][y].kind == num and board[x-1][y] not in array:
            array.append(board[x-1][y])
            array = blockedBoxesFix(board, num, x-1, y, array)
    #right
    if y+1 < len(board):
        if board[x][y+1].kind == num and board[x][y+1] not in array:
            array.append(board[x][y+1])
            array = blockedBoxesFix(board, num, x, y+1, array)
    #down
    if x+1 < len(board):
        if board[x+1][y].kind == num and board[x+1][y] not in array:
            array.append(board[x+1][y])
            array = blockedBoxesFix(board, num, x+1, y, array)
    #left
    if y-1 >= 0:
        if board[x][y-1].kind == num and board[x][y-1] not in array:
            array.append(board[x][y-1])
            array = blockedBoxesFix(board, num, x, y-1, array)

    if board[x][y] not in array:
        array.append(board[x][y])

    return array

#changes clicked value of boxes that are blocked
def displayBlockade(board, array, fleet):
    restartBlockade(board)

    t = list(fleet)
    t.reverse()

    for x in array:
        if len(x) == x[0].kind:
            t[x[0].kind-1] -= 1
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] in x:
                        #up
                        if i-1 >= 0:
                            if board[i-1][j] not in x:
                                if board[i-1][j].kind in fleetShipTypes:
                                    howMuchShips[board[i-1][j].kind - 1] -= 1
                                board[i-1][j].clicked = True
                                board[i-1][j].kind = "w"
                        #upper right
                        if i-1 >= 0 and j+1 < len(board):
                            if board[i-1][j+1] not in x:
                                if board[i-1][j+1].kind in fleetShipTypes:
                                    howMuchShips[board[i-1][j+1].kind - 1] -= 1
                                board[i-1][j+1].clicked = True
                                board[i-1][j+1].kind = "w"
                        #right
                        if j+1 < len(board):
                            if board[i][j+1] not in x:
                                if board[i][j+1].kind in fleetShipTypes:
                                    howMuchShips[board[i][j+1].kind - 1] -= 1
                                board[i][j+1].clicked = True
                                board[i][j+1].kind = "w"
                        #lower right
                        if i+1 < len(board) and j+1 < len(board):
                            if board[i+1][j+1] not in x:
                                if board[i+1][j+1].kind in fleetShipTypes:
                                    howMuchShips[board[i+1][j+1].kind - 1] -= 1
                                board[i+1][j+1].clicked = True
                                board[i+1][j+1].kind = "w"
                        #down
                        if i+1 < len(board):
                            if board[i+1][j] not in x:
                                if board[i+1][j].kind in fleetShipTypes:
                                    howMuchShips[board[i+1][j].kind - 1] -= 1
                                board[i+1][j].clicked = True
                                board[i+1][j].kind = "w"
                        #lower left
                        if i+1 < len(board) and j-1 >= 0:
                            if board[i+1][j-1] not in x:
                                if board[i+1][j-1].kind in fleetShipTypes:
                                    howMuchShips[board[i+1][j-1].kind - 1] -= 1
                                board[i+1][j-1].clicked = True
                                board[i+1][j-1].kind = "w"
                        #left
                        if j-1 >= 0:
                            if board[i][j-1] not in x:
                                if board[i][j-1].kind in fleetShipTypes:
                                    howMuchShips[board[i][j-1].kind - 1] -= 1
                                board[i][j-1].clicked = True
                                board[i][j-1].kind = "w"
                        #upper left
                        if i-1 >= 0 and j-1 >= 0:
                            if board[i-1][j-1] not in x:
                                if board[i-1][j-1].kind in fleetShipTypes:
                                    howMuchShips[board[i-1][j-1].kind - 1] -= 1
                                board[i-1][j-1].clicked = True
                                board[i-1][j-1].kind = "w"
    
    return t

#resets clicked value of every box
def restartBlockade(board):
    for i in board:
        for j in i:
            if j.clicked == True:
                j.clicked = False

def neighbourCount(bBA, bK):
    for i in bBA:
        for j in i:
            if j.kind == bK and len(i) < bK:
                return False
            elif j.kind == bK and len(i) == bK:
                return True

    return True

#checks if player can start a game
def canPFSAFGFFS(bBA, fType):
    t = []

    for i in bBA:
        t.append(len(i))

    t.sort()

    x = list(fType)
    x.reverse()
    
    k = []
    j = list(fleet)

    for i in x:
        k.append(t.count(i))

    if k == j:
        return True
    else:
        return False

#idk, probably some fix for next possible ship placement
def plsBeFinalNextFix(board, x, y, fB):
    j = 0

    if board[x][y].kind == fB:
        if x-1 >= 0:
            if board[x-1][y].kind == fB:
                j+=1
        if y+1 < len(board):
            if board[x][y+1].kind == fB:
                j+=1
        if x+1 < len(board):
            if board[x+1][y].kind == fB:
                j+=1
        if y-1 >= 0:
            if board[x][y-1].kind == fB:
                j+=1

    if j > 1:
        return False
    else:
        return True

#displays start button after user places every ship
def displayStartButton(surf, margin, bSize, bGap, bBox):
    boardW = (bSize*bBox) + ((bSize+1)*bGap)

    bW = 100
    bH = 49
    bMarginY = 25
    bMarginX = int(margin + (boardW/2) - (bW/2))
    bBorder = 2

    pygame.draw.rect(surf, black, (bMarginX, bMarginY, bW, bH))
    pygame.draw.rect(surf, lgray, (bMarginX+bBorder, bMarginY+bBorder, bW-(2*bBorder), bH-(2*bBorder)))

    smallText = pygame.font.SysFont('Sans', 30)

    textSurf, textRect = textObjects("START", smallText, black)
    textRect.center = ( int(bMarginX+(bW/2)), int(bMarginY+(bH/2)) )
    surf.blit(textSurf, textRect)

    return [bMarginX, bMarginY, bW, bH]

#ENEMY AI BELOW

#checks which difficulty the player choose
def enemyTurn(board, ships, boxes, difficulty = "easy"):
    if difficulty == "easy":
        ships, sunk, cords, mType = enemyTurnEasy(board, ships)

    elif difficulty == "normal":
        if len(boxes) == 0:
            ships, boxes, sunk, array, cords, mType = enemyTurnNormalFirst(board, ships)
        else:
            ships, boxes, sunk, array, cords, mType = enemyTurnNormalSecond(board, boxes, ships)

    elif difficulty == "hard":
        if len(boxes) == 0:
            ships, boxes, sunk, array, cords, mType = enemyTurnNormalFirst(board, ships)
        else:
            ships, boxes, sunk, array, cords, mType = enemyTurnNormalSecond(board, boxes, ships)

        if sunk:
            enemyTurnHard(board, array)

    if sunk:
        mType = "z"

    return ships, boxes, False, cords, mType

#function if player choose "easy"
def enemyTurnEasy(board, ships):
    a = True

    while a:
        x = randrange(10)
        y = randrange(10)

        for i in range(len(board)):
            for j in range(len(board[i])):
                if i == x and j == y:
                    if board[x][y].kind not in shotShips:
                        a = False
                        if board[x][y].kind in fleetShipTypes:
                            board[x][y].kind = "t"
                            ships -= 1

                            t = didSunk(board, i, j, True, [])
                            sunk = searchInSunk(t)
                        else:
                            board[x][y].kind = "p"
                            sunk = False

                        return ships, sunk, [x, y], board[x][y].kind

#first function if player choose "normal"
def enemyTurnNormalFirst(board, ships):
    a = True
    while a:
        x = randrange(10)
        y = randrange(10)

        for i in range(len(board)):
            for j in range(len(board[i])):
                if i == x and j == y:
                    if board[x][y].kind not in shotShips:
                        a = False
                        if board[x][y].kind in fleetShipTypes:
                            board[x][y].kind = "t"
                            
                            tempArray = didSunk(board, x, y, True, [])

                            sunk = searchInSunk(tempArray)

                            if sunk:
                                tempArray.append(board[x][y])
                                boxes = []
                            else:
                                boxes = whereNextAi(board, x, y, True, [])

                            ships -= 1

                            return ships, boxes, sunk, tempArray, [x, y], board[x][y].kind
                        else:
                            board[x][y].kind = "p"
                            boxes = []
                            sunk = False
                            tempArray = []

                            return ships, boxes, sunk, tempArray, [x, y], board[x][y].kind

#second function if player choose "normal"
def enemyTurnNormalSecond(board, boxes, ships):
    i = randrange(len(boxes))

    x, y = indexes(board, boxes[i])

    if board[x][y].kind not in fleetShipTypes:
        board[x][y].kind = "p"
        boxes.remove(board[x][y])
        
        sunk = False
        tempArray = []
    else:
        board[x][y].kind = "t"
        tempArray = didSunk(board, x, y, True, [])
        
        sunk = searchInSunk(tempArray)

        ships -= 1

        if sunk:
            boxes = []
        else:
            boxes = whereNextAi(board, x, y, True, [])

    return ships, boxes, sunk, tempArray, [x, y], board[x][y].kind

#function if player choose "hard"
def enemyTurnHard(board, array):
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] in array:
                if x-1 >= 0:
                    if board[x-1][y].kind == "w":
                        board[x-1][y].kind = "n"

                if x-1 >= 0 and y+1 < len(board):
                    if board[x-1][y+1].kind == "w":
                        board[x-1][y+1].kind = "n"
                
                if y+1 < len(board):
                    if board[x][y+1].kind == "w":
                        board[x][y+1].kind = "n"

                if x+1 < len(board) and y+1 < len(board):
                    if board[x+1][y+1].kind == "w":
                        board[x+1][y+1].kind = "n"
                
                if x+1 < len(board):
                    if board[x+1][y].kind == "w":
                        board[x+1][y].kind = "n"

                if x+1 < len(board) and y-1 >= 0:
                    if board[x+1][y-1].kind == "w":
                        board[x+1][y-1].kind = "n"
                
                if y-1 >= 0:
                    if board[x][y-1].kind == "w":
                        board[x][y-1].kind = "n"
                
                if x-1 >= 0 and y-1 >= 0:
                    if board[x-1][y-1].kind == "w":
                        board[x-1][y-1].kind = "n"

#checks if ship was sunk
def searchInSunk(t):
    for i in t:
        if i.kind in fleetShipTypes:
            return False

    return True

#returns values of currently shot ship
def didSunk(board, x, y, a, t):
    if a:
        t = []

    if x-1 >= 0:
        if (board[x-1][y].kind in fleetShipTypes or board[x-1][y].kind == "t") and board[x-1][y] not in t:
            t.append(board[x-1][y])
            t = didSunk(board, x-1, y, False, t)
    
    if y+1 < len(board):
        if (board[x][y+1].kind in fleetShipTypes or board[x][y+1].kind == "t") and board[x][y+1] not in t:
            t.append(board[x][y+1])
            t = didSunk(board, x, y+1, False, t)
    
    if x+1 < len(board):
        if (board[x+1][y].kind in fleetShipTypes or board[x+1][y].kind == "t") and board[x+1][y] not in t:
            t.append(board[x+1][y])
            t = didSunk(board, x+1, y, False, t)
    
    if y-1 >= 0:
        if (board[x][y-1].kind in fleetShipTypes or board[x][y-1].kind == "t") and board[x][y-1] not in t:
            t.append(board[x][y-1])
            t = didSunk(board, x, y-1, False, t)

    return t

#works only on normal/hard, checks next possible ship placement
def whereNextAi(board, x, y, a, t=[], b = ""):
    if a:
        t = []

    j = 0

    if x-1 >= 0:
        if board[x-1][y].kind == "t":
            j += 1

    if y+1 < len(board):
        if board[x][y+1].kind == "t":
            j += 1
    
    if x+1 < len(board):
        if board[x+1][y].kind == "t":
            j += 1

    if y-1 < len(board):
        if board[x][y-1].kind == "t":
            j += 1

    if x-1 >= 0 and b != "d":
        if board[x-1][y].kind == "t":
            t = whereNextAi(board, x-1, y, False, t, "u")
        elif board[x-1][y].kind in fleetShipTypes or board[x-1][y].kind == "w":
            if board[x-1][y] in t:
                t.remove(board[x-1][y])
            elif j < 2:
                t.append(board[x-1][y])
    
    if y+1 < len(board) and b != "l":
        if board[x][y+1].kind == "t":
            t = whereNextAi(board, x, y+1, False, t, "r")
        elif board[x][y+1].kind in fleetShipTypes or board[x][y+1].kind == "w":
            if board[x][y+1] in t:
                t.remove(board[x][y+1])
            elif j < 2:
                t.append(board[x][y+1])
    
    if x+1 < len(board) and b != "u":
        if board[x+1][y].kind == "t":
            t = whereNextAi(board, x+1, y, False, t, "d")
        elif board[x+1][y].kind in fleetShipTypes or board[x+1][y].kind == "w":
            if board[x+1][y] in t:
                t.remove(board[x+1][y])
            elif j < 2:
                t.append(board[x+1][y])
    
    if y-1 >= 0 and b != "r":
        if board[x][y-1].kind == "t":
            t = whereNextAi(board, x, y-1, False, t, "l")
        elif board[x][y-1].kind in fleetShipTypes or board[x][y-1].kind == "w":
            if board[x][y-1] in t:
                t.remove(board[x][y-1])
            elif j < 2:
                t.append(board[x][y-1])

    return t

#searches through board and returns right indexes
def indexes(board, i):
    for x in range(len(board)):
        for y in  range(len(board[x])):
            if board[x][y] == i:
                return x, y

#coin toss, used to determin who starts the game first
def coinToss():
    x = randrange(2)

    if x == 1:
        return True
    else:
        return False

#end game screen display
def gameEnd(surf, w, h, isWinner = True):
    s = pygame.Surface((w,h), pygame.SRCALPHA)
    s.fill(endBg)

    surf.blit(s, (0,0))

    if isWinner:
        text = "You Win!"
        color = green
    else:
        text = "You Lose!"
        color = red

    fSize = 230

    font = pygame.font.SysFont('Sans', fSize)
    
    text = render(text, font, color)
    surfCenter = surf.get_rect().center

    textCenter = (surfCenter[0]-int(text.get_rect().width/2), surfCenter[1]-int(text.get_rect().height + text.get_rect().height/3))

    surf.blit(text, textCenter)

    eGameB = eGameButtonsAssign(eGameButtons, fSize, surfCenter)

    return eGameB

def eGameButtonsAssign(buttons, fSize, center, eGBM = 100, eGBW = 400, eGBH = 90):
    c = 0
    t = []

    for i in buttons:
        x = center[0]-int(eGBW/2)
        y = eGameTMargin + fSize + eGBM + c

        t.append(fBPic(x, y, i))

        c += eGBH + eGameButtonM

    return t  
    
def eGameButtonsHover(surf, eGameB, mouse, fBSize = 60, eGBM = 100, eGBW = 400, eGBH = 90, a = False):
    for i in eGameB:
        pygame.draw.rect(surf, black, (i.x, i.y, eGBW, eGBH))

        font = pygame.font.SysFont('Sans', fBSize)
    
        if i.x+eGBW > mouse[0] >= i.x and i.y+eGBH > mouse[1] >= i.y:
            color = lgrayH
            if a:
                if i.size == "EASY":
                    text = render(i.size, font, greenH)
                elif i.size == "NORMAL":
                    text = render(i.size, font, yellowH)
                elif i.size == "HARD":
                    text = render(i.size, font, redH)
            else:
                text = render(i.size, font, gray)
        else:
            color = lgray
            if a:
                if i.size == "EASY":
                    text = render(i.size, font, green)
                elif i.size == "NORMAL":
                    text = render(i.size, font, yellow)
                elif i.size == "HARD":
                    text = render(i.size, font, red)
            else:
                text = render(i.size, font, black)

        pygame.draw.rect(surf, color, (i.x+eGameButtonB, i.y+eGameButtonB, eGBW-2*eGameButtonB, eGBH-2*eGameButtonB))

        buttonCenter = (i.x + eGBW/2, i.y + eGBH/2)

        textCenter = (int(buttonCenter[0])-int(text.get_rect().width/2), int(buttonCenter[1])-int(text.get_rect().height/2))

        surf.blit(text, textCenter)

def eGameButtonsClick(eGameB, mouse, eGBW = 400, eGBH = 90):
    for i in eGameB:
        if i.x+eGBW > mouse[0] >= i.x and i.y+eGBH > mouse[1] >= i.y:
            return i.size

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor, ocolor=(255, 255, 255), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))

    return surf

def menu(surf, buttons):
    surf.fill(blue)

    fSize = 200

    font = pygame.font.SysFont('Sans', fSize)
    
    text = render("WarShips", font, black)

    surfCenter = surf.get_rect().center
    textCenter = (surfCenter[0]-int(text.get_rect().width/2), menuTMargin)

    surf.blit(text, textCenter)

    menuB = menuButtonsAssign(buttons, fSize, surfCenter)

    return menuB

def menuButtonsAssign(buttons, fSize, center):
    c = 0
    t = []

    for i in buttons:
        x = center[0]-int(menuButtonW/2)
        y = menuTMargin + fSize + menuBetweenM + c

        t.append(fBPic(x, y, i))

        c += menuButtonH + menuButtonM

    return t

def menuButtonsHover(surf, menuB, mouse):
    for i in menuB:
        pygame.draw.rect(surf, black, (i.x, i.y, menuButtonW, menuButtonH))

        font = pygame.font.SysFont('Sans', 60)
    
        if i.x+menuButtonW > mouse[0] >= i.x and i.y+menuButtonH > mouse[1] >= i.y:
            color = lgray
            fColor = gray
        else:
            color = lgrayH
            fColor = black

        pygame.draw.rect(surf, color, (i.x+menuButtonB, i.y+menuButtonB, menuButtonW-2*menuButtonB, menuButtonH-2*menuButtonB))

        text = render(i.size, font, fColor)
        buttonCenter = (i.x + menuButtonW/2, i.y + menuButtonH/2)

        textCenter = (int(buttonCenter[0]-int(text.get_rect().width/2)), int(buttonCenter[1]-int(text.get_rect().height/2)))

        surf.blit(text, textCenter)

def menuButtonsClick(menuB, mouse):
    for i in menuB:
        if i.x+menuButtonW > mouse[0] >= i.x and i.y+menuButtonH > mouse[1] >= i.y:
            return i.size

def difScreen(surf, w, h):
    s = pygame.Surface((w,h), pygame.SRCALPHA)
    s.fill(difBg)

    surf.blit(s, (0,0))

    text = "CHOOSE ENEMY DIFFICULTY"

    fSize = 80

    font = pygame.font.SysFont('Sans', fSize)
    
    text = render(text, font, dBlue)
    surfCenter = surf.get_rect().center

    textCenter = (surfCenter[0]-int(text.get_rect().width/2), surfCenter[1]-int(text.get_rect().height + 2*text.get_rect().height))

    surf.blit(text, textCenter)

    difB = eGameButtonsAssign(difButtons, fSize, surfCenter, difBetweenM, difButtonW, difButtonH)

    return difB

def createMessage(a, cords, mType, gFeed):
    if a:
        who = "Enemy"
    else:
        who = "You"

    if mType == "p" and a:
        cords = cordsTranslation(cords)
        message = who+" missed! ("+str(cords[0])+", "+str(cords[1]+1)+")"
    elif mType == "t" and a:
        cords = cordsTranslation(cords)
        message = who+" hit your ship! ("+str(cords[0])+", "+str(cords[1]+1)+")"
    elif mType == "z" and not a:
        message = who+" sank enemy's ship!"
    elif mType == "z" and a:
        message = who+" sank your ship!"

    return feedAdd(gFeed, message)

def cordsTranslation(cords):
    xCords = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")

    return [xCords[cords[0]], cords[1]]

def botThinkingLol(board, surf, lPBB, sShips, a, cords, mType, gFeed):
    displayLeftPlayerBoard(board, surf, lPBB, sShips)

    gFeed = createMessage(a, cords, mType, gFeed)

    return False, True, gFeed

def feedAdd(gFeed, message):
    gFeed.insert(0, message)

    if len(gFeed) > feedLength:
        del gFeed[feedLength]

    return gFeed

def feedRead(surf, gFeed):

    pygame.draw.rect(surf, lgray, (int(leftBarMargin), int(pWH+leftBarMargin+(leftBarMargin/2)), pWH, int(gameFeedH)))
    j = 0

    fSize = 19
    font = pygame.font.SysFont('Sans', fSize)

    barH = gameFeedH/feedLength
    barW = pWH

    barP = (barH - fSize)/2

    c = 0

    for i in gFeed:
        if j%2 == 0:
            pygame.draw.rect(surf, lgrayH, (int(leftBarMargin), int(pWH+leftBarMargin+(leftBarMargin/2)+gameFeedH-barH-c), pWH, int(barH)))
        else:
            pygame.draw.rect(surf, lgray, (int(leftBarMargin), int(pWH+leftBarMargin+(leftBarMargin/2)+gameFeedH-barH-c), pWH, int(barH)))

        if i == "You sank enemy's ship!":
            color = red
        else:
            color = black

        text, textRect = textObjects(i, font, color)

        textCords = [int(leftBarMargin+barP), int(pWH+leftBarMargin+(leftBarMargin/2)+gameFeedH-barH-c+barP)]
        surf.blit(text, textCords)

        j += 1
        c += barH

def didSunkPlayer(board, eBoard, x, y, a, t):
    if a:
        t = []

    if x-1 >= 0:
        if (eBoard[x-1][y] == "s" or board[x-1][y].kind == "t") and board[x-1][y] not in t:
            t.append(board[x-1][y])
            t = didSunkPlayer(board, eBoard, x-1, y, False, t)
    
    if y+1 < len(board):
        if (eBoard[x][y+1] == "s" or board[x][y+1].kind == "t") and board[x][y+1] not in t:
            t.append(board[x][y+1])
            t = didSunkPlayer(board, eBoard, x, y+1, False, t)
    
    if x+1 < len(board):
        if (eBoard[x+1][y] == "s" or board[x+1][y].kind == "t") and board[x+1][y] not in t:
            t.append(board[x+1][y])
            t = didSunkPlayer(board, eBoard, x+1, y, False, t)
    
    if y-1 >= 0:
        if (eBoard[x][y-1] == "s" or board[x][y-1].kind == "t") and board[x][y-1] not in t:
            t.append(board[x][y-1])
            t = didSunkPlayer(board, eBoard, x, y-1, False, t)

    return t

def searchInSunkPlayer(t):
    for i in t:
        if i.kind == "w":
            return False

    return True

def gPoints(dif, points, sunk):
    if dif == "easy":
        if sunk:
            points += 20
        else:
            points += 10
    elif dif == "normal":
        if sunk:
            points += 40
        else:
            points += 20
    elif dif == "hard":
        if sunk:
            points += 60
        else:
            points += 30

    return points

def displayTimer(surf, cTime):
    smallText = pygame.font.SysFont('Sans', 40)

    cTime = str(cTime)
    time = cTime[:-3]
    textTime = '00:00'

    if time:
        textTime = ''
        time = int(time)

        minutes = int(time/60)
        seconds = time - (minutes*60)

        if(minutes == 0):
            textTime = "00:"
        elif(minutes > 9):
            textTime = str(minutes)+":"
        elif(minutes > 0):
            textTime = "0"+str(minutes)+":"
        
        
        if(seconds > 9):
            textTime += str(seconds)
        elif(seconds > 0):
            textTime += "0"+str(seconds)
        else:
            textTime += "00"

    text, textRect = textObjects(textTime, smallText, black)

    textRect.center = ( pBMarginX + int(pBoardWH/2), int(pBMarginY/2))

    pygame.draw.rect(surf, blue, (pBMarginX, 0, pBMarginX+pBoardWH, pBMarginY))

    surf.blit(text, textRect)

def finalScore(surf, points, time, isWin):
    time = str(time)
    time = time[:-3]
    time = int(time)

    finalMultiplier = float(time/60)

    score = int(points/finalMultiplier)

    textScore = "Your final score: "+str(score)

    smallText = pygame.font.SysFont('Sans', 40)

    text, textRect = textObjects(textScore, smallText, white)

    textRect.center = ( int(boardWidth/2), 300)

    surf.blit(text, textRect)

    try:
        f = open('scoreboard.txt', 'r+')
    except FileNotFoundError:
        f = open('scoreboard.txt', 'w+')

    t = []

    for i in f:
        x = i.strip('\n').split(';')
        t.append(x)

    minutes = int(time/60)
    seconds = time - (minutes*60)

    textTime = ''

    if(minutes == 0):
        textTime = "00:"
    elif(minutes > 9):
        textTime = str(minutes)+":"
    elif(minutes > 0):
        textTime = "0"+str(minutes)+":"


    if(seconds > 9):
        textTime += str(seconds)
    elif(seconds > 0):
        textTime += "0"+str(seconds)
    else:
        textTime += "00"

    if t and isWin:
        j = 0

        for i in t:
            if int(i[1]) < score:

                x = [dif, str(score), textTime]

                t.insert(j, x)
                break
            j += 1

        j = 0

        f.close()
        f = open('scoreboard.txt', 'w+')

        if len(t) > 10:
            dl = 10
        else:
            dl = len(t)

        for i in range(dl):
            if j < dl-1:
                f.write(t[i][0]+';'+t[i][1]+';'+t[i][2]+'\n')
            else:
                f.write(t[i][0]+';'+t[i][1]+';'+t[i][2])
            j += 1

    elif isWin:
        f.write(dif+';'+str(score)+';'+textTime)

    f.close()

def scoreboard(surf):
    surf.fill(blue)

    font = pygame.font.SysFont('Sans', 70)

    text = render("SCOREBOARD", font, black)
    textCenter = (int(boardWidth/2) - int(text.get_rect().width/2), 25)

    surf.blit(text, textCenter)

    try:
        f = open('scoreboard.txt', 'r')
    except FileNotFoundError:
        f = open('scoreboard.txt', 'w+')

    font = pygame.font.SysFont('Sans', 70)

    textDif = "DIFFICULTY"
    textScore = "SCORE"
    textTime = "TIME"

    smallText = pygame.font.SysFont('Sans', 40)

    text, textRect = textObjects(textDif, smallText, black)
    textRect.center = (193 + int(296/2), 133+int(50/2))
    surf.blit(text, textRect)

    text, textRect = textObjects(textScore, smallText, black)
    textRect.center = (193 + 299 + int(296/2), 133+int(50/2))
    surf.blit(text, textRect)

    text, textRect = textObjects(textTime, smallText, black)
    textRect.center = (193 + (299*2) + int(296/2), 133+int(50/2))
    surf.blit(text, textRect)

    t = []

    y = 40

    for i in f:
        i = i.strip('\n').split(';')
        
        smallText = pygame.font.SysFont('Sans', 30)

        text, textRect = textObjects(i[0].capitalize(), smallText, black)
        textRect.center = (193 + int(296/2), 136+ y +int(50/2))
        surf.blit(text, textRect)

        text, textRect = textObjects(i[1], smallText, black)
        textRect.center = (193 + 299 + int(296/2), 136+ y +int(50/2))
        surf.blit(text, textRect)

        text, textRect = textObjects(i[2], smallText, black)
        textRect.center = (193 + (299*2) + int(296/2), 136 + y+int(50/2))
        surf.blit(text, textRect)

        y+=40

    pygame.draw.rect(surf, black, (190, 133, 3, 453))
    pygame.draw.rect(surf, black, (489, 133, 3, 453))
    pygame.draw.rect(surf, black, (788, 133, 3, 453))
    pygame.draw.rect(surf, black, (1087, 133, 3, 453))
    pygame.draw.rect(surf, black, (190, 586, 900, 3))
    pygame.draw.rect(surf, black, (190, 183, 900, 3))
    pygame.draw.rect(surf, black, (190, 133, 900, 3))

def scoreBButton(surf, mouse):
    pygame.draw.rect(surf, black, (int(boardWidth/2) - 150, 586+35, 300, 70))

    font = pygame.font.SysFont('Sans', 50)

    text = render('MENU', font, black)
    textCenter = (int(boardWidth/2) - int(text.get_rect().width/2), 586+40)

    if(int(boardWidth/2) - 150 < mouse[0] <  int(boardWidth/2) - 150 + 300 and 586+35 < mouse[1] < 586+35+70):
        pygame.draw.rect(surf, lgray, (int(boardWidth/2) - 150+3, 586+35+3, 300-6, 70-6))
    else:
        pygame.draw.rect(surf, lgrayH, (int(boardWidth/2) - 150+3, 586+35+3, 300-6, 70-6))
    
    surf.blit(text, textCenter)

main()