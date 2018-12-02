#game.py
#mostly game loop code here
import time, math
import pygame, sys
from car import Car

class Game:
    def __init__(self, canvas_width, canvas_height):
        #initializing pygame and the screen
        pygame.init()
        pygame.key.set_repeat(1, 10)
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Courier New', 30)
        self.width = canvas_width
        self.height = canvas_height
        self.screen = pygame.display.set_mode((self.width, self.height))

        #setting up some road stuff
        self.leftTurns = [60]
        self.rightTurns = [15]
        self.turnLength = 20
        self.turnIntensity = 1
        self.ease = 0
        self.easeIn = False
        self.roadRatio = 0.6
        self.roadColor = pygame.Color(50, 50, 50)

        #player stuff
        self.drawdistance = 30
        self.playerPos = 0
        self.car = Car(self.width*0.5, self.height*0.85, self.width, self.height)
        self.allSprites = pygame.sprite.Group(self.car)
    def start(self, fps):
        #start the game loop given frames per second
        self.millisBetweenTicks = (1/fps) * 1000
        self.lastTick = int(time.time() * 1000)
        self.gameloop()
    def createscreen(self):        
        return 
    def gameloop(self):
        #this is the game loop
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            if(int(time.time()*1000) > self.lastTick + self.millisBetweenTicks):
                self.lastTick = int(time.time() * 1000)
                self.tick()
    def tick(self):
        #this gets called every tick
        self.check_input()
        self.drawBackground()
        self.drawRoad()
        self.movement()
        
        self.allSprites.update()
        self.allSprites.draw(self.screen)
        pygame.display.update()

    def drawRoad(self):
        left=False
        right=False
        nextTurn = 0
        roadWidth = self.width
        stripeWidth = roadWidth/20
        turnPos = 0
        playerDistAway = 0
        for i in range(0, len(self.leftTurns)):
            if(self.playerPos > self.leftTurns[i] - self.drawdistance and self.playerPos < self.leftTurns[i] + self.turnLength):
                left = True
                nextTurn = i
                playerDistAway = self.playerPos - self.leftTurns[nextTurn]
        for i in range(0, len(self.rightTurns)):
            if(self.playerPos > self.rightTurns[i] - self.drawdistance and self.playerPos < self.rightTurns[i] + self.turnLength):
                right = True
                nextTurn = i
                playerDistAway = self.playerPos - self.rightTurns[nextTurn]

        self.easeIn = playerDistAway < 0
        if(left or right):
            if(self.easeIn and self.ease <= self.turnIntensity):
                self.ease += 0.1
            elif(not self.easeIn and self.ease >= 0):
                self.ease -= 0.1
            if(self.ease < 0):
                self.ease = 0
        else:
            self.ease = 0
        for i in range(1, int(self.height*self.roadRatio), 2):
            roadX = 0
            stripeLeftX = 0
            stripeRightX = 0
            rectPos = self.playerPos + (i/(self.height*self.roadRatio))*self.drawdistance
            stripeColor = pygame.Color(255, 255, 255)
            grassColor = pygame.Color(50, 150, 50)
            roadY = self.height - i
            percentPerspective = i/(self.height*self.roadRatio)
            stripeVar = math.sin(30*math.pow(0.5+percentPerspective, 4) + 20*self.playerPos)
            grassVar = math.sin(6*math.pow(0.5+percentPerspective, 4) + 4*self.playerPos)
            print("{}, {}".format(i, rectPos))
            #print(stripeVar)
            if(stripeVar > 0):
                stripeColor = pygame.Color(255, 0, 0)
            if(grassVar > 0):
                grassColor = pygame.Color(50, 200, 50)
            #print(rectPosition)
            if(left or right):
                turnPos = (i/(self.height*self.roadRatio))*self.ease
            else:
                turnPos = 0
            if(left):
                roadX = self.width/2 - roadWidth/2 - turnPos*i
                stripeLeftX = self.width/2 - roadWidth/2 - turnPos*i - stripeWidth/2
                stripeRightX = self.width/2 + roadWidth/2 - turnPos*i- stripeWidth/2
            elif(right):
                roadX = self.width/2 - roadWidth/2 + turnPos*i
                stripeLeftX = self.width/2 - roadWidth/2 + turnPos*i - stripeWidth/2
                stripeRightX = self.width/2 + roadWidth/2 + turnPos*i- stripeWidth/2
            else: 
                roadX = self.width/2 - roadWidth/2
                stripeLeftX = self.width/2 - roadWidth/2 - stripeWidth/2
                stripeRightX = self.width/2 + roadWidth/2 - stripeWidth/2

            pygame.draw.rect(self.screen, grassColor, (0, roadY, self.width, 2))
            pygame.draw.rect(self.screen, self.roadColor, (roadX, roadY, roadWidth, 2))
            pygame.draw.rect(self.screen, stripeColor, (stripeLeftX, roadY, stripeWidth, 2))
            pygame.draw.rect(self.screen, stripeColor, (stripeRightX, roadY, stripeWidth, 2))
            roadWidth-=self.width* 0.005
            stripeWidth = int(roadWidth/20)+1

    
    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.car.accelerate()
        elif keys[pygame.K_s]:
            self.car.decelerate()
        if keys[pygame.K_d]:
            self.car.right()
        elif keys[pygame.K_a]:
            self.car.left()

    def movement(self):
        self.playerPos +=0.1
        textsurface = self.myfont.render("{}".format(self.playerPos), False, (0, 0, 0))
        self.screen.blit(textsurface,(0,0))

    def drawBackground(self):
        pygame.draw.rect(self.screen, pygame.Color("cyan"), (0,0,self.width,self.height*(1-self.roadRatio) + 1))


