import pygame, sys
from pygame.locals import *

class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("car.png")
        #self.rect = self.image.get_rect()
        #self.rect.center = (screenWidth * .5, screenHeight * .75)
        #fixing it to not move but rather just change values for a centered camera
        self.x = screenWidth * .5
        self.y = screenHeight * .75
        self.speed = 0
        self.speedX = 0
        self.minSpeed = 0
        self.maxSpeed = 10
        self.minSpeedX = -1
        self.maxSpeedX = 1

    def apply_drag(self):
        self.speed *= .99 
    
    def physics(self):
        print(self.speedX)
        if(self.speedX > 0):
            self.speedX -= 0.01
        if(self.speedX < 0):
            self.speedX += 0.01
        print(self.speedX)
        car.x += self.speedX
        if car.x > screenWidth:
            car.x = screenWidth
        if car.x < 0:
            car.x = 0

    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            car.speed += .5
            if car.speed > car.maxSpeed:
                car.speed = car.maxSpeed
        elif keys[pygame.K_s]:
            car.speed -= 1
            if car.speed < car.minSpeed:
                car.speed = car.minSpeed
        if keys[pygame.K_d] and car.speed > 0:
            car.speedX += 0.1
            if(car.speedX > car.maxSpeedX):
                car.speedX = car.maxSpeedX
        elif keys[pygame.K_a] and car.speed > 0:
            car.speedX -= 0.1
            if(car.speedX < car.minSpeedX):
                car.speedX = car.minSpeedX

    def update(self):
        self.physics()
        self.check_input()
        self.apply_drag()
