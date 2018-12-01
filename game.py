#game.py
#mostly game loop code here
import time
import pygame, sys

class Game:
    def __init__(self, canvas_width, canvas_height):
        self.width = canvas_width
        self.height = canvas_height
    def start(self, fps):
        #start the game loop given frames per second
        self.millisBetweenTicks = (1/fps) * 1000
        self.lastTick = int(time.time() * 1000)
        self.tick()
    def createscreen(self):        
        return pygame.display.set_mode((self.width, self.height))
    def tick(self):
        #this is the game loop
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            if(int(time.time()*1000) > self.lastTick + self.millisBetweenTicks):
                self.lastTick = int(time.time() * 1000)
                self.update()
    def update(self):
        #this should be overridden with custom game code that gets called every tick
        pass

