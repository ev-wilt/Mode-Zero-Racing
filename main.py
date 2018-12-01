#main.py
#example game code here
import pygame
from game import Game

position = 0
turnleft = [30]
turnright = [15]
drawdistance = 10
turnLength = 20
turnTarget = 2
easeIn = False
ease = 0
width = 800
height = 600
pygame.font.init()
myfont = pygame.font.SysFont('Courier New', 30)


def drawRoad():
    global ease
    left=False
    right=False
    nextTurn = 0
    roadWidth = width
    turnPos = 0
    playerDistAway = 0
    for i in range(0, len(turnleft)):
        if(position > turnleft[i] - drawdistance and position < turnleft[i] + turnLength):
            left = True
            nextTurn = i
            playerDistAway = position - turnleft[nextTurn]
    for i in range(0, len(turnright)):
        if(position > turnright[i] - drawdistance and position < turnright[i] + turnLength):
            right=True
            nextTurn = i
            playerDistAway = position - turnright[nextTurn]

    easeIn = playerDistAway < 0
    print(playerDistAway)
    print(easeIn)
    if(left or right):
        if(easeIn and ease <= turnTarget):
            ease += 0.1
        elif(not easeIn and ease >= 0):
            ease -= 0.1
        if(ease < 0):
            ease = 0
    else:
        ease = 0
    for i in range(1, int(height/2)):
        rectPosition = position + (i/(height/2))*drawdistance
        #print(rectPosition)
        if(left or right):
            turnPos = (i/(height/2))*ease
        else:
            turnPos = 0
        if(left):
            pygame.draw.rect(screen, pygame.Color(50, 50, 50), (width/2 - roadWidth/2 - turnPos*i, height-i, roadWidth, 2))
        elif(right):
            pygame.draw.rect(screen, pygame.Color(50, 50, 50), (width/2 - roadWidth/2 + turnPos*i, height-i, roadWidth, 2))
        else: 
            pygame.draw.rect(screen, pygame.Color(50, 50, 50), (width/2 - roadWidth/2, height-i, roadWidth, 2))
        roadWidth-=2.5

def movement():
    global position
    position+=0.1
    textsurface = myfont.render("{}".format(position), False, (0, 0, 0))
    screen.blit(textsurface,(0,0))

def drawBackground():
    pygame.draw.rect(screen, pygame.Color("cyan"), (0,0,width,height/2))
    pygame.draw.rect(screen, pygame.Color("green"), (0,height/2,width,height/2))



def gameloop():
    drawBackground()
    drawRoad()
    movement()
    
    pygame.display.update()

    
game = Game(width, height)
screen = game.createscreen()
game.update = gameloop
game.start(30)