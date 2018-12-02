import pygame, sys
from pygame.locals import *

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("car.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #fixing it to not move but rather just change values for a centered camera
        self.x = x
        self.y = y
        self.speed = 0
        self.speedX = 0
        self.minSpeed = 0
        self.maxSpeed = 10
        self.minSpeedX = -20
        self.maxSpeedX = 20
        self.screenWidth = width
        self.screenHeight = height

    def apply_drag(self):
        self.speed *= .95
        self.speedX *= .9
    
    def physics(self):
        self.x += self.speedX

        self.rect.x = self.x
        
        #if self.x > self.screenWidth:
        #    self.x = self.screenWidth
        #if self.x < 0:
        #    self.x = 0

    def accelerate(self):
        self.speed += .5
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
    
    def decelerate(self):
        car.speed -= 1
        if self.speed < self.minSpeed:
            self.speed = self.minSpeed

    def left(self):
        if(self.speed > 0):
            self.speedX -= 0.5
            if(self.speedX > self.maxSpeedX):
                self.speedX = self.maxSpeedX
    
    def right(self):
        if(self.speed > 0):
            self.speedX += 0.5
            if(self.speedX < self.minSpeedX):
                self.speedX = self.minSpeedX

    def update(self):
        self.physics()
        self.apply_drag()

    def getX(self):
        return self.x
