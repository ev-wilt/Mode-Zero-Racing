#game.py
#mostly game loop code here
import time, math
import pygame, sys
from car import Car
from enemy import Enemy

class Game:
    def __init__(self, canvas_width, canvas_height):
        #initializing pygame and the screen
        pygame.init()
        pygame.key.set_repeat(1, 10)
        pygame.font.init()
        pygame.display.set_caption('437 Final')
        self.myfont = pygame.font.SysFont('Courier New', 30)
        self.width = canvas_width
        self.height = canvas_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.p1surface = pygame.Surface((self.width,  int(self.height/2)))
        self.p2surface = pygame.Surface((self.width, int(self.height/2)))

        #setting up some road stuff
        self.leftTurns = [55, 180]
        self.rightTurns = [120]
        self.turnLength = 30
        self.turnIntensity = 1
        self.roadRatio = 0.4
        self.roadColor = pygame.Color(50, 50, 50)
        self.drawdistance = 10

        #player stuff
        self.p1 = Car(1, self.width*0.3, (self.height/2)*0.85, self.width, (self.height/2), self.roadRatio)
        self.p2 = Car(2, self.width*0.7, (self.height/2)*0.85, self.width, (self.height/2), self.roadRatio)
        
        self.p1Enemy = Enemy(self.width*0.7, (self.height/2)*0.85, self.p2)
        self.p2Enemy = Enemy(self.width*0.3, (self.height/2)*0.85, self.p1)

        #sprite groups
        self.p1Sprites = pygame.sprite.Group(self.p1)
        self.p1EnemySprites = pygame.sprite.Group(self.p1Enemy)
        self.p2Sprites = pygame.sprite.Group(self.p2)
        self.p2EnemySprites = pygame.sprite.Group(self.p2Enemy)
    def start(self, fps):
        #start the game loop given frames per second
        self.millisBetweenTicks = (1/fps) * 1000
        self.lastTick = int(time.time() * 1000)
        self.gameloop()
    def create_surface(self, width, height):
        return pygame.Surface((width, height))
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

        self.drawBackground(self.p1, self.p1surface)
        self.drawRoad(self.p1, self.p1surface)
        self.drawEnemy(self.p1, self.p1Enemy, self.p1surface)
        self.movement(self.p1, self.p1surface)
        
        self.drawBackground(self.p2, self.p2surface)
        self.drawRoad(self.p2, self.p2surface)
        self.drawEnemy(self.p2, self.p2Enemy, self.p2surface)
        self.movement(self.p2, self.p2surface)
        
        self.p1Sprites.update()
        self.p1EnemySprites.update()

        
        self.p2Sprites.update()
        self.p2EnemySprites.update()
        
        #checking drawing layer order... ugh
        if(self.p1.getPosition() > self.p2.getPosition()):
            self.p1Sprites.draw(self.p1surface)
            self.p1EnemySprites.draw(self.p1surface)
            self.p2EnemySprites.draw(self.p2surface)
            self.p2Sprites.draw(self.p2surface)
        else:
            self.p2Sprites.draw(self.p2surface)
            self.p2EnemySprites.draw(self.p2surface)
            self.p1EnemySprites.draw(self.p1surface)
            self.p1Sprites.draw(self.p1surface)
        
        self.screen.blit(self.p1surface, (0, 0))
        self.screen.blit(self.p2surface, (0, int(self.height/2)))
        pygame.display.update()

    def drawRoad(self, player, surface):
        surfaceHeight = surface.get_height()
        playerPos = player.getPosition()
        left=False
        right=False
        nextTurn = 0
        roadWidth = self.width
        stripeWidth = roadWidth/20
        turnPos = 0
        playerDistAway = 0
        for i in range(0, len(self.leftTurns)):
            if(playerPos > self.leftTurns[i] - self.drawdistance and playerPos < self.leftTurns[i] + self.turnLength):
                left = True
                nextTurn = i
                playerDistAway = playerPos - self.leftTurns[nextTurn]
        for i in range(0, len(self.rightTurns)):
            if(playerPos > self.rightTurns[i] - self.drawdistance and playerPos < self.rightTurns[i] + self.turnLength):
                right = True
                nextTurn = i
                playerDistAway = playerPos - self.rightTurns[nextTurn]

        player.turning = playerDistAway < self.turnLength/2
        if(left or right):
            if(player.isTurning()):
                player.incrementTurnProgress(self.turnIntensity)
            elif(not player.isTurning()):
                player.decrementTurnProgress(0)

        if(left and player.isTurning()):
            player.getBackground().offsetBackground(25*player.speed)
        elif(right and player.isTurning()):
            player.getBackground().offsetBackground(-25*player.speed)

        if(left):
            player.drift(1)
        elif(right):
            player.drift(-1)

        for i in range(0, int(surfaceHeight*self.roadRatio) + 2, 2):
            roadX = 0
            stripeLeftX = 0
            stripeRightX = 0
            stripeColor = pygame.Color(255, 255, 255)
            grassColor = pygame.Color(29, 42, 42)
            roadY = surfaceHeight- i
            percentPerspective = i/(surfaceHeight*self.roadRatio)
            stripeVar = math.sin(24*math.pow(0.5+percentPerspective, 4) + 16*playerPos)
            grassVar = math.sin(6*math.pow(0.5+percentPerspective, 4) + 4*playerPos)
            if(stripeVar > 0):
                stripeColor = pygame.Color(255, 0, 0)
            if(grassVar > 0):
                grassColor = pygame.Color(49, 59, 59)
            if(left or right):
                turnPos = (i/(surfaceHeight*self.roadRatio))*player.getTurnProgress()
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

            pygame.draw.rect(surface, grassColor, (0, roadY, self.width, 2))
            pygame.draw.rect(surface, self.roadColor, (roadX, roadY, roadWidth, 2))
            pygame.draw.rect(surface, stripeColor, (stripeLeftX, roadY, stripeWidth, 2))
            pygame.draw.rect(surface, stripeColor, (stripeRightX, roadY, stripeWidth, 2))
            roadWidth-= 1.98*self.width/(surfaceHeight*self.roadRatio)
            stripeWidth = int(roadWidth/20)+1

    def drawEnemy(self, player, enemySprite, surface):
        distanceFromEnemy = enemySprite.getCar().getPosition() - player.getPosition()
        distanceValue = (self.drawdistance - distanceFromEnemy)/self.drawdistance
        if(distanceFromEnemy < self.drawdistance and distanceFromEnemy > 0):
            enemySprite.scale(distanceValue, player.getTurnProgress())
            enemySprite.y = surface.get_height()*.85 - surface.get_height()*self.roadRatio*(1-distanceValue)*.64
        elif(distanceFromEnemy < self.drawdistance and distanceFromEnemy > -5):
            #don't scale
            enemySprite.scale(distanceValue, player.getTurnProgress())
            enemySprite.y = surface.get_height()*.85 - surface.get_height()*self.roadRatio*(1-distanceValue)
        else:
            enemySprite.scale(0, player.getTurnProgress())


    
    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.p1.accelerate()
        elif keys[pygame.K_s]:
            self.p1.decelerate()
        if keys[pygame.K_d]:
            self.p1.right()
        elif keys[pygame.K_a]:
            self.p1.left()
        else:
            self.p1.straighten()

            
        if keys[pygame.K_UP]:
            self.p2.accelerate()
        elif keys[pygame.K_DOWN]:
            self.p2.decelerate()
        if keys[pygame.K_RIGHT]:
            self.p2.right()
        elif keys[pygame.K_LEFT]:
            self.p2.left()
        else:
            self.p2.straighten()

    def movement(self, player, surface):
        textsurface = self.myfont.render("{}".format(player.getPosition()), False, (0, 0, 0))
        surface.blit(textsurface,(0,0))

    def drawBackground(self, player, surface):
        #pygame.draw.rect(self.screen, pygame.Color("cyan"), (0,0,self.width,self.height*(1-self.roadRatio) + 1))
        surface.blit(player.getBackground().getLeftImage(), player.getBackground().getLeftRect())
        surface.blit(player.getBackground().getRightImage(), player.getBackground().getRightRect())


